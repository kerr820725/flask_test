from typing import Dict

import cx_Oracle
import pymysql

from utils.Logger import create_logger

logger = create_logger(log_folder='/logger', log_name='Connection')


def get_oracle_conn(env):  # 連結數據庫 env 0: dev02 , 1:188
    if env == 2:
        username = 'rdquery'
        service_name = 'gamenxsXDB'
    else:
        username = 'firefog'
        service_name = ''
    oracle_ = {'password': ['LF64qad32gfecxPOJ603', 'JKoijh785gfrqaX67854', 'eMxX8B#wktFZ8V'],
               'ip': ['10.13.22.161', '10.6.1.41', '10.6.1.31'],
               'sid': ['firefog', 'game', '']}
    conn = cx_Oracle.connect(username, oracle_['password'][env], oracle_['ip'][env] + ':1521/' +
                             oracle_['sid'][env] + service_name)
    return conn


def get_sql_exec(env, sql):
    logger.info(f'get_sql_exec : sql = {sql}')
    cursor = get_oracle_conn(env).cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    result = []

    for i in rows:
        result.append(i[0])
    cursor.close()
    return result


def select_domain_default_url(conn, domain):
    with conn.cursor() as cursor:
        sql = "select GDL.domain, GDL.agent, UU.url, GDL.register_display, GDL.app_download_display, GDL.domain_type, GDL.status " \
              "from GLOBAL_DOMAIN_LIST GDL " \
              "inner join user_url UU on GDL.register_url_id = UU.id " \
              f"where GDL.domain = '{domain}'"
        logger.info(f'get_domain_default_url sql = {sql}')
        cursor.execute(sql)
        rows = cursor.fetchall()
        domain_urls = []
        for num, data in enumerate(rows):
            domain_urls.append(list(data))
        logger.info(f'get domain_urls = {domain_urls}')
    conn.close()
    return domain_urls


def select_url_token(conn, token, joint_venture):  # 輸入 token 查詢 連結
    with conn.cursor() as cursor:
        if len(token) == 4:  # 代表是用 註冊碼  ,4位
            sql = "select UC.account,UU.url " \
                  "from user_customer UC " \
                  "inner join user_url UU  on UC.id= UU.creator  " \
                  f"where UU.url like  '%token={token}%' and UC.joint_venture = {joint_venture}"
        else:  # 使用id 去找 url
            sql = "select UC.account,UU.url " \
                  "from user_customer UC " \
                  "inner join user_url UU  on UC.id= UU.creator " \
                  f"where UU.url like  '%id={token}%' and UC.joint_venture = {joint_venture}"
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        token_url = []
        for num, user in enumerate(rows):
            token_url.append(list(user))
    conn.close()
    return token_url


def select_sun_user(conn, user, type_, domain):
    if domain == '1':  # 申博
        come_from = 'sunGame138'
        note = '申博138'
    elif domain == '0':  # 太陽城
        come_from = 'sunGame'
        note = '太阳城'
    else:
        raise Exception('get_sun_user 無對應domain')

    with conn.cursor() as cursor:
        if type_ == 1:  # 1 查詢轉移的用戶
            sql = "select account, cellphone, transfer_status, transfer_date " \
                  "from sun_game_user " \
                  f"where transfer_status = 1 and come_from = '{come_from}' " \
                  "order by transfer_date desc"
        elif type_ == 2:  # 查詢 指定domain flask_test. sun_user2()
            sql = "select GDL.domain,GDL.agent,b.url,GDL.register_display,GDL.status,GDL.note,b.days,b.registers " \
                  "from  GLOBAL_DOMAIN_LIST GDL " \
                  "inner join user_url b on GDL.register_url_id = b.id " \
                  f"where note = '{note}' " \
                  "order by GDL.status asc,b.registers desc"
        else:  # 查詢 指定用戶
            sql = "select * " \
                  "from sun_game_user " \
                  f"where account = '{user}' and come_from = '{come_from}'"
        print(f'get_sun_user - > sql = {sql}')
        cursor.execute(sql)
        rows = cursor.fetchall()
        sun_user = []
        for num, tuple_ in enumerate(rows):  # i 生成tuple
            sun_user[num] = list(tuple_)
    conn.close()
    return sun_user


