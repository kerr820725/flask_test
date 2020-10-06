#!/usr/bin/env python
# coding: utf-8
import traceback
from http.client import HTTPException

from flask import Flask, render_template, request, jsonify, redirect, make_response, url_for, Response, abort
import datetime
from dateutil.relativedelta import relativedelta
import requests
import json
import image_test
import os
import AutoTest
from time import sleep
import random
import threading
import time
import test_benefit
import calendar
import celery
import test_lotteryRecord
import logging
from flask import current_app
from logging import FileHandler
import urllib3
from bs4 import BeautifulSoup
import twstock, stock
import pandas as pd
import numpy as np
import re
from Utils import Config

app = Flask(__name__)  # name 為模塊名稱
logger = logging.getLogger('flask_test')
url_dict = {}  # 存放url 和街口狀態 , 給domain_ 用


def iapi_login(envir):  # iapi 抓取沙巴token
    session = requests.Session()
    global headerSb
    global envSb
    envSb = Config.EnvConfigApp(envir)
    headerSb = {
        'User-Agent': Config.UserAgent.PC.value,
        'Content-Type': 'application/json'
    }

    if envir == 'dev02':
        user = 'hsieh100'
    elif envir == '188':
        user = 'kerr001'
    else:
        raise Exception('envir 參數錯誤')

    login_data = {
        "head": {
            "sessionId": ''},
        "body": {
            "param": {
                "username": user + "|" + envSb.get_uuid(),
                "loginpassSource": envSb.get_login_pass_source(),
                "appCode": 1,
                "uuid": envSb.get_uuid(),
                "loginIp": 2130706433,
                "device": 2,
                "app_id": 9,
                "come_from": "3",
                "appname": "1"
            }
        }
    }
    r = session.post(envSb.get_iapi() + '/front/login', data=json.dumps(login_data), headers=headerSb)
    # print(r.text)
    global token
    token = r.json()['body']['result']['token']
    # print(token)


def sb_game():  # iapi沙巴頁面
    session = requests.Session()

    data = {"head": {"sessionId": token}, "body": {"param": {"CGISESSID": token,
                                                             "loginIp": "10.13.20.57", "types": "1,0,t", "app_id": 9,
                                                             "come_from": "3", "appname": "1"}}}

    r = session.post(envSb.get_iapi() + '/sb/mobile', data=json.dumps(data), headers=headerSb)
    # print(r.text)
    global sb_url
    sb_url = r.json()['body']['result']['loginUrl']
    cookies = r.cookies.get_dict()


