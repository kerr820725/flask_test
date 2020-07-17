import threading
import unittest
from time import sleep

from bs4 import BeautifulSoup
import hashlib
import json
import requests
import time

from utils import Config, Logger, Connection
from utils.Config import LotteryData, func_time

logger = Logger.create_logger(r"\AutoTest", 'auto_test_pc')


class ApiTestPC(unittest.TestCase):
    u"PC接口測試"
    envConfig = None
    user = None
    red_type = None
    money_unit = None

    def setUp(self):
        logger.info('ApiTestPC setUp : {}'.format(self._testMethodName))

    def __init__(self, case, _env, _user, _red_type, _money_unit):
        super().__init__(case)
        # if not logger:
        #     logger = Logger.create_logger(r"\ApiTestPC")
        self.envConfig = _env
        self.user = _user
        self.red_type = _red_type
        self.money_unit = _money_unit
        logger.info('ApiTestPC __init__.')

    def md(self, _password, _param):
        m = hashlib.md5()
        m.update(_password)
        sr = m.hexdigest()
        for i in range(3):
            sr = hashlib.md5(sr.encode()).hexdigest()
        rx = hashlib.md5(sr.encode() + _param).hexdigest()
        return rx

    def select_issue(self, conn, lotteryid):  # 查詢正在銷售的 期號
        # Joy188Test.date_time()
        # today_time = '2019-06-10'#for 預售中 ,抓當天時間來比對,會沒獎期
        try:
            with conn.cursor() as cursor:
                sql = "select web_issue_code,issue_code from game_issue where lotteryid = '%s' and sysdate between sale_start_time and sale_end_time" % (
                    lotteryid)

                cursor.execute(sql)
                rows = cursor.fetchall()

                issueName = []
                issue = []

                if lotteryid in ['99112', '99306']:  # 順利秒彩,順利11選5  不需 講期. 隨便塞
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

    def select_red_bal(self, conn, user) -> list:
        with conn.cursor() as cursor:
            sql = "SELECT bal FROM RED_ENVELOPE WHERE \
            USER_ID = (SELECT id FROM USER_CUSTOMER WHERE account ='%s')" % user
            cursor.execute(sql)
            rows = cursor.fetchall()

            red_bal = []
            for i in rows:  # i 生成tuple
                red_bal.append(i[0])
        conn.close()
        return red_bal

    def select_red_id(self, conn, user):  # 紅包加壁  的訂單號查詢 ,用來審核用
        with conn.cursor() as cursor:
            sql = "SELECT ID FROM RED_ENVELOPE_LIST WHERE status=1 and \
            USER_ID = (SELECT id FROM USER_CUSTOMER WHERE account ='%s')" % user
            cursor.execute(sql)
            rows = cursor.fetchall()

            red_id = []
            for i in rows:  # i 生成tuple
                red_id.append(i[0])
        conn.close()
        return red_id

    def web_issuecode(self, lottery):  # 頁面產生  獎期用法,  取代DB連線問題
        now_time = int(time.time())
        header = {
            'User-Agent': userAgent,
            'Cookies': 'ANVOID=' + cookies_[user]
        }
        r = session.get(em_url + '/gameBet/%s/lastNumber?_=%s' % (lottery, now_time), headers=header)
        try:
            return r.json()['issueCode']
        except:
            pass
        if lottery == 'lhc':
            pass

    def plan_num(self, evn, lottery, plan_len):  # 追號生成
        plan_ = []  # 存放 多少 長度追號的 list
        issue = self.select_issue(Connection.get_conn(evn), LotteryData.lottery_dict[lottery][1])
        for i in range(plan_len):
            plan_.append({"number": issue.get('issueName')[i], "issueCode": issue.get('issue')[i], "multiple": 1})
        return plan_

    def ball_type(self, test):  # 對應完法,產生對應最大倍數和 投注完法
        ball = []
        global mul
        if test == 'wuxing':

            ball = [str(Config.random_mul(9)) for i in range(5)]  # 五星都是數值
            mul = Config.random_mul(2)
        elif test == 'sixing':
            ball = ['-' if i == 0 else str(Config.random_mul(9)) for i in range(5)]  # 第一個為-
            mul = Config.random_mul(22)
        elif test == 'housan':
            ball = ['-' if i in [0, 1] else str(Config.random_mul(9)) for i in range(5)]  # 第1和2為-
            mul = Config.random_mul(222)
        elif test == 'qiansan':
            ball = ['-' if i in [3, 4] else str(Config.random_mul(9)) for i in range(5)]  # 第4和5為-
            mul = Config.random_mul(222)
        elif test == 'zhongsan':
            ball = ['-' if i in [0, 4] else str(Config.random_mul(9)) for i in range(5)]  # 第2,3,4為-
            mul = Config.random_mul(222)
        elif test == 'houer':
            ball = ['-' if i in [0, 1, 2] else str(Config.random_mul(9)) for i in range(5)]  # 第1,2,3為-
            mul = Config.random_mul(2222)
        elif test == 'qianer':
            ball = ['-' if i in [2, 3, 4] else str(Config.random_mul(9)) for i in range(5)]  # 第3,4,5為-
            mul = Config.random_mul(2222)
        elif test == 'yixing':  # 五個號碼,只有一個隨機數值
            ran = Config.random_mul(4)
            ball = ['-' if i != ran else str(Config.random_mul(9)) for i in range(5)]
            mul = Config.random_mul(2222)
        else:
            mul = Config.random_mul(1)
        a = (",".join(ball))
        return a

    def game_type(self, lottery):
        # test___ = play_type()

        game_group = {'wuxing': u'五星', 'sixing': u'四星', 'qiansan': u'前三', 'housan': u'後三',
                      'zhongsan': u'中三', 'qianer': u'前二', 'houer': u'後二', 'xuanqi': u'選ㄧ', 'sanbutonghao': u'三不同號',
                      'santonghaotongxuan': u'三同號通選', 'guanya': u'冠亞', 'biaozhuntouzhu': u'標準玩法', 'zhengma': u'正碼',
                      'p3sanxing': u'P3三星', 'renxuan': u'任選'}

        game_set = {
            'zhixuan': u'直選', 'renxuanqizhongwu': u'任選一中一', 'biaozhun': u'標準', 'zuxuan': u'組選'
            , 'pingma': u'平碼', 'putongwanfa': u'普通玩法'}
        game_method = {
            'fushi': u'複式', 'zhixuanfushi': u'直選複式', 'zhixuanliuma': u'直選六碼',
            'renxuan7': u'任選7'
        }

        group_ = Config.play_type()  # 建立 個隨機的goup玩法 ex: wuxing,目前先給時彩系列使用
        # set_ = game_set.keys()[0]#ex: zhixuan
        # method_ = game_method.keys()[0]# ex: fushi
        play_ = ''

        # play_ = ''#除了 不是 lottery_sh 裡的彩種

        lottery_ball = self.ball_type(group_)  # 組出什麼玩法 的 投注內容 ,目前只有給時彩系列用

        test_dicts = {
            0: ["%s.zhixuan.fushi" % (group_,), lottery_ball],
            1: ["qianer.zhixuan.zhixuanfushi", '3,6,-'],
            2: ["xuanqi.renxuanqizhongwu.fushi", "01,02,05,06,08,09,10"],
            3: ["sanbutonghao.biaozhun.biaozhuntouzhu", "1,2,6"],
            4: ["santonghaotongxuan.santonghaotongxuan.santonghaotongxuan", "111 222 333 444 555 666"],
            5: ["guanya.zhixuan.fushi", "09 10,10,-,-,-,-,-,-,-,-"],
            6: ['qianer.zuxuan.fushi', '4,8'],
            7: ["biaozhuntouzhu.biaozhun.fushi", "04,08,13,19,24,27+09", ],
            8: ["zhengma.pingma.zhixuanliuma", "04"],
            9: ["p3sanxing.zhixuan.p3fushi", "9,1,0", ],
            10: ["renxuan.putongwanfa.renxuan7", "09,13,16,30,57,59,71"],
            11: ["chungtienpao.chungtienpao.chungtienpao", "1.01"]  # 快開
        }

        if lottery in LotteryData.lottery_sh:  # 時彩系列
            num = 0
            play_ = u'玩法名稱: %s.%s.%s' % (game_group[group_], game_set['zhixuan'],
                                         game_method['fushi'])

        elif lottery in LotteryData.lottery_3d:
            num = 1
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['qianer'], game_set['zhixuan'],
                                         game_method['zhixuanfushi'])
        elif lottery in LotteryData.lottery_noRed:
            if lottery in ['p5', 'np3']:
                num = 9
                play_ = u'玩法名稱: %s.%s.%s' % (game_group['p3sanxing'], game_set['zhixuan'],
                                             game_method['fushi'])
            else:
                num = 1
                play_ = u'玩法名稱: %s.%s.%s' % (game_group['qianer'], game_set['zhixuan'],
                                             game_method['zhixuanfushi'])
        elif lottery in LotteryData.lottery_115:
            num = 2
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['xuanqi'], game_set['renxuanqizhongwu'],
                                         game_method['fushi'])
        elif lottery in LotteryData.lottery_k3:
            num = 3
            play_ = u'玩法名稱: %s.%s' % (game_group['sanbutonghao'], game_set['biaozhun'])
        elif lottery in LotteryData.lottery_sb:
            num = 4
            play_ = u'玩法名稱: %s' % (game_group['santonghaotongxuan'])
        elif lottery in LotteryData.lottery_fun:
            num = 5
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['guanya'], game_set['zhixuan'],
                                         game_method['fushi'])
        elif lottery == 'shssl':
            num = 6
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['qianer'], game_set['zuxuan'],
                                         game_method['fushi'])
        elif lottery == 'ssq':
            num = 7
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['biaozhuntouzhu'], game_set['biaozhun'],
                                         game_method['fushi'])
        elif lottery == 'lhc':
            num = 8
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['zhengma'], game_set['pingma'],
                                         game_method['zhixuanliuma'])
        elif lottery == 'p5':
            num = 9
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['p3sanxing'], game_set['zhixuan'],
                                         game_method['fushi'])
        elif lottery == 'bjkl8':
            num = 10
            play_ = u'玩法名稱: %s.%s.%s' % (game_group['renxuan'], game_set['putongwanfa'],
                                         game_method['renxuan7'])
        else:
            num = 11
            # play_ = u'玩法名稱: 沖天炮
        return test_dicts[num][0], test_dicts[num][1], play_

    def req_post_submit(self, account, lottery, data_, moneyunit, awardmode, play_):
        logger.info(
            'account: {}, lottery: {}, data_: {}, moneyunit: {}, awardmode: {}, play_ {}'.format(account, lottery,
                                                                                                 data_, moneyunit,
                                                                                                 awardmode, play_))
        awardmode_dict = {0: u"非一般模式", 1: u"非高獎金模式", 2: u"高獎金"}
        money_dict = {1: u"元模式", 0.1: u"分模式", 0.01: u"角模式"}
        while True:
            header = {
                'Cookie': "ANVOID=" + cookies_[account],
                'User-Agent': userAgent
            }

            r = session.post(em_url + '/gameBet/' + lottery + '/submit',
                             data=json.dumps(data_), headers=header)

            global content_
            try:
                # print(r.json())
                msg = (r.json()['msg'])
                mode = money_dict[moneyunit]
                mode1 = awardmode_dict[awardmode]
                project_id = (r.json()['data']['projectId'])  # 訂單號
                submit_amount = (r.json()['data']['totalprice'])  # 投注金額
                # submit_mul = u"投注倍數: %s"%m#隨機倍數
                lottery_name = u'投注彩種: %s' % LotteryData.lottery_dict[lottery][0]

                if r.json()['isSuccess'] == 0:  #
                    # select_issue(get_conn(envs),lottery_dict[lottery][1])#呼叫目前正在販售的獎期
                    content_ = (lottery_name + "\n" + mul_ + "\n" + play_ + "\n" + msg + "\n")
                    # print(content_)

                    if r.json()['msg'] == u'存在封锁变价':  # 有可能封鎖變價,先跳過   ()
                        break
                    elif r.json()['msg'] == u'您的投注内容 超出倍数限制，请调整！':
                        print(u'倍數超出了唷,下次再來')
                        break
                    elif r.json()['msg'] == u'方案提交失败，请检查网络并重新提交！':
                        print(r.json()['msg'])
                        break
                    else:  # 系統內部錯誤
                        print(r.json()['msg'])
                        break
                else:  # 投注成功
                    if self.red_type == 'yes':
                        content_ = (lottery_name + "\n" + u'投注單號: ' + project_id + "\n"
                                    + mul_ + "\n"
                                    + play_ + "\n" + u"投注金額: " + str(float(submit_amount * 0.0001)) + "\n"
                                    + "紅包金額: 2" + mode + "/" + mode1 + "\n" + msg + "\n")
                    else:
                        content_ = (lottery_name + "\n" + u'投注單號: ' + project_id + "\n"
                                    + mul_ + "\n"
                                    + play_ + "\n" + u"投注金額: " + str(float(submit_amount * 0.0001)) + "\n"
                                    + mode + "/" + mode1 + "\n" + msg + "\n")
                    break
            except ValueError:
                content_ = ('%s 投注失敗' % lottery + "\n")
                break
        print(content_)

    def test_PCLotterySubmit(self, plan=1):  # 彩種投注
        """投注測試"""
        _money_unit = 1  # 初始元模式

        if self.red_type == 'yes':
            print('使用紅包投注')
        else:
            print('不使用紅包投注')
        while True:
            try:
                for i in LotteryData.lottery_dict.keys():
                    global mul_  # 傳回 投注出去的組合訊息 req_post_submit 的 content裡
                    global mul
                    ball_type_post = self.game_type(i)  # 找尋彩種後, 找到Mapping後的 玩法後內容

                    award_mode = 1

                    if self.money_unit == '1':  # 使用元模式
                        _money_unit = 1
                    elif self.money_unit == '2':  # 使用角模式
                        _money_unit = 0.1

                    if i == 'btcctp':
                        award_mode = 2
                        mul = Config.random_mul(1)  # 不支援倍數,所以random參數為1
                    elif i == 'bjkl8':
                        mul = Config.random_mul(5)  # 北京快樂8
                    elif i == 'p5':
                        mul = Config.random_mul(5)

                    elif i in ['btcffc', 'xyft']:
                        award_mode = 2
                    elif i in LotteryData.lottery_sb:  # 骰寶只支援  元模式
                        _money_unit = 1

                    mul_ = (u'選擇倍數: {}'.format(mul))
                    amount = 2 * mul * _money_unit

                    # 從DB抓取最新獎期.[1]為 99101類型select_issueselect_issue

                    if plan == 1:  # 一般投住

                        # Joy188Test.select_issue(Joy188Test.get_conn(1),lottery_dict[i][1])
                        # 從DB抓取最新獎期.[1]為 99101類型
                        # print(issueName,issue)
                        issuecode = self.web_issuecode(i)
                        plan_ = [{"number": '123', "issueCode": issuecode, "multiple": 1}]
                        print(u'一般投住')
                        isTrace = 0
                        traceWinStop = 0
                        traceStopValue = -1
                    else:  # 追號
                        plan_ = self.plan_num(envs, i, Config.random_mul(30))  # 隨機生成 50期內的比數
                        print(u'追號, 期數:%s' % len(plan_))
                        isTrace = 1
                        traceWinStop = 1
                        traceStopValue = 1

                    len_ = len(plan_)  # 一般投注, 長度為1, 追號長度為
                    # print(game_type)

                    post_data = {"gameType": i, "isTrace": isTrace, "traceWinStop": traceWinStop,
                                 "traceStopValue": traceWinStop,
                                 "balls": [{"id": 1, "ball": ball_type_post[1], "type": ball_type_post[0],
                                            "moneyunit": _money_unit, "multiple": mul, "awardMode": award_mode,
                                            "num": 1}], "orders": plan_, "amount": len_ * amount}  # 不使用紅包

                    post_data_lhc = {"balls": [{"id": 1, "moneyunit": _money_unit, "multiple": 1, "num": 1,
                                                "type": ball_type_post[0], "amount": amount, "lotterys": "13",
                                                "ball": ball_type_post[1], "odds": "7.5"}],
                                     "isTrace": 0, "orders": plan_,
                                     "amount": amount, "awardGroupId": 202}

                    post_data_sb = {"gameType": i, "isTrace": 0, "multiple": 1, "trace": 1,
                                    "amount": amount,
                                    "balls": [{"ball": ball_type_post[1],
                                               "id": 11, "moneyunit": _money_unit, "multiple": 1, "amount": amount,
                                               "num": 1,
                                               "type": ball_type_post[0]}],
                                    "orders": plan_}

                    if i in 'lhc':
                        self.req_post_submit(self.user, 'lhc', post_data_lhc, _money_unit, award_mode,
                                             ball_type_post[2])

                    elif i in LotteryData.lottery_sb:
                        self.req_post_submit(self.user, i, post_data_sb, _money_unit, award_mode, ball_type_post[2])
                    else:
                        if self.red_type == 'yes':  # 紅包投注
                            post_data['redDiscountAmount'] = 2  # 增加紅包參數
                            self.req_post_submit(self.user, i, post_data, _money_unit, award_mode, ball_type_post[2])
                        else:
                            self.req_post_submit(self.user, i, post_data, _money_unit, award_mode, ball_type_post[2])
                red_bal = self.select_red_bal(Connection.get_conn(1), user)
                print('紅包餘額: %s' % (int(red_bal[0]) / 10000))
                break
            except KeyError as e:
                print(u"輸入值有誤")
                break
            except IndexError as e:
                # print(e)
                break

    @func_time
    def test_PcLogin(self, source='Pc'):
        print("Enter test_PcLogin")
        u"登入測試"
        global user  # 傳給後面 PC 街口案例  request參數
        global password  # 傳入 werbdriver登入的密碼
        global post_url  # 非em開頭
        global em_url  # em開頭
        global userAgent
        global envs  # 回傳redis 或 sql 環境變數   ,dev :0, 188:1
        global cookies_
        global third_list
        third_list = ['gns', 'shaba', 'im', 'ky', 'lc', 'city']
        cookies_ = {}
        user = self.user
        account_ = {self.user: '輸入的用戶名'}
        em_url = self.envConfig.get_em_url()
        password = str.encode(self.envConfig.get_password())
        envs = self.envConfig.get_env_id()
        post_url = self.envConfig.get_post_url()

        param = b'f4a30481422765de945833d10352ea18'

        # 判斷從PC ,ios ,還世 andriod
        # global userAgent
        if source == 'Pc':
            userAgent = Config.UserAgent.PC.value

        elif source == 'Android':
            userAgent = Config.UserAgent.ANDROID.value

        elif source == 'Ios':
            userAgent = Config.UserAgent.IOS.value

        header = {
            'User-Agent': userAgent
        }
        print("userAgent : " + userAgent)
        print("post_url : " + post_url)
        global session
        while True:
            try:
                for i in account_.keys():
                    postData = {
                        "username": i,
                        "password": self.md(password, param),
                        "param": param
                    }
                    session = requests.Session()
                    r = session.post(post_url + '/login/login', data=postData, headers=header)
                    cookies = r.cookies.get_dict()  # 獲得登入的cookies 字典
                    cookies_.setdefault(i, cookies['ANVOID'])
                    t = time.strftime('%Y%m%d %H:%M:%S')
                    # msg = (u'登錄帳號: %s,登入身分: %s'%(i,account_[i])+u',現在時間:'+t+r.text)
                    print(u'登錄帳號: %s' % (i) + u',現在時間:' + t)
                    print(r.text)
                    print(r.json()['isSuccess'])

                    # return url
                break
            except requests.exceptions.ConnectionError:
                raise Exception("ConnectionError Exception")
                break

            except IOError:
                raise Exception('IOError Exception')
                break

    def session_post(self, account, third, url, post_data):  # 共用 session post方式 (Pc)
        header = {
            'User-Agent': userAgent,
            'Cookie': 'ANVOID=' + cookies_[account],
            'Content-Type': 'application/json; charset=UTF-8',
        }
        try:
            r = session.post(post_url + url, headers=header, data=json.dumps(post_data))

            if 'Balance' in url:
                print('%s, 餘額: %s' % (third, r.json()['balance']))
            elif 'transfer' in url:
                if r.json()['status'] == True:
                    print('帳號 kerrthird001 轉入 %s ,金額:1, 進行中' % third)
                else:
                    print('%s 轉帳失敗' % third)
            elif 'getuserbal' in url:
                print('4.0 餘額: %s' % r.json()['data'])
            # print(title)#強制便 unicode, 不燃顯示在html報告  會有誤
            # print('result: '+statu_code+"\n"+'---------------------')

        except requests.exceptions.ConnectionError:
            print(u'連線有問題,請稍等')

    def session_get(self, user, url_, url):  # 共用 session get方式
        header = {
            'User-Agent': userAgent,
            'Cookie': 'ANVOID=' + cookies_[user],
            'Content-Type': 'application/json; charset=UTF-8',
        }
        try:
            r = session.get(url_ + url, headers=header)
            html = BeautifulSoup(r.text, 'lxml')  # type為 bs4類型
            title = str(html.title)
            statu_code = str(r.status_code)  # int 轉  str

            print(title)  # 強制便 unicode, 不燃顯示在html報告  會有誤
            print(url)
            print('result: ' + statu_code + "\n" + '---------------------')

        except requests.exceptions.ConnectionError:
            print(u'連線有問題,請稍等')

    @func_time
    def test_PcThirdHome(self):  # 登入第三方頁面,創立帳號
        u"第三方頁面測試"
        threads = []
        third_url = ['gns', 'ag', 'sport', 'shaba', 'lc', 'im', 'ky', 'fhx', 'bc', 'fhll', 'bc']

        for i in third_url:
            if i == 'shaba':  # 沙巴特立
                url = '/shaba/home?act=esports'
            elif i == 'fhll':  # 真人特例
                fhll_dict = {'77104': u'樂利時彩', '77101': u'樂利1.5分彩',
                             '77103': u'樂利六合彩', '77102': u'樂利快3'}
                for i in fhll_dict.keys():
                    url = '/fhll/home/%s' % i
                    # print(url)
                    # print(fhll_dict[i])#列印 中文(因為fhll的title都是一樣)
                    t = threading.Thread(target=self.session_get, args=(user, post_url, url))
                    threads.append(t)
                    # Joy188Test.session_get(user,post_url,url)# get方法
                break  # 不再跑到 下面 session_get 的func
            elif i == 'fhx':
                url = '/fhx/index'
            else:
                url = '/%s/home' % i
            # print(url)
            t = threading.Thread(target=self.session_get, args=(user, post_url, url))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()

            # Joy188Test.session_get(user,post_url,url)

    @func_time
    def test_PcFFHome(self):
        u"4.0頁面測試"
        threads = []
        url_188 = ['/fund', '/bet/fuddetail', '/withdraw', '/transfer', '/index/activityMall'
            , '/ad/noticeList?noticeLevel=2', '/frontCheckIn/checkInIndex', '/frontScoreMall/pointsMall']
        em_188 = ['/gameUserCenter/queryOrdersEnter', '/gameUserCenter/queryPlans']
        for i in url_188:
            if i in ['/frontCheckIn/checkInIndex', '/frontScoreMall/pointsMall']:
                self.session_get(user, post_url, i)
            else:
                t = threading.Thread(target=self.session_get, args=(user, post_url, i))
                threads.append(t)
            # Joy188Test.session_get(user,post_url,i)
        for i in em_188:
            # Joy188Test.session_get(user,em_url,i)
            t = threading.Thread(target=self.session_get, args=(user, em_url, i))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()

    @func_time
    def test_PcChart(self):
        "走勢圖測試"
        ssh_url = ['cqssc', 'hljssc', 'tjssc', 'xjssc', 'llssc', 'txffc', 'btcffc', 'fhjlssc',
                   'jlffc', 'slmmc', 'sd115', 'll115', 'gd115', 'jx115']
        k3_url = ['jsk3', 'ahk3', 'jsdice', 'jldice1', 'jldice2']
        low_url = ['d3', 'v3d']
        fun_url = ['xyft', 'pk10']
        for i in ssh_url:
            self.session_get(user, em_url, '/game/chart/%s/Wuxing' % i)
        for i in k3_url:
            self.session_get(user, em_url, '/game/chart/%s/chart' % i)
        for i in low_url:
            self.session_get(user, em_url, '/game/chart/%s/Qiansan' % i)
        for i in fun_url:
            self.session_get(user, em_url, '/game/chart/%s/CaipaiweiQianfushi' % i)
        self.session_get(user, em_url, '/game/chart/p5/p5chart')
        self.session_get(user, em_url, '/game/chart/ssq/ssq_basic')
        self.session_get(user, em_url, '/game/chart/kl8/Quwei')

    @func_time
    def test_PcThirdBalance(self):
        '''4.0/第三方餘額'''
        threads = []

        header = {
            'User-Agent': userAgent,
            'Cookie': 'ANVOID=' + cookies_[user]
        }

        print('帳號: %s' % user)
        for third in third_list:
            if third == 'gns':
                third_url = '/gns/gnsBalance'
            else:
                third_url = '/%s/thirdlyBalance' % third
                # r = session.post(post_url+third_url,headers=header)
            # print('%s, 餘額: %s'%(third,r.json()['balance']))
            t = threading.Thread(target=self.session_post, args=(user, third, third_url, ''))
            threads.append(t)
        t = threading.Thread(target=self.session_post, args=(user, '', '/index/getuserbal', ''))
        threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        '''
        r = session.post(post_url+'/index/getuserbal',headers=header)
        print('4.0 餘額: %s'%r.json()['data'])
        '''

    @func_time
    def test_PcTransferin(self):  # 第三方轉入
        '''第三方轉入'''
        header = {
            'User-Agent': userAgent,
            'Cookie': 'ANVOID=' + cookies_[user],
            'Content-Type': 'application/json; charset=UTF-8'
        }
        post_data = {"amount": 1}
        statu_dict = {}  # 存放 轉帳的 狀態
        for third in third_list:
            if third == 'gns':
                third_url = '/gns/transferToGns'
            else:
                third_url = '/%s/transferToThirdly' % third
            r = session.post(post_url + third_url, data=json.dumps(post_data), headers=header)

            # t = threading.Thread(target=Joy188Test.session_post,args=('kerrthird001',third,third_url,post_data))
            # threads.append(t)

            # 判斷轉帳的 狀態
            if r.json()['status'] == True:
                print('帳號 %s 轉入 %s ,金額:1, 進行中' % (user, third))
                status = r.json()['status']
            else:
                status = r.json()['status']
                print('%s 轉帳失敗' % third)  # 列出錯誤訊息 ,

            statu_dict[third] = status  # 存放 各第三方的轉帳狀態
        # print(statu_dict)

        for third in statu_dict.keys():
            if statu_dict[third] == True:  # 判斷轉帳的狀態, 才去要 單號
                tran_result = Connection.thirdly_tran(Connection.my_con(evn=envs, third=third), tran_type=0,
                                                      third=third,
                                                      user=user)  # tran_type 0為轉轉入
                count = 0
                while tran_result[1] != '2' and count != 10:  # 確認轉帳狀態,  2為成功 ,最多做10次
                    tran_result = Connection.thirdly_tran(Connection.my_con(evn=envs, third=third),
                                                          tran_type=0,
                                                          third=third,
                                                          user=user)  #
                    sleep(1.5)
                    count += 1
                    if count == 15:
                        # print('轉帳狀態失敗')# 如果跑道9次  需確認
                        pass
                print('狀態成功. %s ,sn 單號: %s' % (third, tran_result[0]))
            else:
                pass

        self.test_PcThirdBalance()

    @func_time
    def test_PcTransferout(self):  # 第三方轉回
        '''第三方轉出'''
        statu_dict = {}  # 存放 第三方狀態
        header = {
            'User-Agent': userAgent,
            'Cookie': 'ANVOID=' + cookies_[user],
            'Content-Type': 'application/json; charset=UTF-8'
        }
        post_data = {"amount": 1}
        for third in third_list:
            url = '/%s/transferToFF' % third

            r = session.post(post_url + url, data=json.dumps(post_data), headers=header)
            if r.json()['status'] == True:
                print('帳號 %s, %s轉回4.0 ,金額:1, 進行中' % (user, third))
                status = r.json()['status']
            else:
                print(third + r.json()['errorMsg'])
                status = r.json()['status']
                # print('轉帳接口失敗')
            statu_dict[third] = status

        for third in statu_dict.keys():
            if statu_dict[third] == True:
                tran_result = Connection.thirdly_tran(Connection.my_con(evn=envs, third=third), tran_type=1,
                                                      third=third,
                                                      user=user)  # tran_type 1 是 轉出
                count = 0
                while tran_result[1] != '2' and count != 10:  # 確認轉帳狀態,  2為成功 ,最多做10次
                    tran_result = Connection.thirdly_tran(Connection.my_con(evn=envs, third=third),
                                                          tran_type=0,
                                                          third=third,
                                                          user=user)  #
                    sleep(1)
                    count += 1
                    if count == 9:
                        # print('轉帳狀態失敗')# 如果跑道9次  需確認
                        pass
                print('狀態成功. %s ,sn 單號: %s' % (third, tran_result[0]))
            else:
                pass
        self.test_PcThirdBalance()

    @staticmethod
    def admin_login(env_config):
        global admin_cookie, admin_url, header, cookies
        admin_cookie = {}
        header = {
            'User-Agent': Config.UserAgent.PC.value,
            'Content-Type': 'application/x-www-form-urlencoded'}
        admin_data = env_config.get_admin_data()
        admin_url = env_config.get_admin_url()
        session = requests.Session()
        r = session.post(admin_url + '/admin/login/login', data=admin_data, headers=header)
        cookies = r.cookies.get_dict()  # 獲得登入的cookies 字典
        admin_cookie['admin_cookie'] = cookies['ANVOAID']
        print(admin_cookie)
        print('登入後台 , 環境: %s' % admin_url)
        print(r.text)
        return cookies

    def test_redEnvelope(self):  # 紅包加壁,審核用
        user = self.user
        print('用戶: %s' % user)
        red_list = []  # 放交易訂單號id

        try:
            red_bal = self.select_red_bal(Connection.get_conn(envs), user)
            print('紅包餘額: %s' % (int(red_bal[0]) / 10000))
        except IndexError:
            print('紅包餘額為0')
        self.admin_login(env_config=self.envConfig)  # 登入後台
        data = {"receives": user, "blockType": "2", "lotteryType": "1", "lotteryCodes": "",
                "amount": "100", "note": "test"}
        header['Cookie'] = 'ANVOAID=' + admin_cookie['admin_cookie']  # 存放後台cookie
        header['Content-Type'] = 'application/json'
        r = session.post(admin_url + '/redAdmin/redEnvelopeApply',  # 後台加紅包街口
                         data=json.dumps(data), headers=header)
        if r.json()['status'] == 0:
            print('紅包加幣100')
        else:
            print('失敗')
        red_id = self.select_red_id(Connection.get_conn(envs), user)  # 查詢教地訂單號,回傳審核data
        # print(red_id)
        red_list.append('%s' % red_id[0])
        # print(red_list)
        data = {"ids": red_list, "status": 2}
        r = session.post(admin_url + '/redAdmin/redEnvelopeConfirm',  # 後台審核街口
                         data=json.dumps(data), headers=header)
        try:
            logger.info('r.json() : {}'.format(r.json()))
            if r.json()['status'] == 0:
                print('審核通過')
        except Exception as e:
            print(r.json()['errorMsg'])
            logger.error(e)
        red_bal = self.select_red_bal(Connection.get_conn(envs), user)
        print('紅包餘額: %s' % (int(red_bal[0]) / 10000))

    def tearDown(self) -> None:
        pass


class ApiTestYFT(unittest.TestCase):
    """
    YFT API測試
    """

    def __init__(self, case):
        super().__init__(case)
        pass