def select_user_url(conn, _user, _type=1, _joint_type=''):  # 用戶的 連結 ,type= 1 找用戶本身開戶連結, 0 找用戶的從哪個連結開出
    with conn.cursor() as cursor:
        user_url = []
        if _type == 1:  # 這邊user參數 為 userid , test_applycenter()方法使用
            sql = "select url " \
                  "from user_url " \
                  f"where url like '%{_user}%' and days=-1"
        elif _type == 2:  # user 為用戶名,這個表如果沒有, 有可能是 上級開戶連結 刪除,導致空 ,再去做else 那段
            sql = "select UC.account, UU.url, UC.user_chain, UC.device, UU.days " \
                  "from user_customer UC " \
                  "inner join  user_url UU on UC.url_id = UU.id " \
                  f"where UC.account = '{_user}' and joint_venture = '{_joint_type}'"
        else:  # 最後才去用 user_customer. referer 去找, 這邊APP 開戶出來的會是null
            sql = "select account, referer, user_chain, device " \
                  "from user_customer " \
                  f"where account = '{_user}' and joint_venture = '{_joint_type}'"
        logger.info(f'select_user_url -> sql : {sql}')
        cursor.execute(sql)
        rows = cursor.fetchall()
        for num, url in enumerate(rows):
            user_url.append(list(url))
        # if isinstance(user_url, list) is True:  # 為list
        #     for i in rows:
        #         user_url.append(i[0])
        # else:  # user_url 為dict
        #     for num, _user in enumerate(rows):
        #         user_url[num] = list(_user)
    conn.close()
    return user_url


def select_user_id(conn, account_, joint_type=None):
    with conn.cursor() as cursor:
        if joint_type is None:
            sql = "select id " \
                  "from user_customer " \
                  f"where account = '{account_}'"
        else:
            sql = "select id " \
                  "from user_customer " \
                  f"where account = '{account_}' and joint_venture = '{joint_type}'"
        print(f'get_user_id -> sql : {sql}')
        cursor.execute(sql)
        rows = cursor.fetchall()
        user_id = []

        for i in rows:
            print(f'i : {i}')
            user_id.append(i[0])
    conn.close()
    return user_id


def select_red_fund(conn, user, type_=None):  # 充值 紅包 查尋  各充值表
    with conn.cursor() as cursor:
        if type_ == 0:  # 新手任務
            sql = "select UC.account,BM.cancel_reason " \
                  "from BEGIN_MISSION BM " \
                  "inner join user_customer UC on  BM.user_id = UC.id  " \
                  f"where UC.is_freeze = 0 and UC.account = '{user}'"
        elif type_ == 1:  # 活動充值表
            sql = "select UC.account, AFOR.THE_DAY " \
                  "from ACTIVITY_FUND_OPEN_RECORD  AFOR " \
                  "inner join user_customer UC on AFOR.user_id = UC.id " \
                  f"where UC.account = '{user}'"
        elif type_ == 2:  # 資金異動表'
            sql = "select UC.account,FCL.sn,FCL.GMT_CREATED " \
                  "from fund_change_log FCL " \
                  "inner join user_customer UC on FCL.user_id = UC.id " \
                  f"where UC.account = '{user}' and  FCL.reason like '%ADAL%'"
        elif type_ == 3:  # 資金異動表 搬動
            sql = "select UC.account,FCLH.sn,FCLH.GMT_CREATED " \
                  "from fund_change_log_hist FCLH " \
                  "inner join user_customer UC on FCLH.user_id = UC.id " \
                  f"where UC.account = '{user}' and  FCLH.reason like '%ADAL%'"
        else:  # - 判斷 是否有領過 首充附言鼓励金
            sql = "select REL.amount " \
                  "from  RED_ENVELOPE_LIST  REL " \
                  "inner join  user_customer UC on REL.user_id  = UC.id " \
                  f"where UC.account = '{user}' and note = '首充附言鼓励金'"
        logger.info(f'get_red_fund -> sql = {sql}')
        cursor.execute(sql)
        rows = cursor.fetchall()
        fund_ = []
        for index, data in enumerate(rows):
            fund_.append(list(data))
    conn.close()
    return fund_