def get_sb():  # 沙巴體育
    session = requests.Session()
    iapi_login('dev02')
    sb_game()
    # 抓取沙巴,token成功的方式, 先get 在post
    r = session.get(sb_url + '/', headers=headerSb)
    cookies = r.cookies.get_dict()
    r = session.post(sb_url + '/', headers=headerSb)

    headerSb['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    session = requests.Session()

    data = {
        'GameId': 1,
        'DateType': 't',
        'BetTypeClass': 'WhatsHot',
        # 'Matchid':''
    }
    url = 'http://smartsbtest.thirdlytest.st402019.com'
    # /Odds/ShowAllOdds ,   /Odds/GetMarket
    r = session.post(url + '/Odds/ShowAllOdds', headers=headerSb, data=data, cookies=cookies)

    global sb_list
    sb_list = []
    # print(r.json())
    game = r.json()['Data']['NewMatch']
    game_map = r.json()['Data']['TeamN']
    for dict_ in game:
        team1 = game_map[str(dict_['TeamId1'])]
        # team1 = game['TeamId1']
        team2 = game_map[str(dict_['TeamId2'])]
        # print(team1,team2,score1,score2)
        game_dict = {}
        for k in dict_:  # 字典的keys 找出來
            if k in ['MatchId', 'MarketId', 'T1V', 'T2V', 'TeamId1', 'TeamId2', 'Etm']:
                game_dict[k] = dict_[k]
            game_dict['team1name'] = team1
            game_dict['team2name'] = team2
            date_day = dict_['Etm'].split('T')  # 將str 分割成 日棋 和時間
            d = datetime.datetime.strptime(date_day[0] + ' ' + date_day[1], '%Y-%m-%d %H:%M:%S')  # date_day 0為年月日, 1為時間
            # print(d)
            game_dict['Etm'] = (d + relativedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S')  # 加12小時
        sb_list.append(game_dict)
    sb_list.sort(key=lambda k: (k.get('Etm', 0)))  # 列表裡包字典, 時間排序

    for i in sb_list:  # list取出各個字點
        # print(i['MatchId'])#抓出mathch id ,去對應 賠率
        data['Matchid'] = i['MatchId']
        r = session.post(url + '/Odds/GetMarket', headers=headerSb, data=data, cookies=cookies)
        # print(r.text)
        game_Odd = (r.json()['Data']['NewOdds'])
        # print(game_Odd)
        for odd in game_Odd:
            if odd['BetTypeId'] == 5:  # 抓 特定玩法
                i['price1'] = odd['Selections']['1']['Price']  # 多增加賠率欄位
                i['price2'] = odd['Selections']['2']['Price']
                # game_list.append(i)
            else:
                pass


def date_time():  # 給查詢 獎期to_date時間用, 今天時間
    global today_time

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    format_month = '{:02d}'.format(month)
    format_day = '{:02d}'.format(day)
    today_time = '%s-%s-%s' % (year, format_month, format_day)


def test_sport(type_keys='全部'):  # 企鵝網
    header = {
        'User-Agent': Config.UserAgent.PC.value
    }
    type_ = {'全部': 0, "英超": 1}
    date_time()
    session = requests.Session()

    r = session.get('http://live.qq.com' +
                    '/api/calendar/game_list/%s/%s/%s' % (type_[type_keys], today_time, today_time),
                    headers=header)
    # print(r.json())
    # print(r.json())
    global sport_list
    sport_list = []  # 存放請求
    len_game = len(r.json()[today_time])  # 當天遊戲列表長度
    # print(r.json()[today_time])

    for game in range(len_game):  # 取出長度
        game_dict = r.json()[today_time][game]
        # print(game_dict)
        play_status = game_dict['play_status']
        # if play_status != '1':#1: 正在 ,2:比完, 3: 還未開打
        '''
        team1_name =game_dict['team1_name']
        team2_name = game_dict['team2_name']
        team1_score = game_dict['team1_score']
        team2_score = game_dict['team2_score']
        '''
        game_new = {}  # 把需要抓取的欄位 存放近來,  在把所有當天比賽放到game_list
        for i in game_dict.keys():
            if i in ['id', 'team1_id', 'team2_id', 'team1_name',
                     'team2_name', 'team1_score', 'team2_score', 'play_status', 'team1_icon',
                     'team2_icon', 'category_name']:
                game_new[i] = game_dict[i]  # key = value
            else:
                pass
        # print(game_new)
        sport_list.append(game_new)
        # else:
        # pass
    # print(game_new)
    # print(sport_list)


# test_sport('全部')

@app.route('/form', methods=['POST', 'GET'])
def test_form():  # 輸入/form 頁面, 呼叫render_template的html
    if request.method == "POST":
        username = request.form['username']  # 在頁面上填的資料
        email = request.form['email']
        hobbies = request.form['hobbies']
        return redirect(url_for('showbio',  # 提交
                                username=username,  # 前面為參數,後面為資料
                                email=email,
                                hobbies=hobbies))  # redirect 重新定向
    return render_template('bio_form.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/showbio', methods=["GET"])
def showbio():  # 提交submit後的頁面顯示
    username = request.args.get('username')
    email = request.args.get('email')
    hobbies = request.args.get('hobbies')
    return render_template("show_bio.html",
                           username=username,  # 前面username 傳回html的 ,後面username 是用戶填寫
                           email=email,
                           hobbies=hobbies)


@app.route('/sport', methods=["GET"])
def sport_():  # 體育比分
    test_sport()
    # return jsonify(game_list)
    return render_template('sport.html', sport_list=sport_list, today_time=today_time)


@app.route('/sportApi', methods=['GET'])
def sport_api():  # 體育api
    test_sport()
    return jsonify(sport_list)


@app.route('/sb', methods=['GET'])
def sb_():
    get_sb()
    date_time()
    return render_template('sb.html', sb_list=sb_list, today_time=today_time)


@app.route('/sbApi', methods=['GET'])
def sb_api():  # 體育api
    get_sb()
    return jsonify(sb_list)


@app.route('/image', methods=['GET'])
def image_():  # 調整圖片大小
    img_path = (os.path.join(os.path.expanduser("~"), 'Desktop'))
    return render_template('image.html', img_path=img_path)


@app.route('/imageAdj', methods=["POST"])
def imageAdj():
    testInfo = {}  # 存放 圖名,長,寬 的資料
    image_name = request.form.get('image_name')
    height = request.form.get('height')
    width = request.form.get('width')
    testInfo['image_name'] = image_name
    testInfo['height'] = height
    testInfo['width'] = width
    image_test.image_(image_name, height, width)  # 將圖名, 長,寬 回傳給 image_test檔案下 image_的 func使用
    msg = image_test.msg  # 宣告image_test方法裡 global msg變數
    testInfo['msg'] = msg

    return json.dumps(testInfo['msg'])

@app.route('/autoTest', methods=["GET", "POST"])  # 自動化測試 頁面
def autoTest():
    try:
        if request.method == "POST":
            logger.info('logged by app.module')
            current_app.logger.info('logged by current_app.logger')
            # response_status ='start_progress'
            # return redirect("/progress")
            testcase = []
            username = request.form.get('username')
            test_case = request.form.getlist('test_Suite')  # 回傳 測試案例data內容
            envConfig = Config.EnvConfig(request.form.get('env_type'))  # 初始化
            awardmode = request.form.get('awardmode')# 頁面獎金玩法選擇
            red = request.form.get('red_type')#紅包選擇
            money = request.form.get('moneymode')#金額模式
            print(red,awardmode)
            print(envConfig.get_post_url())# url
            domain_url = envConfig.get_post_url().split('http://')[1]# 後台全局 url 需把 http做切割
            
            domain_type = envConfig.get_joint_venture(envConfig.get_env_id(),domain_url)# 查詢 後台是否有設置 該url 
            #domain_type = Config.domain_type#後台 該url joint_venture 的 類型

            AutoTest.Joy188Test.select_userid(AutoTest.Joy188Test.get_conn(envConfig.get_env_id()),username,domain_type)  # 查詢用戶 userid
            userid = AutoTest.userid
            # joint_venture = AutoTest.joint_venture #joint_venture 為合營,  0 為一般, 1為合營
            print(userid)  # joint_venture)
            print(username)

            for test in test_case:
                testcase.append(test)
            print(testcase)
            if len(userid) > 0:  # userid 值為空,　代表該ＤＢ　環境　沒有此用戶名　，　就不用做接下來的事
                AutoTest.suite_test(testcase,username,envConfig.get_domain(),red,awardmode,money)# 呼叫autoTest檔 的測試方法, 將頁面參數回傳到autoTest.py
                return redirect('report')
            else:
                # print(response_status)
                return('此環境沒有該用戶')# 強制return 讓頁面location.reload
        # return redirect("/report")
    except Exception as e:
        from Utils.TestTool import traceLog
        traceLog(e)
        abort(500)
    return render_template('autoTest.html')


@app.route("/report", methods=['GET'])
def report():
    return render_template('report.html')


@app.route('/progress')
def progress():  # 執行測試案例時, 目前 還位判斷 request街口狀態,  需 日後補上
    def generate():
        x = 0
        # global response_status
        # print(response_status)
        while x <= 100:
            # print(response_status)
            yield "data:" + str(x) + "\n\n"  # data內容, 換行
            x = x + 1
            sleep(0.5)
        # yield "data:"+ str(100)

    return Response(generate(), mimetype='text/event-stream')


@app.route('/benefit', methods=["GET", "POST"])  # 日工資頁面  按鈕提交後, 在導往  benefit_日工資/分紅頁面
def benefit():
    if request.method == "POST":
        testInfo = {}  # 存放資廖
        cookies_dict = {}  # 存放cookie
        global result  # 日工資 data資料

        cookies_ = request.cookies  # 目前的改瀏覽器上的cookie
        print(cookies_)

        benefit_type = request.form.get('benefit_type')
        username = request.form.get('username')
        month = request.form.get('month')
        day = request.form.get('day')
        env = request.form.get('env')
        testInfo['benefit_type'] = benefit_type
        testInfo['username'] = username
        testInfo['month'] = month
        testInfo['day'] = day
        testInfo['env'] = env

        print(testInfo)  # 方便看資料用

        if env not in cookies_.keys():  # 請求裡面 沒有 這些環境cookie,就再登入各環境後台
            test_benefit.admin_Login(env)  # 登入生產環境 後台
            admin_cookie = test_benefit.admin_cookie  # 呼叫  此function ,

            cookies_dict[env] = admin_cookie['admin_cookie']
            cookies = admin_cookie['admin_cookie']
            # print(cookies_dict)
        else:
            cookies = cookies_[env]  # cookies_已經有了, 就直接使用

        if benefit_type == 'day':
            test_benefit.game_report_day(user=username, month=int(month), day=int(day), cookies=cookies, env=env)
            result = test_benefit.result_data
            print(result)
            if result['msg'] == '你輸入的日期或姓名不符,請再確認':  # 有cookie, 但cookie失效, 需再重新做
                test_benefit.admin_Login(env)
                admin_cookie = test_benefit.admin_cookie  # 呼叫  此function ,
                cookies_dict[env] = admin_cookie['admin_cookie']
                cookies = admin_cookie['admin_cookie']
                test_benefit.game_report_day(user=username, month=int(month), day=int(day), cookies=cookies, env=env)
                result = test_benefit.result_data
                res = redirect('benefit_day')
            else:
                res = redirect('benefit_day')
            if cookies_dict == {}:  # 會為空 代表,瀏覽器 有存在的cookie. 不用再額外在set
                pass
            else:
                res.set_cookie(env, cookies_dict[env])
            return res
        elif benefit_type == 'month':  # 需將 頁面獲得的 0或1  轉帳 日期 上半月: 15 ,下半月: 當月最後一天
            # print(type(day))
            print(type(day), day)
            if day == '0':
                day = 15
            elif day == '1':
                now = datetime.datetime.now()
                day = calendar.monthrange(now.year, int(month))[1]  # 獲取當月 最後一天
            test_benefit.game_report_month(user=username, month=int(month), day=int(day), cookies=cookies, env=env)
            result = test_benefit.result_data
            res = redirect('benefit_month')
            if cookies_dict == {}:
                pass
            else:
                res.set_cookie(env, cookies_dict[env])
            return res
        else:
            print('福利中心 類型錯誤')
    return render_template('benefit.html')  # 這邊是 單存get,表單填寫頁面


@app.route('/benefit_day', methods=["GET"])
def benefit_day():
    return render_template('benefit_day.html', result=result)


@app.route('/benefit_month', methods=["GET"])
def benefit_month():
    return render_template('benefit_month.html', result=result)


@app.route('/report_APP', methods=["GET", "POST"])  # APP戰報
def report_APP():
    global result
    if request.method == 'POST':
        envtype = request.form.get('env_type')
        print(envtype)
        if envtype == 'dev':
            env = 0
        else:  # 188
            env = 1
        test_lotteryRecord.all_lottery(env)
        result = test_lotteryRecord.result

        return redirect('report_AppData')

    return render_template('report_APP.html')


@app.route('/report_AppData', methods=["GET"])  # APP戰報資料顯示
def report_AppData():
    return render_template('report_AppData.html', result=result)


@app.route('/domain_list', methods=["GET"])  # 域名列表測試,抓取 http://172.16.210.101/domain_list  提供的 網域
def domain_list():
    return render_template('domain_list.html')


def session_get(url):
    urllib3.disable_warnings()  # 解決 會跳出 request InsecureRequestWarning問題
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.100 Safari/537.36'
    }
    global r, url_dict
    try:
        r = requests.get(url + '/', headers=header, verify=False, timeout=5)
    except:
        pass
    url_dict[url] = r.status_code
    # print(url_dict)


@app.route('/domain_status', methods=["GET"])
def domain_status():  # 查詢domain_list 所有網域的  url 接口狀態
    global url_dict
    urllib3.disable_warnings()  # 解決 會跳出 request InsecureRequestWarning問題
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.100 Safari/537.36'
    }
    r = requests.get('http://66dca985.ngrok.io' + '/domain_list', headers=header)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    url_dict = {}  # 存放url 和 皆口狀態
    try:  # 過濾 從頁面上抓取的url, 有些沒帶http
        for i in soup.find_all('table', {'class': 'domain_table'}):
            for a in i.find_all('a'):
                if 'http' not in a.text:
                    url = 'http://' + a.text
                    url_dict[url] = ''  # 先存訪到url_dict
                else:  # 這邊提供的  頁面 不用做額外處理, 就是 a.text
                    url_dict[a.text] = ''
        threads = []
        for url_key in url_dict:
            threads.append(threading.Thread(target=session_get, args=(url_key,)))
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    except requests.Timeout as e:
        pass
    except urllib3.exceptions.NewConnectionError as e:
        print(e)
    print(url_dict)
    return url_dict
    # return render_template('domain_status.html',url_dict=url_dict)


