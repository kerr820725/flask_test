import hashlib
import threading
import unittest
from time import sleep

import re
import redis
import json
import random
import requests
import time

from utils import Config, Logger
from utils.TestTool import trace_log
from utils.Config import LotteryData, func_time

logger = Logger.create_logger(r"\AutoTest", 'auto_test_app')
YFT_SIGN = None


class ApiTestApp(unittest.TestCase):
    u'APP接口測試'
    __slots__ = '_env_config', '_user', '_red_type', '_userAgent', '_header', '_conn_oracle', '_conn_mysql'

    def setUp(self):
        logger.info(f'ApiTestApp setUp : {self._testMethodName}')

    def __init__(self, case_, env_config, user, red_type, oracle, mysql):
        super().__init__(case_)
        # if not loggerApiTest:
        #     loggerApiTest = loggerApiTest.create_loggerApiTest(r"\ApiTestApp")
        self._env_config = env_config
        self._user = user
        self._red_type = red_type
        self._userAgent = Config.UserAgent.PC.value
        self._conn_oracle = oracle
        self._conn_mysql = mysql
        self._header = {
            'User-Agent': self._userAgent,
            'Content-Type': 'application/json'
        }
        logger.info('ApiTestApp __init__.')

    @func_time
    def test_AppLogin(self):
        u"APP登入測試"
        account_ = {self._user: '輸入的用戶名'}
        global TOKEN_, USERID_
        TOKEN_ = {}
        USERID_ = {}

        # 判斷用戶是dev或188,  uuid和loginpasssource為固定值
        global ENV_ID, ENV_IAPI  # envs : DB環境 用, env 環境 url ,request url 用, domin_url APP開戶 參數用

        ENV_IAPI = self._env_config.get_iapi()
        ENV_ID = self._env_config.get_env_id()
        uuid = self._env_config.get_uuid()
        login_pass_source = self._env_config.get_login_pass_source()
        joint_venture = self._env_config.get_joint_venture_by_domain()

        # 登入request的json
        for i in account_.keys():
            login_data = {
                "head": {
                    "sessionId": ''
                },
                "body": {
                    "param": {
                        "username": i + "|" + uuid,
                        "loginpassSource": login_pass_source,
                        "appCode": 1,
                        "uuid": uuid,
                        "loginIp": 2130706433,
                        "device": 2,
                        "app_id": 9,
                        "come_from": "3",
                        "appname": "1",
                        "jointVenture": joint_venture
                    }
                }
            }
            print("Joy188Test3 Start")
            # print(login_data)
            try:
                r = requests.post(ENV_IAPI + '/front/login', data=json.dumps(login_data), headers=self._header)
                logger.info(f'login request response = {r.json()}')
                token = r.json()['body']['result']['token']
                user_id = r.json()['body']['result']['userid']
                TOKEN_.setdefault(i, token)
                USERID_.setdefault(i, user_id)
                print(f'APP登入成功,登入帳號: {i}')
                print(f"Token: {token}")
                print(f"Userid: {user_id}")
            except ValueError as e:
                logger.error(trace_log(e))
                self.fail(u"登入失敗")
            # user_list.setdefault(userid,token)
        self.get_token(ENV_ID, self._user)

    def get_token(self, envs, user):
        redis_conn = self.get_rediskey(envs)
        user_keys = ''
        redis_keys = redis_conn.keys(f"USER_TOKEN_{re.findall(r'[0-9]+|[a-z]+', user)[0]}*")
        for index in redis_keys:
            if user in str(index):
                user_keys = (str(index).replace("'", '')[1:])
        if user_keys == '':
            raise Exception('token 取得失敗')

        user_dict = redis_conn.get(user_keys)
        timestap = str(user_dict).split('timeOut')[1].split('"token"')[0][2:-4]  #
        token_time = time.localtime(int(timestap))
        print(
            f'token到期時間: {token_time.tm_year}-{token_time.tm_mon}-{token_time.tm_mday} {token_time.tm_hour}:{token_time.tm_min}:{token_time.tm_sec}')

    def get_rediskey(self, envs):  # env參數 決定是哪個環境
        redis_dict = {'ip': ['10.13.22.152', '10.6.1.82']}  # 0:dev,1:188
        pool = redis.ConnectionPool(host=redis_dict['ip'][envs], port=6379)
        return redis.Redis(connection_pool=pool)

    @func_time
    def test_AppSubmit(self):
        u"APP投注"
        global USER

        USER = self._user  # 業面用戶登入
        t = time.strftime('%Y%m%d %H:%M:%S')
        print(f'投注帳號: {USER}, 現在時間: {t}')
        try:
            for i in LotteryData.lottery_dict.keys():
                if i in ['slmmc', 'sl115', 'btcctp']:
                    '''
                    data_ = {"head":{"sessionId":token_[user]},
                    "body":{"param":{"data":{"version":"1.0.30",
                    "channel":"android","gameType":"slmmc_","amount":2,
                    "balls":[{"id":0,"ball":"-,-,9,3,3",
                    "type":"housan.zhixuan.fushi","num":1,"multiple":1,"moneyunit":1,"amount":2}],
                    "isTrace":0,"traceWinStop":0,"traceStopValue":-1,"activityType":0,"awardMode":1,
                    "orders":[{"number":"/","issueCode":1,"multiple":1}],"loginIp":168627247},
                    "app_id":10,"come_from":"4","appname":"1"}}}
                    '''
                    pass
                else:
                    lottery_id = LotteryData.lottery_dict[i][1]

                    issue = self._conn_oracle.select_issue(lottery_id)  # 目前彩種的獎棋
                    # print(issue,issueName)
                    now = int(time.time() * 1000)  # 時間戳
                    ball_type_post = self.game_type(i)  # 玩法和內容,0為玩法名稱, 1為投注內容
                    methodid = ball_type_post[0].replace('.', '')  # ex: housan.zhuiam.fushi , 把.去掉

                    # 找出對應的玩法id
                    bet_type = self._conn_oracle.select_bet_type_code(lottery_id, methodid)

                    data_ = {"head":
                                 {"sessionId": TOKEN_[USER]},
                             "body": {"param": {"CGISESSID": TOKEN_[USER],  # 產生  kerr001的token
                                                "lotteryId": str(lottery_id), "chan_id": 1, "userid": 1373224,
                                                "money": 2 * MUL, "issue": issue['issue'][0],
                                                "issueName": issue['issueName'][0],
                                                "isFirstSubmit": 0,
                                                "list": [
                                                    {"methodid": bet_type[0], "codes": ball_type_post[1], "nums": 1,
                                                     "fileMode": 0, "mode": 1, "times": MUL, "money": 2 * MUL}],
                                                # times是倍數
                                                "traceIssues": "", "traceTimes": "", "traceIstrace": 0,
                                                "saleTime": now,
                                                "userIp": 168627247, "channelId": 402, "traceStop": 0}}}
                    session = requests.session()

                    r = session.post(self._env_config.get_post_url() + 'game/buy', data=json.dumps(data_),
                                     headers=self._header)

                    if r.json()['head']['status'] == 0:  # status0 為投注成功
                        print(f'{LotteryData.lottery_dict[i][0]} 投注成功')
                        print(bet_type[2])  # 投注完法 中文名稱
                        print(f"投注內容 : {ball_type_post[1]}")
                        print(f"投注金額 : {2 * MUL}, 投注倍數: {MUL}")  # mul 為game_type方法對甕倍數
                        # print(r.json())
                        orderid = (r.json()['body']['result']['orderId'])
                        order_code = self._conn_oracle.get_order_code_iapi(orderid)  # 找出對應ordercode
                        # print(f'orderid: {orderid}')
                        print(f'投注單號: {order_code[-1]}')
                        print('------------------------------')
                    else:
                        print(f'{LotteryData.lottery_dict[i][0]} 投注失敗')
                        pass
        except requests.exceptions.ConnectionError:
            print('please wait')
        except IndexError:
            pass

    def ball_type(self, test):  # 對應完法,產生對應最大倍數和 投注完法
        ball = []
        global MUL
        if test == 'wuxing':

            ball = [str(Config.random_mul(9)) for i in range(5)]  # 五星都是數值
            MUL = Config.random_mul(2)
        elif test == 'sixing':
            ball = ['-' if i == 0 else str(Config.random_mul(9)) for i in range(5)]  # 第一個為-
            MUL = Config.random_mul(22)
        elif test == 'housan':
            ball = ['-' if i in [0, 1] else str(Config.random_mul(9)) for i in range(5)]  # 第1和2為-
            MUL = Config.random_mul(222)
        elif test == 'qiansan':
            ball = ['-' if i in [3, 4] else str(Config.random_mul(9)) for i in range(5)]  # 第4和5為-
            MUL = Config.random_mul(222)
        elif test == 'zhongsan':
            ball = ['-' if i in [0, 4] else str(Config.random_mul(9)) for i in range(5)]  # 第2,3,4為-
            MUL = Config.random_mul(222)
        elif test == 'houer':
            ball = ['-' if i in [0, 1, 2] else str(Config.random_mul(9)) for i in range(5)]  # 第1,2,3為-
            MUL = Config.random_mul(2222)
        elif test == 'qianer':
            ball = ['-' if i in [2, 3, 4] else str(Config.random_mul(9)) for i in range(5)]  # 第3,4,5為-
            MUL = Config.random_mul(2222)
        elif test == 'yixing':  # 五個號碼,只有一個隨機數值
            ran = Config.random_mul(4)
            ball = ['-' if i != ran else str(Config.random_mul(9)) for i in range(5)]
            MUL = Config.random_mul(2222)
        else:
            MUL = Config.random_mul(1)
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
            0: [f"{group_}.zhixuan.fushi", lottery_ball],
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
            play_ = f'玩法名稱: {game_group[group_]}.{game_set["zhixuan"]}.{game_method["fushi"]}'

        elif lottery in LotteryData.lottery_3d:
            num = 1
            play_ = f'玩法名稱: {game_group["qianer"]}.{game_set["zhixuan"]}.{game_method["zhixuanfushi"]}'
        elif lottery in LotteryData.lottery_noRed:
            if lottery in ['p5', 'np3']:
                num = 9
                play_ = f'玩法名稱: {game_group["p3sanxing"]}.{game_set["zhixuan"]}.{game_method["fushi"]}'
            else:
                num = 1
                play_ = f'玩法名稱: {game_group["qianer"]}.{game_set["zhixuan"]}.{game_method["zhixuanfushi"]}'
        elif lottery in LotteryData.lottery_115:
            num = 2
            play_ = f'玩法名稱: {game_group["xuanqi"]}.{game_set["renxuanqizhongwu"]}.{game_method["fushi"]}'
        elif lottery in LotteryData.lottery_k3:
            num = 3
            play_ = f'玩法名稱: {game_group["sanbutonghao"]}.{game_set["biaozhun"]}'
        elif lottery in LotteryData.lottery_sb:
            num = 4
            play_ = f'玩法名稱: {game_group["santonghaotongxuan"]}'
        elif lottery in LotteryData.lottery_fun:
            num = 5
            play_ = f'玩法名稱: {game_group["guanya"]}.{game_set["zhixuan"]}.{game_method["fushi"]}'
        elif lottery == 'shssl':
            num = 6
            play_ = f'玩法名稱: {game_group["qianer"]}.{game_set["zuxuan"]}.{game_method["fushi"]}'
        elif lottery == 'ssq':
            num = 7
            play_ = f'玩法名稱: {game_group["biaozhuntouzhu"]}.{game_set["biaozhun"]}.{game_method["fushi"]}'
        elif lottery == 'lhc':
            num = 8
            play_ = f'玩法名稱: {game_group["zhengma"]}.{game_set["pingma"]}.{game_method["zhixuanliuma"]}'
        elif lottery == 'p5':
            num = 9
            play_ = f'玩法名稱: {game_group["p3sanxing"]}.{game_set["zhixuan"]}.{game_method["fushi"]}'
        elif lottery == 'bjkl8':
            num = 10
            play_ = f'玩法名稱: {game_group["renxuan"]}.{game_set["putongwanfa"]}.{game_method["renxuan7"]}'
        else:
            num = 11
            # play_ = u'玩法名稱: 沖天炮
        return test_dicts[num][0], test_dicts[num][1], play_

    def test_AppOpenLink(self):
        """APP開戶/註冊"""
        user = self._user
        if ENV_ID == 1:  # 188 環境
            data_ = {"head": {"sowner": "", "rowner": "", "msn": "", "msnsn": "", "userId": "", "userAccount": "",
                              "sessionId": TOKEN_[user]}, "body": {"pager": {"startNo": "1", "endNo": "99999"},
                                                                   "param": {"CGISESSID": TOKEN_[user], "type": 1,
                                                                             "days": -1, "infos": [
                                                                           {"lotteryId": "77101",
                                                                            "lotterySeriesCode": 10,
                                                                            "lotterySeriesName": "\\u771f\\u4eba\\u5f69\\u7968",
                                                                            "awardGroupId": 77101,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99101",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 12,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99103",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 19,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99104",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 36,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99105",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 13,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99105",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 5,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41700",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99105",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 16,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41500",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99106",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 33,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99107",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 15,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99107",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 8,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41700",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99107",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 18,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41500",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99108",
                                                                                             "lotterySeriesCode": 2,
                                                                                             "lotterySeriesName": "3D\\u7cfb",
                                                                                             "awardGroupId": 101,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41700",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99109",
                                                                            "lotterySeriesCode": 2,
                                                                            "lotterySeriesName": "3D\\u7cfb",
                                                                            "awardGroupId": 102,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41700",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99111",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 41,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99112",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 56,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99113",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 205,
                                                                                             "awardName": "2000\\u5956\\u91d1\\u7ec4",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99114",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 208,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99115",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 219,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41000",
                                                                                             "directLimitRet": 4300,
                                                                                             "threeLimitRet": 4300,
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99116",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 231,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99117",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 248,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99118",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 249,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99119",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 253,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99120",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 254,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99121",
                                                                                             "lotterySeriesCode": 1,
                                                                                             "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 255,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99122",
                                                                            "lotterySeriesCode": 1,
                                                                            "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                                                                            "awardGroupId": 256,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99123",
                                                                                             "lotterySeriesCode": 2,
                                                                                             "lotterySeriesName": "3D\\u7cfb",
                                                                                             "awardGroupId": 258,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directLimitRet": 450,
                                                                                             "threeLimitRet": 450,
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99124",
                                                                            "lotterySeriesCode": 2,
                                                                            "lotterySeriesName": "3D\\u7cfb",
                                                                            "awardGroupId": 259,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directLimitRet": 450, "threeLimitRet": 450,
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99201",
                                                                                             "lotterySeriesCode": 4,
                                                                                             "lotterySeriesName": "\\u57fa\\u8bfa\\u7cfb",
                                                                                             "awardGroupId": 32,
                                                                                             "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99202",
                                                                            "lotterySeriesCode": 4,
                                                                            "lotterySeriesName": "\\u57fa\\u8bfa\\u7cfb",
                                                                            "awardGroupId": 206,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directLimitRet": 950, "directRet": 0,
                                                                            "threeoneRet": 0, "superRet": 0},
                                                                           {"lotteryId": "99203",
                                                                            "lotterySeriesCode": 4,
                                                                            "lotterySeriesName": "\\u57fa\\u8bfa\\u7cfb",
                                                                            "awardGroupId": 238,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41000",
                                                                            "directLimitRet": 5000, "directRet": 0,
                                                                            "threeoneRet": 0, "superRet": 0},
                                                                           {"lotteryId": "99301",
                                                                            "lotterySeriesCode": 3,
                                                                            "lotterySeriesName": "11\\u90095\\u7cfb",
                                                                            "awardGroupId": 24,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41782",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99302",
                                                                                             "lotterySeriesCode": 3,
                                                                                             "lotterySeriesName": "11\\u90095\\u7cfb",
                                                                                             "awardGroupId": 27,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41782",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99303",
                                                                            "lotterySeriesCode": 3,
                                                                            "lotterySeriesName": "11\\u90095\\u7cfb",
                                                                            "awardGroupId": 29,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41782",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99306",
                                                                                             "lotterySeriesCode": 3,
                                                                                             "lotterySeriesName": "11\\u90095\\u7cfb",
                                                                                             "awardGroupId": 192,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41782",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99401",
                                                                            "lotterySeriesCode": 5,
                                                                            "lotterySeriesName": "\\u53cc\\u8272\\u7403\\u7cfb",
                                                                            "awardGroupId": 107,
                                                                            "awardName": "\\u53cc\\u8272\\u7403\\u5956\\u91d1\\u7ec4",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99501",
                                                                                             "lotterySeriesCode": 6,
                                                                                             "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 188,
                                                                                             "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99502",
                                                                            "lotterySeriesCode": 6,
                                                                            "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb",
                                                                            "awardGroupId": 190,
                                                                            "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99601",
                                                                                             "lotterySeriesCode": 7,
                                                                                             "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 189,
                                                                                             "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99602",
                                                                            "lotterySeriesCode": 7,
                                                                            "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb",
                                                                            "awardGroupId": 203,
                                                                            "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99604",
                                                                                             "lotterySeriesCode": 7,
                                                                                             "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 213,
                                                                                             "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0},
                                                                           {"lotteryId": "99605",
                                                                            "lotterySeriesCode": 7,
                                                                            "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb",
                                                                            "awardGroupId": 207,
                                                                            "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99701",
                                                                                             "lotterySeriesCode": 9,
                                                                                             "lotterySeriesName": "\\u516d\\u5408\\u7cfb",
                                                                                             "awardGroupId": 202,
                                                                                             "awardName": "\\u516d\\u5408\\u5f69\\u5956\\u91d1\\u7ec4",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0,
                                                                                             "lhcYear": 0,
                                                                                             "lhcColor": 0,
                                                                                             "lhcFlatcode": 0,
                                                                                             "lhcHalfwave": 0,
                                                                                             "lhcOneyear": 0,
                                                                                             "lhcNotin": 0,
                                                                                             "lhcContinuein23": 0,
                                                                                             "lhcContinuein4": 0,
                                                                                             "lhcContinuein5": 0,
                                                                                             "lhcContinuenotin23": 0,
                                                                                             "lhcContinuenotin4": 0,
                                                                                             "lhcContinuenotin5": 0,
                                                                                             "lhcContinuecode": 0},
                                                                           {"lotteryId": "99801",
                                                                            "lotterySeriesCode": 2,
                                                                            "lotterySeriesName": "3D\\u7cfb",
                                                                            "awardGroupId": 223,
                                                                            "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                            "directLimitRet": 450, "threeLimitRet": 450,
                                                                            "directRet": 0, "threeoneRet": 0,
                                                                            "superRet": 0}, {"lotteryId": "99901",
                                                                                             "lotterySeriesCode": 11,
                                                                                             "lotterySeriesName": "\\u9ad8\\u9891\\u5f69\\u7cfb",
                                                                                             "awardGroupId": 243,
                                                                                             "awardName": "\\u5956\\u91d1\\u7ec41800",
                                                                                             "directRet": 0,
                                                                                             "threeoneRet": 0,
                                                                                             "superRet": 0}],
                                                                             "memo": "", "setUp": 1, "needContact": "N",
                                                                             "authenCellphone": "N",
                                                                             "showRegisterBtn": "Y", "app_id": "9",
                                                                             "come_from": "3", "appname": "1",
                                                                             "domain": "https:\\/\\/www2.joy188.com"}}}
        else:  # dev
            data_ = {"head": {"sessionId": TOKEN_[user]}, "body": {
                "param": {"CGISESSID": TOKEN_[user], "type": 1, "days": -1, "infos": [
                    {"lotteryId": "77101", "lotteryName": "\\u4e50\\u5229\\u771f\\u4eba\\u5f69",
                     "lotterySeriesCode": 10, "lotterySeriesName": "\\u771f\\u4eba\\u5f69\\u7968",
                     "awardGroupId": 77101, "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 480},
                    {"lotteryId": "99101", "lotteryName": "\\u6b22\\u4e50\\u751f\\u8096", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 12,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99103", "lotteryName": "\\u65b0\\u7586\\u65f6\\u65f6\\u5f69", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 19,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99104", "lotteryName": "\\u5929\\u6d25\\u65f6\\u65f6\\u5f69", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 36,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99105", "lotteryName": "\\u9ed1\\u9f99\\u6c5f\\u65f6\\u65f6\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 13,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99106", "lotteryName": "\\u51e4\\u51f0\\u4e50\\u5229\\u65f6\\u65f6\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 33,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99107", "lotteryName": "\\u4e0a\\u6d77\\u65f6\\u65f6\\u4e50", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 15,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99108", "lotteryName": "3D", "lotterySeriesCode": 2,
                     "lotterySeriesName": "3D\\u7cfb", "awardGroupId": 101, "awardName": "\\u5956\\u91d1\\u7ec41700",
                     "directLimitRet": 1380, "threeLimitRet": 980},
                    {"lotteryId": "99109", "lotteryName": "P5", "lotterySeriesCode": 2,
                     "lotterySeriesName": "3D\\u7cfb", "awardGroupId": 102, "awardName": "\\u5956\\u91d1\\u7ec41700",
                     "directLimitRet": 1380, "threeLimitRet": 980},
                    {"lotteryId": "99111", "lotteryName": "\\u51e4\\u51f0\\u5409\\u5229\\u5206\\u5206\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 41,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99112", "lotteryName": "\\u51e4\\u51f0\\u987a\\u5229\\u79d2\\u79d2\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 56,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99113", "lotteryName": "\\u8d85\\u7ea72000\\u79d2\\u79d2\\u5f69(APP\\u7248)",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb",
                     "awardGroupId": 11416083, "awardName": "2000\\u5956\\u91d1\\u7ec4", "superLimitRet": 80},
                    {"lotteryId": "99114", "lotteryName": "\\u817e\\u8baf\\u5206\\u5206\\u5f69", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 208,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99115", "lotteryName": "\\u51e4\\u51f0\\u6bd4\\u7279\\u5e01\\u5206\\u5206\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 214,
                     "awardName": "\\u5956\\u91d1\\u7ec41000", "directLimitRet": 4780, "threeLimitRet": 4780},
                    {"lotteryId": "99116", "lotteryName": "\\u51e4\\u51f0\\u5409\\u5229\\u65f6\\u65f6\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 228,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99117", "lotteryName": "\\u51e4\\u51f0\\u91cd\\u5e86\\u5168\\u7403\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 263,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99118", "lotteryName": "\\u51e4\\u51f0\\u65b0\\u7586\\u5168\\u7403\\u5f69",
                     "lotterySeriesCode": 1, "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 264,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99119", "lotteryName": "\\u6cb3\\u5185\\u5206\\u5206\\u5f69", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 268,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99120", "lotteryName": "\\u6cb3\\u5185\\u4e94\\u5206\\u5f69", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 273,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99121", "lotteryName": "360\\u5206\\u5206\\u5f69", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 274,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99122", "lotteryName": "360\\u4e94\\u5206\\u5f69", "lotterySeriesCode": 1,
                     "lotterySeriesName": "\\u65f6\\u65f6\\u5f69\\u7cfb", "awardGroupId": 275,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99123", "lotteryName": "\\u8d8a\\u5357\\u798f\\u5f69", "lotterySeriesCode": 2,
                     "lotterySeriesName": "3D\\u7cfb", "awardGroupId": 278, "awardName": "\\u5956\\u91d1\\u7ec41800",
                     "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99124", "lotteryName": "\\u8d8a\\u53573D\\u798f\\u5f69", "lotterySeriesCode": 2,
                     "lotterySeriesName": "3D\\u7cfb", "awardGroupId": 279, "awardName": "\\u5956\\u91d1\\u7ec41800",
                     "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99201", "lotteryName": "\\u5317\\u4eac\\u5feb\\u4e508", "lotterySeriesCode": 4,
                     "lotterySeriesName": "\\u57fa\\u8bfa\\u7cfb", "awardGroupId": 32,
                     "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4", "directLimitRet": 1980, "threeLimitRet": 1380},
                    {"lotteryId": "99202", "lotteryName": "PK10", "lotterySeriesCode": 4,
                     "lotterySeriesName": "\\u57fa\\u8bfa\\u7cfb", "awardGroupId": 206,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 980},
                    {"lotteryId": "99203", "lotteryName": "\\u98de\\u8247", "lotterySeriesCode": 4,
                     "lotterySeriesName": "\\u57fa\\u8bfa\\u7cfb", "awardGroupId": 233,
                     "awardName": "\\u5956\\u91d1\\u7ec41000", "directLimitRet": 4780},
                    {"lotteryId": "99301", "lotteryName": "\\u5c71\\u4e1c11\\u90095", "lotterySeriesCode": 3,
                     "lotterySeriesName": "11\\u90095\\u7cfb", "awardGroupId": 24,
                     "awardName": "\\u5956\\u91d1\\u7ec41782", "directLimitRet": 980, "threeLimitRet": 980},
                    {"lotteryId": "99302", "lotteryName": "\\u6c5f\\u897f11\\u90095", "lotterySeriesCode": 3,
                     "lotterySeriesName": "11\\u90095\\u7cfb", "awardGroupId": 27,
                     "awardName": "\\u5956\\u91d1\\u7ec41782", "directLimitRet": 980, "threeLimitRet": 980},
                    {"lotteryId": "99303", "lotteryName": "\\u5e7f\\u4e1c11\\u90095", "lotterySeriesCode": 3,
                     "lotterySeriesName": "11\\u90095\\u7cfb", "awardGroupId": 29,
                     "awardName": "\\u5956\\u91d1\\u7ec41782", "directLimitRet": 980, "threeLimitRet": 980},
                    {"lotteryId": "99306", "lotteryName": "\\u51e4\\u51f0\\u987a\\u522911\\u90095",
                     "lotterySeriesCode": 3, "lotterySeriesName": "11\\u90095\\u7cfb", "awardGroupId": 192,
                     "awardName": "\\u5956\\u91d1\\u7ec41782", "directLimitRet": 980, "threeLimitRet": 980},
                    {"lotteryId": "99401", "lotteryName": "\\u53cc\\u8272\\u7403", "lotterySeriesCode": 5,
                     "lotterySeriesName": "\\u53cc\\u8272\\u7403\\u7cfb", "awardGroupId": 107,
                     "awardName": "\\u53cc\\u8272\\u7403\\u5956\\u91d1\\u7ec4", "directLimitRet": 1480,
                     "threeLimitRet": 1480},
                    {"lotteryId": "99501", "lotteryName": "\\u6c5f\\u82cf\\u5feb\\u4e09", "lotterySeriesCode": 6,
                     "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb", "awardGroupId": 188,
                     "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4", "directLimitRet": 1280},
                    {"lotteryId": "99502", "lotteryName": "\\u5b89\\u5fbd\\u5feb\\u4e09", "lotterySeriesCode": 6,
                     "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb", "awardGroupId": 190,
                     "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4", "directLimitRet": 1280},
                    {"lotteryId": "99601", "lotteryName": "\\u6c5f\\u82cf\\u9ab0\\u5b9d", "lotterySeriesCode": 7,
                     "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb", "awardGroupId": 189,
                     "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4", "directLimitRet": 880}, {"lotteryId": "99602",
                                                                                                  "lotteryName": "\\u51e4\\u51f0\\u5409\\u5229\\u9ab0\\u5b9d(\\u5a31\\u4e50\\u5385)",
                                                                                                  "lotterySeriesCode": 7,
                                                                                                  "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb",
                                                                                                  "awardGroupId": 203,
                                                                                                  "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4",
                                                                                                  "directLimitRet": 880},
                    {"lotteryId": "99604", "lotteryName": "\\u5b89\\u5fbd\\u9ab0\\u5b9d", "lotterySeriesCode": 7,
                     "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb", "awardGroupId": 11416087,
                     "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4", "directLimitRet": 880},
                    {"lotteryId": "99605", "lotteryName": "\\u51e4\\u51f0\\u987a\\u5229\\u9ab0\\u5b9d",
                     "lotterySeriesCode": 7, "lotterySeriesName": "\\u5feb\\u4e50\\u5f69\\u7cfb", "awardGroupId": 207,
                     "awardName": "\\u6df7\\u5408\\u5956\\u91d1\\u7ec4", "directLimitRet": 880, "threeLimitRet": 130},
                    {"lotteryId": "99701", "lotteryName": "\\u516d\\u5408\\u5f69", "lotterySeriesCode": 9,
                     "lotterySeriesName": "\\u516d\\u5408\\u7cfb", "awardGroupId": 202,
                     "awardName": "\\u516d\\u5408\\u5f69\\u5956\\u91d1\\u7ec4", "directLimitRet": 1390,
                     "lhcYearLimit": 280, "lhcColorLimit": 280, "lhcFlatcodeLimit": 380, "lhcHalfwaveLimit": 280,
                     "lhcOneyearLimit": 180, "lhcNotinLimit": 280, "lhcContinuein23Limit": 280,
                     "lhcContinuein4Limit": 480, "lhcContinuein5Limit": 480, "lhcContinuenotin23Limit": 280,
                     "lhcContinuenotin4Limit": 480, "lhcContinuenotin5Limit": 480, "lhcContinuecodeLimit": 480},
                    {"lotteryId": "99801", "lotteryName": "\\u51e4\\u51f0\\u5409\\u52293D", "lotterySeriesCode": 2,
                     "lotterySeriesName": "3D\\u7cfb", "awardGroupId": 223, "awardName": "\\u5956\\u91d1\\u7ec41800",
                     "directLimitRet": 880, "threeLimitRet": 980},
                    {"lotteryId": "99901", "lotteryName": "\\u5feb\\u5f00", "lotterySeriesCode": 11,
                     "lotterySeriesName": "\\u9ad8\\u9891\\u5f69\\u7cfb", "awardGroupId": 238,
                     "awardName": "\\u5956\\u91d1\\u7ec41800", "directLimitRet": 980}], "memo": "", "setUp": 1,
                          "needContact": "N", "authenCellphone": "N", "showRegisterBtn": "Y"}}}
        logger.info(f"link = {ENV_IAPI + '/information/doRetSetting'}")
        r = requests.post(ENV_IAPI + '/information/doRetSetting', data=json.dumps(data_),
                          headers=self._header)  # 儲存連結反點,生成連結
        print(r.content)
        logger.info(r.content)
        if r.json()['head']['status'] == 0:
            print('開戶連結創立成功')
            data_ = {"head": {"sowner": "", "rowner": "", "msn": "", "msnsn": "", "userId": "", "userAccount": "",
                              "sessionId": TOKEN_[user]},
                     "body": {"param": {"CGISESSID": TOKEN_[user], "app_id": "10", "come_from": "4",
                                        "appname": "1"}, "pager": {"startNo": "", "endNo": ""}}}

            r = requests.post(ENV_IAPI + '/information/openLinkList', data=json.dumps(data_),
                              headers=self._header)  # 找出開戶連結后的註冊id,回傳註冊
            # print(r.json())
            result = r.json()['body']['result']['list'][0]
            global REGCODE, TOKEN, EXP, PID
            REGCODE = result['regCode']  # 回傳開戶 的 id
            TOKEN = result['urlstring'].split('token=')[1]  # 回傳 開戶 的token
            # print(token)
            EXP = result['urlstring'].split('exp=')[1].split('&')[0]
            PID = result['urlstring'].split('pid=')[1].split('&')[0]
            print(f'{user} 的 開戶連結')
            print(f"註冊連結: {result['urlstring']}, \n註冊碼: {result['regCode']}, 建置於: {result['start']}")
        else:
            self.fail('創立失敗')
        user_random = random.randint(1, 100000)  # 隨機生成 頁面輸入 用戶名 + 隨機數 的下級
        new_user = self._user + str(user_random)
        data_ = {"head": {"sowner": "", "rowner": "", "msn": "", "msnsn": "", "userId": "", "userAccount": ""},
                 # 開戶data
                 "body": {
                     "param": {"token": TOKEN, "accountName": new_user, "password": "3bf6add0828ee17c4603563954473c1e",
                               "cellphone": "", "qqAccount": "", "wechat": "", "id": int(REGCODE), "exp": EXP,
                               "pid": int(PID), "qq": '',
                               "ip": "192.168.2.18", "app_id": "10", "come_from": "4", "appname": "1"},
                     "pager": {"startNo": "", "endNo": ""}}}
        if self._env_config in ['dev02', 'joy188']:  # 一般 4.0  data 不用帶 joint_venture
            pass
        elif self._env_config in ['fh82dev02', 'teny2020dev02', 'joy188.teny2020', 'joy188.195353']:  # 合營版
            data_['body']['param']['jointVenture'] = 1
        else:  # 歡樂棋牌
            data_['body']['param']['jointVenture'] = 2

        r = requests.post(ENV_IAPI + '/user/register', data=json.dumps(data_), headers=self._header)
        if r.json()['head']['status'] == 0:
            print(f'{new_user} 註冊成功')
        else:
            print('註冊失敗')

    def amount_data(self, _user):
        data = {"head": {"sowner": "", "rowner": "", "msn": "", "msnsn": "", "userId": "", "userAccount": "",
                         "sessionId": TOKEN_[_user]},
                "body": {"param": {"amount": 10, "CGISESSID": TOKEN_[_user], "app_id": "9",
                                   "come_from": "3", "appname": "1"}, "pager": {"startNo": "", "endNo": ""}}}
        return data

    def balance_data(self, _user):
        data = {"head": {"sowner": "", "rowner": "", "msn": "", "msnsn": "", "userId": "",
                         "userAccount": "", "sessionId": TOKEN_[_user]}, "body": {"param": {"CGISESSID": TOKEN_[_user],
                                                                                            "loginIp": "61.220.138.45",
                                                                                            "app_id": "9",
                                                                                            "come_from": "3",
                                                                                            "appname": "1"},
                                                                                  "pager": {"startNo": "",
                                                                                            "endNo": ""}}}
        return data

    def APP_SessionPost(self, third: str, url: str, post_data):  # 共用 session post方式 (Pc)
        self._header = {
            'User-Agent': self._userAgent,
            'Content-Type': 'application/json; charset=UTF-8',
        }
        try:
            session = requests.Session()
            response = session.post(ENV_IAPI + f'/{third}/{url}', headers=self._header, data=json.dumps(post_data))

            if 'balance' in url:
                balance = response.json()['body']['result']['balance']
                print(f'{third} 的餘額為: {balance}')
            elif 'getBalance' in url:
                balance = response.json()['body']['result']['balance']
                print(f'4.0餘額: {balance}')

        except requests.exceptions.ConnectionError:
            self.fail(u'連線有問題,請稍等')

    @func_time
    def test_AppBalance(self):
        """APP 4.0/第三方餘額"""
        threads = []
        user = self._user
        data_ = self.balance_data(user)
        third_list = ['gns', 'sb', 'im', 'ky', 'lc', 'city']
        print(f'帳號: {user}')
        for third in third_list:
            if third == 'shaba':
                third = 'sb'
            # r = requests.post(env + f'/{third}/balance', data=json.dumps(data_), headers=self.header)
            t = threading.Thread(target=self.APP_SessionPost, args=(third, 'balance', data_))
            threads.append(t)
        t = threading.Thread(target=self.APP_SessionPost, args=('information', 'getBalance', data_))
        threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
            # print(r.json())
            # balance = r.json()['body']['result']['balance']
            # print(f'{third} 的餘額為: {balance}')
        '''
        r = requests.post(env+'/information/getBalance',data=json.dumps(data_),headers=self.header)
        balance =  r.json()['body']['result']['balance']
        print('4.0餘額: %s'%balance)
        '''

    @func_time
    def test_ApptransferIn(self):
        """APP轉入"""
        data_ = self.amount_data(self._user)
        print(f'帳號: {self._user}')
        third_list = ['gns', 'sb', 'im', 'ky', 'lc', 'city']
        third_failed = {}
        for third in third_list:
            logger.info('First.  for third in third_list:')
            tran_url = 'Thirdly'  # gns規則不同
            if third == 'gns':
                tran_url = 'Gns'
            response = requests.post(ENV_IAPI + f'/{third}/transferTo{tran_url}', data=json.dumps(data_),
                                     headers=self._header)
            logger.info('test_ApptransferIn third = {third}, response = {response.content}')
            status = response.json()['body']['result']['status']
            if status == 'Y':
                print(f'轉入{third}金額 10')
            else:
                third_failed[f'{third} 轉入失敗'] = response.json()  # 若轉入失敗計入錯誤

        for third in third_list:
            logger.info(f'{third} 轉入開始')
            if third == 'sb':
                third = 'shaba'
            tran_result = ['', '']
            count = 0
            logger.info(f'tran_result : {tran_result}')
            while tran_result[1] != '2' and count < 16:  # 確認轉帳狀態,  2為成功 ,最多做10次
                tran_result = self._conn_mysql.thirdly_tran(
                    tran_type=0,
                    third=third,
                    user=self._user)
                logger.info(f'tran_result : {tran_result}')
                sleep(2)
                count += 1
                if tran_result[1] == '2':
                    logger.info(f'轉帳狀態成功 : [{third}] = {tran_result}')
                    print(f'{third}: 轉帳成功 ,sn 單號: {tran_result[0]}')
                if count == 15:
                    # raise Exception(f'轉帳狀態失敗 : {third}')  # 如果跑道9次  需確認
                    # print(f'{third}: 轉帳失敗, sn 單號: {tran_result[0]}')  # 如果跑道9次  需確認  # 驗證超出次數
                    logger.error(f'轉帳狀態失敗 : [{third}] = {tran_result}')
                    third_failed[f'{third} 驗證逾時'] = tran_result  # 若有多次嘗試仍未成功計入錯誤

        if len(third_failed.items()) > 0:  # 若有三方轉帳錯誤紀錄
            for key, value in third_failed.items():
                print(f'三方: {key}, 錯誤: {value}')
            self.fail('三方轉出有誤')

        self.test_AppBalance()

    @func_time
    def test_ApptransferOut(self):
        """APP轉出"""
        data_ = self.amount_data(self._user)
        print(f'帳號: {self._user}')
        third_list = ['gns', 'sb', 'im', 'ky', 'lc', 'city']
        third_failed = {}
        for third in third_list:  # PC 沙巴 是 shaba , iapi 是 sb
            response = requests.post(ENV_IAPI + f'/{third}/transferToFF', data=json.dumps(data_), headers=self._header)
            logger.info(f'test_ApptransferOut : third = {third}, response = {response.content}')
            status = response.json()['body']['result']['status']
            if status == 'Y':
                # print(f'轉出接口回傳:{response.json()}')
                print(f'{third} 轉出金額 10')
            else:
                third_failed[f'{third} 轉出'] = response.json()

        for third in third_list:
            logger.info(f'{third} 轉出開始')
            if third == 'sb':
                third = 'shaba'
            tran_result = ["", -1]
            count = 0
            while tran_result[1] != '2' and count < 16:  # 確認轉帳狀態,  2為成功 ,最多做10次
                tran_result = self._conn_mysql.thirdly_tran(tran_type=1, third=third, user=self._user)
                logger.info(f'tran_result : {tran_result}')
                sleep(2)
                count += 1
                if tran_result[1] == '2':
                    logger.info(f'轉帳狀態成功 : [{third}] = {tran_result}')
                    print(f'{third}: 轉帳成功, sn 單號: {tran_result[0]}')
                if count == 15:
                    # raise Exception(f'轉帳狀態失敗 : {third}')  # 驗證超出次數
                    # print(f'{third}: 轉帳失敗, sn 單號: {tran_result[0]}')  # 如果跑道9次  需確認  # 驗證超出次數
                    logger.error(f'轉帳狀態失敗 : [{third}] = {tran_result}')
                    third_failed[f'{third} 驗證逾時'] = tran_result

            if len(third_failed.items()) > 0:
                for key, value in third_failed.items():
                    print(f'三方: {key}, 錯誤: {value}')
                self.fail('三方轉出有誤')
        self.test_AppBalance()

    def tearDown(self) -> None:
        pass


class ApiTestAPP_YFT(unittest.TestCase):
    """
    YFT APP API測試
    """
    __slots__ = '_api_url', '_iapi_default', '_session', '_env_config', '_user', '_money_unit',\
                '_award_mode', '_conn_postgre', '_header'

    def setUp(self):
        from utils.requestContent_YFT import _iapi_default
        self._iapi_default = json.loads(_iapi_default)

        global YFT_SIGN
        logger.info(f'ApiTestPC setUp : {self._testMethodName}')
        if YFT_SIGN is None:
            YFT_SIGN = self.login()

    def __init__(self, case, env_config, user, conn, money_unit=1, award_mode=0):
        super().__init__(case)
        logger.info(
            f'ApiTestAPP_YFT __init__ : _env={env_config}, _user={user}, _money_unit={money_unit}, _award_mode={award_mode}')
        self._api_url = '/app/call'
        self._env_config = env_config
        self._user = user
        self._money_unit = money_unit
        self._award_mode = award_mode
        self._conn_postgre = conn
        self._header = {'User-Agent': Config.UserAgent.PC.value,
                        'Content-Type': 'application/json'}
        self._session = requests.Session()

    def login(self):
        call_type = 'login'

        md = hashlib.md5()
        md.update(self._env_config.get_password().encode('utf-8'))
        data = self._iapi_default
        data['callType'] = call_type
        data[
            "content"] = f'{{"passwd":"{md.hexdigest()}","account":"{self._user}","uuid":"DF4D21DD8B87A5A84F5EE57122CCB06F6D14CFE6"}}'
        response = self._session.post(url=self._env_config.get_post_url() + self._api_url, data=json.dumps(data),
                                      headers=self._header)
        response_json = json.loads(response.content)
        logger.debug(f'login_url = {self._env_config.get_post_url() + self._api_url}')
        logger.debug(f'Login response = {response.content}')
        logger.debug(f'Cookies = {response_json["content"]["sign"]}')
        if response_json["content"]["sign"]:
            return response_json["content"]["sign"]  # setCookie into header
        else:
            self.fail('登入失敗.')

    """時時彩投注"""

    def test_bet_qqffc(self, stop_on_win=True):
        """
        QQ分分彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['qqffc', 'QQ分分彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_hjcqssc(self, stop_on_win=True):
        """
        懷舊重慶時時彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['hjcqssc', '懷舊重慶時時彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_ynffc(self, stop_on_win=True):
        """
        印尼分分彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['ynffc', '印尼分分彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_tcffc(self, stop_on_win=True):
        """
        騰訊分分彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['tcffc', '騰訊分分彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_se15fc(self, stop_on_win=True):
        """
        首爾1.5分彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['se15fc', '首爾1.5分彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_yn2fc(self, stop_on_win=True):
        """
        印尼2分彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['yn2fc', '印尼2分彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_xjssc(self, stop_on_win=True):
        """
        新疆時時彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['xjssc', '新疆時時彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_tjssc(self, stop_on_win=True):
        """
        天津時時彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['tjssc', '天津時時彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_tcdffc(self, stop_on_win=True):
        """
        騰訊兩分彩投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['tcdffc', '騰訊兩分彩']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_cqssc(self, stop_on_win=True):
        """
        重慶時時彩生肖
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """

        game_name = ['cqssc', '重慶時時彩生肖']
        self.bet_trace(game_name, stop_on_win)

    """快艇／賽車投注"""

    def test_bet_fhxyft(self, stop_on_win=True):
        """
        幸運飛艇投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['fhxyft', '鳳凰幸運飛艇']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_bjpk10(self, stop_on_win=True):
        """
        PK10投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['bjpk10', '北京PK10']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_djpk10(self, stop_on_win=True):
        """
        東京賽車投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['djpk10', '東京賽車']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_xyftpk10(self, stop_on_win=True):
        """
        皇家幸運飛艇投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['xyftpk10', '皇家幸運飛艇']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_metftpk10(self, stop_on_win=True):
        """
        馬爾他飛艇投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['metftpk10', '馬爾他飛艇']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_xnpk10(self, stop_on_win=True):
        """
        悉尼PK10投注
        牛牛不可高獎金，另外投注。
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['xnpk10', '悉尼PK10']
        self.bet_trace(game_name, stop_on_win)

    """快三投注"""

    def test_bet_ahk3(self, stop_on_win=True):
        """
        安徽快三投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['ahk3', '安徽快三']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_hbk3(self, stop_on_win=True):
        """
        湖北快三投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['hbk3', '湖北快三']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_jsk3(self, stop_on_win=True):
        """
        江蘇快三投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['jsk3', '江蘇快三']
        self.bet_trace(game_name, stop_on_win)

    """11選5投注"""

    def test_bet_sd11x5(self, stop_on_win=True):
        """
        山東11選5投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['sd11x5', '山東11選5']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_jx11x5(self, stop_on_win=True):
        """
        江西11選5投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['jx11x5', '江西11選5']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_sh11x5(self, stop_on_win=True):
        """
        上海11選5投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['sh11x5', '上海11選5']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_js11x5(self, stop_on_win=True):
        """
        江蘇11選5投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['sd11x5', '江蘇11選5']
        self.bet_trace(game_name, stop_on_win)

    def test_bet_gd11x5(self, stop_on_win=True):
        """
        廣東11選5投注
        :param stop_on_win: 追號與否
        :return: None
        """
        game_name = ['gd11x5', '廣東11選5']
        self.bet_trace(game_name, stop_on_win)

    def get_lottery_info(self, lottery_name):
        """
        取得彩種資訊（獎期等）
        :param lottery_name: 彩種英文ID
        :return: 返還獎期資訊內容
        """
        call_type = 'get_bet_issue_info'
        data = self._iapi_default
        data['callType'] = call_type
        if YFT_SIGN is None:
            raise Exception('Sign is None.')
        data['sign'] = YFT_SIGN
        data['content'] = {"lotteryType": lottery_name}
        logger.debug(f'data = {json.dumps(data)}')
        response = self._session.post(url=self._env_config.get_post_url() + self._api_url, data=json.dumps(data),
                                      headers=self._header)
        logger.debug(f'lottery_info response = {response.content}')
        return response.json()['content']

    def bet_yft(self, lottery_name, games, is_trace=False, stop_on_win=True):
        """
        YFT發起投注
        :param games: 投注玩法清單，可取自BetContent_yft.py
        :param lottery_name: 彩種英文ID
        :param is_trace: 追號與否，影響投注內容需替換的參數
        :param stop_on_win: 追中即停
        :return: 投注結果
        """
        call_type = 'bet_v2'
        lottery_info = self.get_lottery_info(lottery_name)

        import json
        default = self._iapi_default
        from utils.requestContent_YFT import game_dict
        totalAmount = 0
        schemeList = []
        for game in games:
            if game_dict.get(game) and game not in ('pt333bt02', 'pt137bt02'):  # 排除牛牛
                schemeList.append(game_dict.get(game)[0])
                totalAmount += game_dict.get(game)[1]
        default['content']['currIssueNo'] = lottery_info["noopsycheIssueList"][0]
        default['content']['lotteryType'] = lottery_name
        default['sign'] = YFT_SIGN
        default['content']['schemeList'] = schemeList
        default['content']['lotteryType'] = lottery_name
        default['content']['issueList'] = [1]
        default['callType'] = call_type

        if is_trace:
            default['content']['issueList'] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            totalAmount *= 10
            if stop_on_win:
                default['content']['stopOnWon'] = 'yes'
        if self._money_unit == '0.1':
            totalAmount *= 0.1
        elif self._money_unit == '0.01':
            totalAmount *= 0.01

        default['content']['totalAmount'] = totalAmount

        data = json.dumps(default)

        logger.debug(f"self.money_unit == '0.1' = {self._money_unit == '0.1'}\n"
                     f"self.money_unit == '0.01' = {self._money_unit == '0.01'}\n"
                     f"self.award_mode == '2' = {self._award_mode == '2'}")
        if self._money_unit == '0.1':
            data.replace('"potType": "Y"', '"potType": "J"')
        elif self._money_unit == '0.01':
            data.replace('"potType": "Y""', '"potType": "F"')
        if self._award_mode == '2':
            data.replace('"doRebate": "yes"', '"doRebate": "no"')

        logger.info(f'Bet content = {data}')
        bet_response = self._session.post(url=self._env_config.get_post_url() + self._api_url, data=data,
                                          headers=self._header)
        logger.info(f'Bet response = {bet_response.json()}\n')
        return bet_response.json()

    def bet_trace(self, game_name, stop_on_win):
        games = self._conn_postgre.get_lottery_games(game_name[0])
        expected = 'ok'
        bet_response = self.bet_yft(lottery_name=game_name[0], stop_on_win=stop_on_win, games=games,
                                    is_trace=False)
        if bet_response['status'] == expected:
            print(
                f'{game_name[1]}投注追號成功。　訂單編號：{bet_response["content"]["orderNo"]}'
                f'\n用戶餘額：{bet_response["content"]["_balUsable"]} ; 投注金額：{bet_response["content"]["_balWdl"]}')
        else:
            self.fail(f'投注失敗，接口返回：{bet_response}')

        bet_response = self.bet_yft(lottery_name=game_name[0], stop_on_win=stop_on_win, games=games,
                                    is_trace=True)
        if bet_response['status'] == expected:
            print(
                f'{game_name[1]}追號全彩種成功。　訂單編號：{bet_response["content"]["orderNo"]}'
                f'\n用戶餘額：{bet_response["content"]["_balUsable"]} ; 投注金額：{bet_response["content"]["_balWdl"]}')
        else:
            self.fail(f'投注失敗，接口返回：{bet_response}')