def get_mysql_conn(evn, third):  # 第三方  mysql連線
    third_dict = {'lc': ['lcadmin', ['cA28yF#K=yx*RPHC', 'XyH]#xk76xY6e+bV'], 'ff_lc'],
                  'ky': ['kyadmin', ['ALtfN#F7Zj%AxXgs=dT9', 'kdT4W3#dEug3$pMM#z7q'], 'ff_ky'],
                  'city': ['761cityadmin', ['KDpTqUeRH7s-s#D*7]mY', 'bE%ytPX$5nU3c9#d'], 'ff_761city'],
                  'im': ['imadmin', ['D97W#$gdh=b39jZ7Px', 'nxDe2yt7XyuZ@CcNSE'], 'ff_im'],
                  'shaba': ['sbadmin', ['UHRkbvu[2%N=5U*#P3JR', 'aR8(W294XV5KQ!Zf#"v9'], 'ff_sb'],
                  'bbin': ['bbinadmin', 'Csyh*P#jB3y}EyLxtg', 'ff_bbin'],
                  'gns': ['gnsadmin', 'Gryd#aCPWCkT$F4pmn', 'ff_gns']
                  }
    if evn == 0:  # dev
        ip = '10.13.22.151'
    elif evn == 1:  # 188
        ip = '10.6.32.147'
    else:
        raise Exception('evn 錯誤')

    user_ = third_dict[third][0]
    db_ = third_dict[third][2]

    if third == 'gns':  # gns只有一個 測試環境
        password_ = third_dict[third][1]
        ip = '10.6.32.147'  # gns Db 只有 188
    else:
        password_ = third_dict[third][1][evn]

    db = pymysql.connect(
        host=ip,
        user=user_,
        passwd=password_,
        db=db_)
    return db


def thirdly_tran(db, tran_type, third, user) -> list:
    cur = db.cursor()
    # third 判斷 第三方 是那個 ,gns table 名稱不同
    if third in ['lc', 'ky', 'city', 'im', 'shaba']:
        table_name = 'THIRDLY_TRANSCATION_LOG'
        if tran_type == 0:  # 轉入
            trans_name = 'FIREFROG_TO_THIRDLY'
        else:  # 轉出
            trans_name = 'THIRDLY_TO_FIREFROG'
    elif third == 'gns':
        table_name = 'GNS_TRANSCATION_LOG'
        if tran_type == 0:  # gns轉入
            trans_name = 'FIREFROG_TO_GNS'
        else:
            trans_name = 'GNS_TO_FIREFROG'
    else:
        print('第三方 名稱錯誤')

    sql = f"SELECT SN,STATUS FROM {table_name} WHERE FF_ACCOUNT = '{user}'\
    AND CREATE_DATE > DATE(NOW()) AND TRANS_NAME= '{trans_name}'"

    cur.execute(sql)
    for row in cur.fetchall():
        result = [row[0], row[1]]
        return result


def select_domain_url(conn, domain) -> Dict[int, list]:  # 查詢 全局管理 後台設置的domain ,連結設置 (因為生產 沒權限,看不到)
    with conn.cursor() as cursor:
        sql = f"select a.domain,a.agent,b.url,a.register_display,a.app_download_display,a.domain_type,a.status from  \
        GLOBAL_DOMAIN_LIST a inner join user_url b \
        on a.register_url_id = b.id  where a.domain like '%{domain}%' "
        cursor.execute(sql)
        rows = cursor.fetchall()
        domain_url = {}
        for num, url in enumerate(rows):
            domain_url[num] = list(url)
        # print(domain_url)
    conn.close()
    return domain_url