@app.route('/stock_search', methods=["GET", "POST"])
def stock_search():
    stock_detail = {}
    try:
        if request.method == "POST":
            stock_num = request.form.get('stock_search')
            stock_name = request.form.get('stock_search2')
            print(stock_num,stock_name)#股票號碼,股票名稱
            if stock_name not in  [None,'']:# 代表頁面 輸入名稱 , 先從DB 找 有沒有該名稱,在去yahoo找
                stock.stock_selectname(stock.kerr_conn(),stock_name)#找出相關資訊
                stock_detail2 = stock.stock_detail2
                if len(stock_detail2) == 0:# 名稱營收db為空的, 就不列印營收資訊
                    return('沒有該股票名稱: %s'%stock_name)
                else:# DB有找到該名稱 ,
                    stock_deatil2 = stock.stock_detail2
                    print(stock_deatil2)
                    stock_num = str(list(stock_deatil2.values())[0][1])#號碼
                    stock.df_test(stock_num)
                    stock.df_test2(stock_num)
                    now = stock.now#查詢時間
                    latest_close = stock.latest_close#最新收盤
                    latest_open = stock.latest_open
                    latest_high = stock.latest_high
                    latest_low = stock.latest_low
                    latest_volume = stock.latest_volume
            else:# 輸入號碼 ,和頁面輸入名稱流程不同,  有號碼 先從yahoo直接去找
                try:
                    stock_name = twstock.codes[stock_num][2]
                    stock.df_test(stock_num)
                    stock.df_test2(stock_num)
                    now = stock.now#查詢時間
                    latest_close = stock.latest_close#最新收盤
                    latest_open = stock.latest_open
                    latest_high = stock.latest_high
                    latest_low = stock.latest_low
                    latest_volume = stock.latest_volume
                except KeyError:
                    return('沒有該股票號碼: %s'%stock_num)#yahoo沒有,DB正常就不會有
                stock.stock_selectnum(stock.kerr_conn(),int(stock_num))# 有股號後, 從mysql 抓出更多資訊
                stock_detail2 = stock.stock_detail2
                if len(stock_detail2) == 0:# 營收db為空的,但 yahoo查詢是有該股的, 就不列印營收資訊 ,
                    data ={"股票名稱":stock_name,'股票號碼':stock_num,"目前股價":latest_close,
                    '開盤':latest_open,'高點': latest_high,'低點': latest_low,'成交量':latest_volume,
                    "查詢時間":now
                    }
                    frame = pd.DataFrame(data,index=[0])
                    print(frame)
                    return(frame.to_html())
                else:# yahoo有, DB也有, 就是多列印 營收
                    pass# 走到下面  和輸入 名稱  共用  營收邏輯
                
            # 有營收, 輸入號碼 和輸入 名稱 共用
            stock_curMonRev = list(stock_detail2.values())[0][4]
            stock_lastMonRev = list(stock_detail2.values())[0][5]
            stock_lastYearMonRev=list(stock_detail2.values())[0][6]
            stock_lastMonRate=list(stock_detail2.values())[0][7]
            stock_lastYearMonRate=list(stock_detail2.values())[0][8]
            stock_curYearRev=list(stock_detail2.values())[0][9]
            stock_lastYearRev=list(stock_detail2.values())[0][10]
            stock_lastYearRate=list(stock_detail2.values())[0][11]
            stock_memo=list(stock_detail2.values())[0][12]
            data ={"股票名稱":stock_name,'股票號碼':stock_num,"目前股價":latest_close,
            '開盤':latest_open,'高點': latest_high,'低點': latest_low,'成交量':latest_volume,
            "當月營收":stock_curMonRev,'上月營收':stock_lastMonRev,'去年當月': stock_lastYearMonRev,"上月營收增":stock_lastMonRate,
            '去年同月營收增減':stock_lastYearMonRate,'今年營收':stock_curYearRev,'去年營收':stock_lastYearRev,'去年營收增減': stock_lastYearRate,'股票備注':stock_memo, "查詢時間":now
            }
            now_hour = datetime.datetime.now().hour #現在時間 :時
            weekday = datetime.date.today().weekday()+1#現在時間 :周, 需加1 , 禮拜一為0
            print('現在時數: %s,禮拜:%s'%(now_hour,weekday))
            if now_hour > 14 or weekday in [6,7] :
                print('大於最後成交時間或者六日,不再做更新股價')
            else:
                print(stock.stock_detail2)  # mysql抓出來的 資訊
                '''
                stock_prize = (stock_detail['realtime']['latest_trade_price'])  # 股票 最新一筆成交價
                print(stock_prize, type(stock_prize))  # 為一個 str ,需把 小數點  . 三和四 去除掉
                if stock_prize == '-':  # 抓出來 是  "-"  就先不理會,給一個值0
                    stock_prize = 0
                else:
                    stock_prize = stock_prize[0:-2]  # 後面兩個00不用,   到小數電第四位即可
                # stock_prize = stock_prize[0:-2]# 後面兩個00不用,   到小數電第四位即可
                print(stock_prize)
                '''

                stock.stock_update(stock.kerr_conn(), float(latest_close), int(stock_num))  # 將股價 Update進去 Mysql

                '''
                data = {"股票名稱": stock_detail['info']['name'], "目前股價": latest_close,
                        "開盤": latest_open,
                        "高點": stock_detail['realtime']['high'], "低點": stock_detail['realtime']['low'],
                        "查詢時間": stock_detail['info']['time']}
                '''
            frame = pd.DataFrame(data, index=[0])
            print(frame)
            # print(frame.to_html())
            return frame.to_html()
        return render_template('stock.html')
    except requests.exceptions.Timeout as e:
        print(e)


@app.route('/stock_search2', methods=["POST"])
def stock_search2():
    stock_type = request.form.getlist('Revenue')
    print(stock_type)
    stock.stock_select2(stock.kerr_conn(),stock_type)  # select 出來
    stock_detail3 = stock.stock_detail3
    stock_num, stock_name, stock_prize, stock_curMonRev, stock_lastMonRev, stock_lastYearMonRev, stock_lastMonRate, stock_lastYearMonRate, stock_curYearRev, stock_lastYearRev, stock_lastYearRate, stock_memo = [], [], [], [], [], [], [], [], [], [], [], []

    for num in stock_detail3.keys():
        stock_num.append(stock_detail3[num][1])
        stock_name.append(stock_detail3[num][2])
        try:
            if stock_detail3[num][3] == 0:  # 股價是0,代表還沒有Update 股價過

                stock_detail = twstock.realtime.get(str(stock_detail3[num][1]))
                print(stock_detail)
                prize = (stock_detail['realtime']['latest_trade_price'])  # 股票 最新一筆成交價
                if prize == '-':  # 抓出來 是  "-"  就先不理會,給一個值0
                    prize = 0
                else:
                    prize = prize[0:-2]  # 後面兩個00不用,   到小數電第四位即可
                print(prize, type(prize))
                stock_prize.append(prize)
                stock.stock_update(stock.kerr_conn(), float(prize),
                                   int(stock_detail3[num][1]))  # 將股價 Update進去 Mysql
            else:
                stock_prize.append(stock_detail3[num][3])
        except requests.exceptions.ConnectionError:
            print('連線失敗')
            stock_prize.append(stock_detail3[num][3])
        stock_curMonRev.append(stock_detail3[num][4])
        stock_lastMonRev.append(stock_detail3[num][5])
        stock_lastYearMonRev.append(stock_detail3[num][6])
        stock_lastMonRate.append(stock_detail3[num][7])
        stock_lastYearMonRate.append(stock_detail3[num][8])
        stock_curYearRev.append(stock_detail3[num][9])
        stock_lastYearRev.append(stock_detail3[num][10])
        stock_lastYearRate.append(stock_detail3[num][11])
        stock_memo.append(stock_detail3[num][12])

    # print(stock_num,stock_name,stock_prize,stock_curMonRev,stock_lastMonRev,stock_lastYearMonRev,stock_lastMonRate,stock_lastYearMonRate,stock_curYearRev,stock_lastYearRev,stock_lastYearRate,stock_memo)
    print(stock_prize)

    data = {'股票號碼': stock_num, "股票名稱": stock_name, "股價": stock_prize, "當月營收": stock_curMonRev,
            "上月營收增減": stock_lastMonRate,
            '去年同月營收增減': stock_lastYearMonRate, '今年營收': stock_curYearRev, '去年營收': stock_lastYearRev,
            '去年營收增減': stock_lastYearRate, '股票備注': stock_memo}
    frame = pd.DataFrame(data)
    print(frame)
    # print(frame.to_html())
    return frame.to_html()



def game_map():  # 玩法 和 說明 mapping
    global game_explan, game_playtype  # 說明, 玩法
    if '五星' in game_playtype:
        if game_playtype in ['复式', '单式']:
            game_explan = '五個號碼順續需全相同'
        elif '组选120' in game_playtype:
            game_explan = '五個號碼相同,順續無需相同(開獎號無重覆號碼)'

    else:
        game_explan = 'test'
    return game_explan
@app.route('/stock_search3',methods=["POST"])    
def stock_search3():
    stock.stock_search3(stock.kerr_conn())
    stock_detail = stock.stock_detail3


def status_style(val):  # 判斷狀態,來顯示顏色屬性 , 給 game_order 裡的order_status用
    if val == '中獎':
        color = 'blue'
    elif val == '未中獎':
        color = 'red'
    else:
        pass
    return ('color:%s' % color)