def select_game_result(conn, result) -> list:  # 查詢用戶訂單號, 回傳訂單各個資訊
    with conn.cursor() as cursor:
        sql = f"select a.order_time,a.status,a.totamount,f.lottery_name,\
        c.group_code_title,c.set_code_title,c.method_code_title,\
        b.bet_detail,e.award_name,b.award_mode,b.ret_award,b.multiple,b.money_mode,b.evaluate_win\
        ,a.lotteryid,b.bet_type_code,c.theory_bonus,a.award_group_id\
        from(((\
        (game_order a inner join game_slip b on\
        a.id = b.orderid and a.userid=b.userid and a.lotteryid=b.lotteryid) inner join \
        game_bettype_status c on \
        a.lotteryid = c.lotteryid and b.bet_type_code=c.bet_type_code) inner join\
        game_award_user_group d on\
        a.lotteryid = d.lotteryid and a.userid=d.userid) inner join \
        game_award_group e on \
        a.award_group_id = e.id and a.lotteryid =e.lotteryid) \
        inner join game_series f on  a.lotteryid = f.lotteryid where a.order_code = '{result}' and d.bet_type=1"
        cursor.execute(sql)
        rows = cursor.fetchall()
        detail_list = []  # 存放各細節
        # game_detail[result] = detail_list# 讓訂單為key,　value 為一個list 存放各訂單細節
        for tuple_ in rows:
            for i in tuple_:
                # print(i)
                detail_list.append(i)
    conn.close()
    return detail_list


def select_game_order(conn, play_type):  # 輸入玩法,找尋訂單
    with conn.cursor() as cursor:
        sql = f"select f.lottery_name,a.order_time,a.order_code,\
        c.group_code_title,c.set_code_title,c.method_code_title,a.status,g.account,b.bet_detail,h.number_record\
        from((((((\
        game_order a inner join  game_slip b on \
        a.id = b.orderid and a.userid=b.userid and a.lotteryid=b.lotteryid) inner join game_bettype_status c on \
        a.lotteryid = c.lotteryid and b.bet_type_code=c.bet_type_code) \
        inner join game_award_user_group d on \
        a.lotteryid = d.lotteryid and a.userid=d.userid) \
        inner join game_award_group e on \
        a.award_group_id = e.id and a.lotteryid =e.lotteryid) \
        inner join game_series f on a.lotteryid = f.lotteryid) inner join user_customer g on\
        a.userid = g.id and d.userid = g.id) inner join game_issue h on\
        a.lotteryid = h.lotteryid and a.issue_code = h.issue_code\
        where a.order_time >sysdate - interval '1' month and \
        c.group_code_title||c.set_code_title||c.method_code_title like '{play_type}' and d.bet_type=1  and a.status !=1 \
        order by a.order_time desc"
        cursor.execute(sql)
        rows = cursor.fetchall()
        game_order = {}
        len_order = len(rows)  # 需傳回去長度
        # print(rows,len(rows))#rows 為一個 list 包 tuple
        order_list = []  # 存放指定玩法 產生 的多少訂單
        for index, tuple_ in enumerate(rows):  # 取出 list長度 的各訂單 tuple
            order_list.append(list(tuple_))  # 把tuple 轉乘list  ,然後放入  order_list
            game_order[index] = order_list[index]  # 字典 index 為 key ,  order_list 為value
        # print(game_order)
    conn.close()
    return [game_order, len_order]


def select_active_app(conn, user):  # 查詢APP 是否為有效用戶表
    with conn.cursor() as cursor:
        sql = f"select *  from USER_CENTER_THIRDLY_ACTIVE where \
        create_date >=  trunc(sysdate,'mm') and user_id in \
        ( select id from user_customer where account = '{user}')"
        cursor.execute(sql)
        rows = cursor.fetchall()
        active_app = []
        for tuple_ in rows:
            for i in tuple_:
                # print(i)
                active_app.append(i)
        # print(active_app,len(active_app))
    conn.close()
    return active_app