@app.route('/game_result', methods=["GET", "POST"])  # 查詢方案紀錄定單號
def game_result():
    global game_explan, game_playtype
    cookies_dict = {}  # 存放cookie,避免一隻 登入後台
    if request.method == "POST":
        game_code = request.form.get('game_code')  # 訂單號
        game_type = request.form.get('game_type')  # 玩法
        env = request.form.get('env_type')  # 環境
        cookies_ = request.cookies  # 瀏覽器上的cookie
        print(cookies_)
        if env == 'dev02':  # 傳給DB 環境 get_conn(env)用
            envs = 0
        else:
            envs = 1
        if game_code != '':  # game_code 不為空,代表前台 是輸入 訂單號
            AutoTest.Joy188Test.select_gameResult(AutoTest.Joy188Test.get_conn(envs), game_code)  # 傳回此方法.找出相關 訂單細節
            game_detail = AutoTest.game_detail  # 將 global  game_detail 宣告變數 遊戲訂單的 內容
            if len(game_detail[game_code]) == 0:
                return "此環境沒有此訂單號"
            else:
                game_status = game_detail[game_code][1]  # 需判斷  訂單狀態
                if game_status == 1:
                    game_status = '等待開獎'
                elif game_status == 2:
                    game_status = '中獎'
                elif game_status == 3:
                    game_status = '未中獎'
                elif game_status == 4:
                    game_status = '撤銷'
                else:
                    game_status = '待確認'
                game_amount = float(game_detail[game_code][2] / 10000)  # 投注金額  需在除 1萬
                game_retaward = float(game_detail[game_code][10] / 10000)  # 反點獎金 需除1萬
                game_moneymode = game_detail[game_code][12]  # 元角分模式 , 1:元, 2: 角
                if game_moneymode == 1:
                    game_moneymode = '元'
                elif game_moneymode == 2:
                    game_moneymode = '角'
                else:
                    game_moneymode = '分'

                # 遊戲玩法 : 後三 + 不定位+ 一碼不定位 , 並回傳給 game_map 來做 mapping
                game_playtype = game_detail[game_code][4] + game_detail[game_code][5] + game_detail[game_code][6]
                print("玩法: %s" % game_playtype)

                game_award = float(game_detail[game_code][13] / 10000)  # 中獎獎金
                AutoTest.return_env(envs)  # 呼叫環境變數, 傳給 登入後台用
                print(AutoTest.env_)

                if env not in cookies_.keys():
                    print("瀏覽器上 還沒有後台cookie,需登入")
                    AutoTest.Joy188Test.admin_login()
                    award_id = game_detail[game_code][17]  # 獎金id, 傳后查詢尋是哪個獎金組
                    lotteryid = game_detail[game_code][14]  # 採種Id 傳給 後台 查詢哪個彩種
                    session = requests.Session()
                    header = AutoTest.header  # 後台 登入header
                    cookie = AutoTest.cookies['ANVOAID']  # 後台登入 cookie

                    res = redirect('game_result')
                    res.set_cookie(env, cookie)  # 存放cookie

                    # return res
                    # print(cookie)
                    # cookies_[env] = cookie
                else:
                    print("瀏覽器已經存在cookie,無須登入")
                    cookie = cookies_[env]
                header['Cookie'] = 'ANVOAID=' + cookie  # 存放後台cookie
                # header['Content-Type'] ='application/json'
                r = session.get(AutoTest.admin_url + "/gameoa/queryGameAward?lotteryId=%s&awardId=%s&status=1" % (
                    lotteryid, award_id)
                                , headers=header)  # 登入後台 查詢 用戶獎金值
                # print(r.text)
                soup = BeautifulSoup(r.text, 'lxml')
                if game_detail[game_code][16] == 0:  # 理論獎金為0, 代表一個完髮有可能有不同獎金
                    print('有多獎金玩法')
                    point_id = str(game_detail[game_code][15])
                    bonus = []
                    for i in soup.find_all('span', id=re.compile("^(%s)" % point_id)):
                        bonus.append(float(i.text))  # 有多個獎金
                    bonus = " ".join([str(x) for x in bonus])  # 原本bonus裡面裝 float  .需list裡轉成字元,

                    # bonus = "".join(bonus)# dataframe 不能支援list
                else:
                    point_id = str(game_detail[game_code][15]) + "_" + str(
                        game_detail[game_code][16])  # 由bet_type_code + theory_bonus 串在一起(投注方式+理論獎金])
                    for i in soup.find_all('span', id=re.compile("^(%s)" % point_id)):  # {'id':point_id}):
                        bonus = float(i.text)
                print(bonus, point_id)
                game_awardmode = game_detail[game_code][9]  # 是否為高獎金
                if game_awardmode == 1:
                    game_awardmode = '否'
                elif game_awardmode == 2:
                    game_awardmode = '是'
                    bonus = game_retaward + bonus  # 高獎金的話, 獎金 模式 + 反點獎金
                # print(bonus)
                game_map()  # 呼叫玩法說明
                data = {"遊戲訂單號": game_code, "訂單時間": game_detail[game_code][0], "中獎狀態": game_status,
                        "投注金額": game_amount, "投注彩種": game_detail[game_code][3],
                        "投注玩法": game_playtype,
                        "投注內容": game_detail[game_code][7], "獎金組": game_detail[game_code][8], "獎金模式": bonus,
                        "獎金模式狀態": game_awardmode, "反點獎金": game_retaward, "投注倍數": game_detail[game_code][11],
                        "元角分模式": game_moneymode, "中獎獎金": game_award, "遊戲說明": game_explan
                        }
                global frame
                frame = pd.DataFrame(data, index=[0])
                print(frame)
                # return frame
                return frame.to_html()
        elif game_type != '':  # game_type 不為空,拜表前台輸入 指定玩法
            if "_" in game_type:  # 把頁面輸入  _   去除
                print('有_需移除')
                if "2000" in game_type:  # 超級2000 在DB格式 前面 多帶 _ ,不能移除
                    test_list = []  # 存放 超級2000 後新的列表,並join 新的 game_type
                    for i in game_type.split('_'):
                        if "2000" in i:
                            i = i + "_"
                        test_list.append(i)  # 新的列表
                    game_type = "".join(test_list)  # 超級2000符合的 DB mapping
                else:
                    game_type = game_type.replace("_", "")  # 不是超級2000, _ 就值皆去除
            elif game_type[-1] == " ":  # 判斷輸入後面多增加空格:
                print('輸入玩法 有空格需去除掉')
                game_type = game_type.replace(' ', '')
            print(game_type)
            AutoTest.Joy188Test.select_gameorder(AutoTest.Joy188Test.get_conn(envs), '%' + game_type + '%')
            game_order = AutoTest.game_order
            len_order = AutoTest.len_order
            # print(game_order)
            order_list = []  # 因為可能有好幾個訂單,  傳入 dataframe 需為列表 ,訂單
            order_time = []  # 時間
            order_lottery = []  # 採種
            order_type = []  # 玩法
            order_status = []  # 狀態
            order_user = []  # 用戶名
            order_detail = []  # 投注內容
            order_record = []  # 開獎號碼
            for len_ in range(len_order):  # 取出長度
                order_list.append(game_order[len_][2])  # 2為訂單號.
                order_time.append(game_order[len_][1])
                order_lottery.append(game_order[len_][0])
                order_type.append(game_order[len_][3] + game_order[len_][4] + game_order[len_][5])
                if game_order[len_][6] == 1:
                    game_order[len_][6] = '等待開獎'
                elif game_order[len_][6] == 2:
                    game_order[len_][6] = '中獎'
                elif game_order[len_][6] == 3:
                    game_order[len_][6] = '未中獎'
                elif game_order[len_][6] == 4:
                    game_order[len_][6] = '撤銷'
                else:
                    game_order[len_][6] = '確認狀態'
                order_status.append(game_order[len_][6])
                order_user.append(game_order[len_][7])
                order_detail.append(game_order[len_][8])
                order_record.append(game_order[len_][9])
            # print(order_list)
            data = {"訂單號": order_list, "用戶名": order_user, "投注時間": order_time, "投注彩種": order_lottery, "投注玩法": order_type,
                    "投注內容": order_detail, "開獎號碼": order_record, "中獎狀態": order_status}
            frame = pd.DataFrame(data)
            # test = frame.style.applymap(status_style)#增加狀態顏色 ,這是for jupyter_notebook可以直接使用
            print(frame)
            return frame.to_html()

    return render_template('game_result.html')


@app.route('/user_active', methods=["POST", "GET"])
def user_acitve():  # 驗證第三方有校用戶
    if request.method == "POST":
        user = request.form.get('user')
        env = request.form.get('env_type')
        joint_type = request.form.get('joint_type')
        if env == 'dev02':
            envs = 0
        elif env == 'joy188':
            envs = 1
        else:
            envs = 2
        AutoTest.Joy188Test.select_userid(AutoTest.Joy188Test.get_conn(envs),user,int(joint_type))
        #查詢用戶 userid
        userid = AutoTest.userid
        print(user, env)
        if len(userid) == 0:
            return ("此環境沒有該用戶")
        else:
            AutoTest.Joy188Test.select_activeAPP(AutoTest.Joy188Test.get_conn(envs), user)
            # 查詢APP有效用戶 是否有值  ,沒值 代表 沒投注

            active_app = AutoTest.active_app  # 呼叫 此變數
            # print(active_user)
            bind_card = []  # 綁卡列表.可能超過多張
            card_number = []  # 該綁卡,有被多少張數綁定,但段 是否為有效性
            # print(active_app)

            AutoTest.Joy188Test.select_activeFund(AutoTest.Joy188Test.get_conn(envs), user)  # 當月充值
            user_fund = AutoTest.user_fund
            print(user_fund)

            AutoTest.Joy188Test.select_activeCard(AutoTest.Joy188Test.get_conn(envs), user, envs)  # 查詢綁卡數量
            card_num = AutoTest.card_num  # 綁卡 和 該卡榜定幾張

            if len(active_app) == 0:  # 非有效用戶,也代表 APP 有效用戶表沒資料(舊式沒投注)
                print("%s用戶 為非有效用戶" % user)

                active_submit = 0  # 有效投注
                is_active = "否"  # 有效用戶值

                # AutoTest.Joy188Test.select_activeFund(AutoTest.Joy188Test.get_conn(envs),user)#當月充值
                if user_fund[0] == None:  # 確認沒充值
                    real_charge = 0
                else:
                    real_charge = float(user_fund[0]) / 10000  # 抓充值表, 顯示充值金額

                if len(card_num) == 0:
                    print("綁卡數量為0")
                    bind_card = "沒有綁卡"
                    card_number = ""
                else:
                    for card_ in card_num.keys():
                        print(card_)
                        print(bind_card)
                        bind_card.append(str(card_num[card_][0]))
                        card_number.append(str(card_num[card_][1]))
                    bind_card = " ,".join(bind_card)
                    card_number = " ,".join(card_number)
                print(bind_card, card_number)

                # bind_card.append("test")
            else:  # 這邊長度非0, 是select_activeAPP 這方法,有值, 需判斷 is_active 是否為1
                if active_app[2] == 0:  # 列表[1] = is_active,  值 0 非有效
                    is_active = "否"  # active_user[0][1]
                    print("%s用戶 為非有效用戶" % user)
                else:
                    is_active = "是"  # active_user[0][1]
                    print("%s用戶 為有效用戶" % user)
                active_submit = active_app[3]

                # AutoTest.Joy188Test.select_activeFund(AutoTest.Joy188Test.get_conn(envs),user)#當月充值

                if user_fund[0] == None:  # 確認沒充值
                    real_charge = 0
                else:
                    real_charge = float(user_fund[0]) / 10000  # 抓充值表, 顯示充值金額

                if len(card_num) == 0:
                    print("綁卡數量為0")
                    bind_card = "沒有綁卡"
                    card_number = ""
                else:
                    for card_ in card_num.keys():
                        bind_card.append(str(card_num[card_][0]))
                        card_number.append(str(card_num[card_][1]))
                    bind_card = " ,".join(bind_card)
                    card_number = " ,".join(card_number)
                print(bind_card, card_number)

            data = {"用戶名": user, "是否為有效用戶": is_active, "當月有效投注": active_submit,
                    "當月有效充值": real_charge, "銀行卡號": bind_card, "該卡號綁訂張數": card_number
                    }

            frame = pd.DataFrame(data, index=['是否為有效用戶'])
            print(frame)

            return frame.to_html()

    return render_template('user_active.html')


@app.route('/app_bet', methods=["POST"])
def app_bet():
    user = request.form.get('user')
    env = request.form.get('env_type')
    joint = request.form.get('joint_type')
    if env == 'dev02':
        envs = 0
    elif env == 'joy188':
        envs = 1
    else:
        envs = 2
    AutoTest.Joy188Test.select_AppBet(AutoTest.Joy188Test.get_conn(envs), user)  # APP代理中心,銷量/盈虧
    AutoTest.Joy188Test.select_userid(AutoTest.Joy188Test.get_conn(envs),user,int(joint))#查詢用戶 userid
    userid = AutoTest.userid
    print(userid)
    if len(userid) == 0:
        return('此環境沒有該用戶')
    app_bet = AutoTest.app_bet  # 銷量/盈虧
    third_list = []  # 存放第三方列表
    active_bet = []  # 第三方有效投注
    third_prize = []  # 第三方獎金
    third_report = []  # 第三方盈虧
    third_memo = []  # 第三方memo
    user_list = []
    for third in app_bet.keys():
        third_list.append(third)
        active_bet.append(app_bet[third][0])  # 有效銷量 為列表 1
        third_prize.append(app_bet[third][1])
        third_report.append(app_bet[third][2])
        if third == "ALL":
            user_list.append(user)
        else:
            user_list.append("")
        if third == "ALL":
            third_memo.append("用戶盈虧: 總獎金-有效銷量")
        elif third == 'CITY':
            third_memo.append("#後台投注紀錄盈虧值 為用戶角度")
        elif third == 'BBIN':
            third_memo.append('#獎金不會小於0')
        else:  # 待後續確認每個第三方 規則
            third_memo.append('')
    # print(user_list,active_bet,third_prize,third_report)

    data = {"用戶名": user_list,"有效銷量": active_bet, "總獎金": third_prize, "用戶盈虧": third_report,
            "備註": third_memo}
    frame = pd.DataFrame(data, index=third_list)
    print(frame)
    return frame.to_html()