def select_app_bet(conn, user):  # 查詢APP 代理中心 銷量
    with conn.cursor() as cursor:
        app_bet = {}
        for third in ['ALL', 'LC', 'KY', 'CITY', 'GNS', 'FHLL', 'BBIN', 'IM', 'SB', 'AG']:
            if third == 'ALL':
                sql = f"select sum(bet) 總投注額 ,sum(cost) 用戶總有效銷量, sum(prize)總獎金 ,sum(bet)- sum(prize)用戶總盈虧 \
                from V_THIRDLY_AGENT_CENTER where account = '{user}' \
                and create_date > trunc(sysdate,'mm')"
            else:
                sql = f"select sum(bet) 總投注額 ,sum(cost) 用戶總有效銷量, sum(prize)總獎金 ,sum(bet)- sum(prize)用戶總盈虧 \
                from V_THIRDLY_AGENT_CENTER where account = '{user}' \
                and create_date > trunc(sysdate,'mm') and plat='{third}'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            new_ = []  # 存放新的列表內容
            for tuple_ in rows:
                for i in tuple_:
                    if i is None:  # 就是 0
                        i = 0
                    new_.append(i)
                app_bet[third] = new_

        print(app_bet)
    conn.close()
    return app_bet


def select_active_card(conn, user, envs):  # 查詢綁卡是否有重複綁
    with conn.cursor() as cursor:
        if envs == 2:  # 生產另外一張表
            sql = f"SELECT bank_number, count(id) FROM rd_view_user_bank \
            WHERE bank_number in (SELECT bank_number FROM rd_view_user_bank WHERE account = '{user}' \
            ) group BY bank_number"
        else:
            sql = f"SELECT BANK_NUMBER,count(user_id) FROM USER_BANK \
            WHERE BANK_NUMBER in \
            (SELECT BANK_NUMBER FROM USER_BANK WHERE USER_ID= \
            (SELECT ID FROM USER_CUSTOMER WHERE ACCOUNT='{user}')) \
            group by bank_number"
        cursor.execute(sql)
        rows = cursor.fetchall()
        card_num = {}
        for index, tuple_ in enumerate(rows):
            card_num[index] = list(tuple_)
        # print(card_num)
    conn.close()
    return card_num


def select_active_fund(conn, user):  # 查詢當月充值金額
    with conn.cursor() as cursor:
        sql = f"select sum(real_charge_amt) from fund_charge where status=2 and apply_time > trunc(sysdate,'mm')  \
              and user_id in ( select id from user_customer where account = '{user}')"
        cursor.execute(sql)
        rows = cursor.fetchall()
        user_fund = []  # 當月充值金額
        print(rows)
        for tuple_ in rows:
            for i in tuple_:
                # print(i)
                user_fund.append(i)
    conn.close()
    return user_fund


def select_issue(conn, lottery_id):  # 查詢正在銷售的 期號
    # Joy188Test.date_time()
    # today_time = '2019-06-10'#for 預售中 ,抓當天時間來比對,會沒獎期
    try:
        with conn.cursor() as cursor:
            sql = f"select web_issue_code,issue_code from game_issue where lotteryid = '{lottery_id}' and sysdate between sale_start_time and sale_end_time"

            cursor.execute(sql)
            rows = cursor.fetchall()

            issueName = []
            issue = []

            if lottery_id in ['99112', '99306']:  # 順利秒彩,順利11選5  不需 講期. 隨便塞
                issueName.append('1')
                issue.append('1')
            else:
                for i in rows:  # i 生成tuple
                    issueName.append(i[0])
                    issue.append(i[1])
        conn.close()
        return {'issueName': issueName, 'issue': issue}
    except:
        pass


def select_red_id(conn, user):  # 紅包加壁  的訂單號查詢 ,用來審核用
    with conn.cursor() as cursor:
        sql = f"SELECT ID FROM RED_ENVELOPE_LIST WHERE status=1 and \
        USER_ID = (SELECT id FROM USER_CUSTOMER WHERE account ='{user}')"
        cursor.execute(sql)
        rows = cursor.fetchall()

        red_id = []
        for i in rows:  # i 生成tuple
            red_id.append(i[0])
    conn.close()
    return red_id


def select_red_bal(conn, user) -> list:
    with conn.cursor() as cursor:
        sql = f"SELECT bal FROM RED_ENVELOPE WHERE \
        USER_ID = (SELECT id FROM USER_CUSTOMER WHERE account ='{user}')"
        cursor.execute(sql)
        rows = cursor.fetchall()

        red_bal = []
        for i in rows:  # i 生成tuple
            red_bal.append(i[0])
    conn.close()
    return red_bal