@app.route('/url_token',methods=["POST","GET"])    
def url_token():
    domain_keys ={ # url 為 keys,values 0 為預設連結, 1為 DB環境參數 , 2 為預設註冊按紐顯示 
        'www.dev02.com': ['id=18408686&exp=1867031785352&pid=13438191&token=5705',0,'否','一般'],
        'www.fh82dev02.com': ['id=18416115&exp=1898836925873&pid=13518151&token=674d',0,'是','合營'],
        'www.teny2020dev02.com': ['id=18416115&exp=1898836925873&pid=13518151&token=674d',0,'是','合營'],
        'www.88hlqpdev02.com': ['id=18416447&exp=1900243129901&pid=13520850&token=c46d',0,'是','歡樂棋排'],
        'www2.joy188.com':['id=23629565&exp=1870143471538&pid=14055451&token=e609',1,'否','一般'],
        'www2.joy188.195353.com':['id=30402641&exp=1899103987027&pid=14083381&token=f2ae',1,'是','合營'],
        'www2.joy188.maike2020.com':['id=30402641&exp=1899103987027&pid=14083381&token=f2ae',1,'是','合營'],
        'www2.joy188.teny2020.com':['id=30402641&exp=1899103987027&pid=14083381&token=f2ae',1,'是','合營'],
        'www2.joy188.88hlqp.com':['id=30402801&exp=1900315909746&pid=14084670&token=296f',1,'是','歡樂棋排'],
        'www.88hlqp.com': ['id=12724515&exp=1900124358942&pid=23143290&token=60f9',2,'是','歡樂棋排'],
        'www.maike2020.com':['id=12569709&exp=1900396646000&pid=23075061&token=f943',2,'是','合營'],
        'www.maike2021.com':['id=12569709&exp=1900396646000&pid=23075061&token=f943',2,'是','合營'],
        'www.maike2022.com':['id=12569709&exp=1900396646000&pid=23075061&token=f943',2,'是','合營'],
        'www.maike2023.com':['id=12569709&exp=1900396646000&pid=23075061&token=f943',2,'是','合營'],
        'www.teny2020.com':['id=12727731&exp=1900585598288&pid=23119541&token=60ac&qq=7769700',2,'是','合營'],
        'www.fh82.com':['id=12464874&exp=1883450993237&pid=2163831&token=b12f&qq=1055108800',1,'是','一般'],
        'www.fhhy2020.com':['',2,'待確認','合營'],
        'www.fh888.bet':['',2,'待確認','合營'],
        'www.fh666.bet':['',2,'待確認','合營']
    }
    if request.method == "POST":
        token = request.form.get('token')
        id_ = request.form.get('id')
        user = request.form.get('user')
        env = request.form.get('env_type')
        joint_type = request.form.get('joint_type')
        #print(env)
        if env == '0':
            env_type = '02'
        elif env == '1':
            env_type = '188'
        else:
            env_type = '生產'
        
        #print(token,env,id_,joint_type,domain)
        if token not in  ['',None] : #token 直不為空, 代表頁面輸入的是token
            print('頁面輸入token')
            AutoTest.Joy188Test.select_urltoken(AutoTest.Joy188Test.get_conn(int(env)),token,joint_type)
            token_url = AutoTest.token_url
            print(token_url)
            user =[]
            user_url = []
            len_data = [] # 用註冊碼查, 長度可能會有多個
            for i in token_url.keys():
                user.append(token_url[i][0])
                user_url.append(token_url[i][1])
                len_data.append(i)
            data = {'用戶名':user,'開戶連結':user_url}        
        elif id_ not in ['',None]:
            print('頁面輸入id')
            AutoTest.Joy188Test.select_urltoken(AutoTest.Joy188Test.get_conn(int(env)),id_,joint_type)
            token_url = AutoTest.token_url
            print(token_url)
            user =[]
            user_url = []
            for i in token_url.keys():
                user.append(token_url[i][0])
                user_url.append(token_url[i][1])
            
            data = {'用戶名':user,'開戶連結':user_url}
            len_data = [0]#輸入ID 查 連結, ID 為唯一直
        elif user not in ['',None]:# 頁面輸入 用戶名 查詢用戶從哪開出
            print('頁面輸入用戶名')
            AutoTest.Joy188Test.select_userUrl(AutoTest.Joy188Test.get_conn(int(env)),user,2,joint_type)
            user_url =AutoTest.user_url
            print(user_url)
            if len(user_url) == 0:# user_url 有可能找不到 ,再從 user_customer 的refere去找
                AutoTest.Joy188Test.select_userid(AutoTest.Joy188Test.get_conn(int(env)),user,joint_type)# 檢查環境是否有這用戶
                if len(AutoTest.userid) == 0:
                    return('%s環境沒有該用戶: %s'%(env_type,user))
                
                data = {'用戶名':user,'用戶從此連結開出':'被刪除'}
                frame = pd.DataFrame(data,index=[0])
                print(frame)
                return frame.to_html()
                 
            elif user_url[0][4] != -1:# '失效'
                print('連結失效,從referer找')
                days= '是'# user_url 找不到的連結 ,一定失效或被刪除
                AutoTest.Joy188Test.select_userUrl(AutoTest.Joy188Test.get_conn(int(env)),user,0)
                user_url =AutoTest.user_url
                print(user_url)
            else:# 這邊代表  user_url 是有值,  在去從days 判斷是否失效
                if user_url[0][4] == -1:
                    days= '否'
                else:# 不等於 -1 為失效
                    days = '是'
            data = {'用戶名':user,'用戶從此連結開出':user_url[0][1],'連結是否失效':days,
            '用戶代理線':user_url[0][2],'裝置':user_url[0][3]}
            len_data = [0]
        else:# 輸入domain 查尋 預設連結
            try:# 對頁面輸入的domain, 做格式化處理
                domain = request.form.get('domain').strip()# 頁面網域名稱 . strip 避免有空格問題
                '''
                if 'joy188' in domain:# joy188 前面為www2
                    if 'www2' in domain:
                        pass
                    else:
                        domain = 'www2.%s.com'%domain
                elif any(s in domain for s in ['com','www']):# 網域名稱 有帶 www /com 不用額外更動
                    pass #  後續可以 對 開頭是否有 http ,尾不是 com  去做處理
                else: # 沒有帶  www
                    
                    if any(s in domain for s in ['fh888','fh666']):
                        domain = 'www.%s.bet'%domain
                    else:
                        domain = 'www.%s.com'%domain
                '''    
                print(domain)
                #env = domain_keys[domain][1]#  1 為環境 ,0 為預設連結
            except KeyError:# 
                return('沒有該連結')
            AutoTest.Joy188Test.select_domainUrl(AutoTest.Joy188Test.get_conn(int(env)),domain)
            domain_url = AutoTest.domain_url
            print(domain_url)
            if len(domain_url) != 0:# 代表該預名 在後台全局管理有做設置
                domain_admin = '是'# 後台是否有設定 該domain
                register_display = domain_url[0][3]# 前台註冊按紐 是否隱藏
                if register_display == 0:
                    register_display = '關閉'
                else:
                    register_display = '開啟'
                app_display = domain_url[0][4]# 前台掃碼 是否隱藏
                if app_display == 0:
                    app_display = '關閉'
                else:
                    app_display = '開啟'
                admin_url = domain_url[0][2]#url 是預設連結,或者後台的設置 代理聯結
                agent = domain_url[0][1]
                domain_type = domain_url[0][5]# 後台設置 環境組 的欄位
                if domain_type == 0:#  0:一般,1:合營,2:歡樂期排
                    domain_type = '一般'
                elif domain_type == 1:
                    domain_type = '合營'
                else:
                    domain_type = '歡樂期排'
                env_type = domain_type+"/"+env_type#還台有設置 ,不能用damain_keys來看, 有可能 業務後台增加, damain_keys沒有

                status = domain_url[0][6]
                if status == 0:
                    status = '上架'
                else:
                    status = '下架/導往百度'
                
                data = {"網域名":domain,'環境':env_type,'後台是否有設置該網域':domain_admin,'後台設定連結': admin_url,
                '後台設定待理': agent,'後台註冊開關':register_display, '後台掃碼開關':app_display,'後台設定狀態':status}
            else:# 就走預設的設定
                try:
                    if domain_keys[domain][1] != int(env):
                        return("該環境沒有此domain")
                    domain_admin = '否'
                    admin_url = '無'#後台沒設置
                    url = domain_keys[domain][0]# 沒設定 ,為空, 走預設連結
                    register_status = domain_keys[domain][2]
                    env_type = domain_keys[domain][3] +"/"+env_type#後台沒設置, 就從domain_keys 原本 預設的規則走
                except KeyError:
                    return('沒有該連結')
                
                data = {"網域名":domain,'環境':env_type,'後台是否有設置該網域':domain_admin,'預設連結':url,
                '預設註冊按紐':register_status}
            len_data = [0]# 查詢網域名 ,長度只會為 1
        try:
            frame = pd.DataFrame(data,index=len_data)
            print(frame)
            return frame.to_html()
        except ValueError:
            return('DATA有錯誤')
    return render_template('url_token.html')
@app.route('/sun_user2',methods=["POST"])
def sun_user2():# 查詢太陽成 指定domain
    if request.method == 'POST':
        env = request.form.get('env_type')
        domain = request.form.get('domain_type')
        print(env,domain)
        AutoTest.Joy188Test.select_sunuser(AutoTest.Joy188Test.get_conn(int(env)),'',2,domain)
        sun_user = AutoTest.sun_user
        print(sun_user)
        
        data = {'域名':[sun_user[i][0] for i in sun_user.keys()],
        '代理':[sun_user[i][1] for i in sun_user.keys()],
        '連結':[sun_user[i][2] for i in sun_user.keys()],
        '註冊顯示':['是' if sun_user[i][3] == 1 else "否" for i in sun_user.keys()],
        '狀態':['下架' if sun_user[i][4] == 1 else '正常' for i in sun_user.keys()],
        '備註':[sun_user[i][5] for i in sun_user.keys()],
        '連結失效性':['失效' if sun_user[i][6]!= -1 else '正常' for i in sun_user.keys()],
        '註冊數量':['0' if sun_user[i][7] == None else int(sun_user[i][7]) for i in sun_user.keys()]
        }
        frame = pd.DataFrame(data,index=[i for i in sun_user.keys()])
        print(frame)
        return frame.to_html()
    else:
        return('錯誤')
@app.route('/sun_user',methods=["POST","GET"])
def sun_user():# 太陽成用戶 找尋
    if request.method =="POST":
        user = request.form.get('user')
        env = request.form.get('env_type')
        domain = request.form.get('domain_type')
        print(user,env,domain)
        if env =='0' :
            env_name = 'dev'
        elif env == '1':
            env_name = '188'
        else:
            print(env)
            env_name = '生產'
        if domain == '0':
            domain_type = '太陽城'
        else:
            domain_type = '申博'# domain  = "1"
        if user in [None,'']:
            type_ = 1# 頁面查詢 轉移成功用戶, 
        else:
            type_ = ''# 查詢 指定用戶
        print(type_)
        AutoTest.Joy188Test.select_sunuser(AutoTest.Joy188Test.get_conn(int(env)),user,type_,domain)# 太陽/申博用戶 
        sun_user = AutoTest.sun_user
        print(sun_user)
        if len(sun_user) == 0:
            if type_ ==1:
                return('目前還沒有成功轉移用戶')
            return('%s沒有該用戶:%s'%(env_name+domain_type,user))
        if type_!=1:# 指定用戶
            user = sun_user[0][0]
            phone = sun_user[0][1]
            tran_statu = sun_user[0][4]
            if tran_statu == 1:
                tran_statu = '成功'
            else:
                tran_statu = '未完成'
            tran_time = sun_user[0][5]
            index_len = [0]
            AutoTest.Joy188Test.select_userid(AutoTest.Joy188Test.get_conn(int(env)),user,int(domain))# 4.0 資料庫
            userid = AutoTest.userid
            '''
            if len(userid) == 0:# 代表該4.0環境沒有該用戶
                FF_memo = '無'
            else:
                FF_memo = '有'
            '''
            data = {'環境/類型':env_name+domain_type,'用戶名':user,'電話號碼':phone,'轉移狀態':tran_statu,'轉移時間':tran_time,
            #'4.0資料庫':FF_memo
            }
        else:# 找尋以轉移用戶, 資料會很多筆
            user = []
            phone = []
            tran_statu = []
            tran_time = []
            index_len = []
            for num in sun_user.keys():
                user.append(sun_user[num][0])
                phone.append(sun_user[num][1])
                if sun_user[num][2] == 1:
                    statu = '成功'
                else: 
                    statu = '失敗'
                tran_statu.append(statu)
                tran_time.append(sun_user[num][3])
                index_len.append(num)
            data = {'環境/類型':env_name+domain_type,'用戶名':user,'電話號碼':phone,'轉移狀態':tran_statu,'轉移時間':tran_time}
        frame = pd.DataFrame(data,index=index_len)
        print(frame)
        return frame.to_html()
    return render_template('sun_user.html')
@app.route('/fund_activity',methods=["POST","GEt"])
def fund_activity():# 充值紅包 查詢
    if request.method =="POST":
        user = request.form.get('user')
        env = request.form.get('env_type')
        print(user,env)
        AutoTest.Joy188Test.select_userid(AutoTest.Joy188Test.get_conn(int(env)),user,'')# 查詢頁面上 該環境是否有這用戶
        if len(AutoTest.userid) == 0:
            return('該環境沒有此用戶')
        AutoTest.Joy188Test.select_FundRed(AutoTest.Joy188Test.get_conn(int(env)),user,'')# 先確認 是否領取過紅包
        red_able = AutoTest.fund_
        print(red_able)
         
        fund_list = []# 存放各充值表的 紀錄 ,總共四個表
        for i in range(4):
            AutoTest.Joy188Test.select_FundRed(AutoTest.Joy188Test.get_conn(int(env)),user,i)
            fund_list.append(AutoTest.fund_)
        #begin_mission = AutoTest.fund_# 新守任務表
        print(fund_list)
        data = {}
        fund_log = 0# 紀錄 是否 四個表都沒有資料
        for index,i in enumerate(fund_list):
            if index == 0:
                msg = '新守任務/BEGIN_MISSION'
            elif index ==1:
                msg = ('活動/ACTIVITY_FUND_OPEN_RECORD')
            elif index ==2:
                msg = ('資金明細/fund_change_log')
            elif index==3:
                msg = ('資金明細搬動/fund_change_log_hist')
            if len(i) ==0:
                msg2 = ('無紀錄')
            else:
                msg2 = ('%s'%i[0])
                fund_log = fund_log+1#
            print(msg,msg2)
            data[msg] = msg2
        if len(red_able) == 0:# 紅包還沒領取
            red_able = '否' 
            if fund_log == 0:# 代表沒成功
                activity_able = '符合資格'
            else:
                activity_able = "不符合資格"
        else:# 代表已經領取過 紅包
            red_able = float(red_able[0][0]/10000)
            activity_able = "符合資格"
        data['紅包是否領取'] = '紅包金:%s'%red_able
        data['充直紅包活動'] = activity_able
        print(data)
        frame = pd.DataFrame(data,index=[0])
        print(frame)
        return frame.to_html()
    return render_template('fund_activity.html')


@app.route('/error')#錯誤處理
def error():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    print(error)
    return render_template('404.html'), 500


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    error_dict = {
        'code': error.code,
        'description': error.description,
        'stack_trace': traceback.format_exc()
    }
    log_msg = f"HTTPException {error_dict.code}, Description: {error_dict.description}, Stack trace: {error_dict.stack_trace}"
    logger.log(msg=log_msg)
    response = jsonify(error_dict)
    response.status_code = error.code
    return response


'''
@celery.task()
def test_fun():
    for _ in range(10000):
        for j in range(50000):
            i = 1
    print('hello')
'''

if __name__ == "__main__":
    '''
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    '''
    app.config['TESTING'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(host="0.0.0.0", debug=True, port=4444, threaded=True)
    # app.config.from_object(DevConfig)
