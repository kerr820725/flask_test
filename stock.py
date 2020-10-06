import pymysql as p
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime,time
import requests,urllib3
from bs4 import BeautifulSoup
import pandas_datareader as pdr
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import twstock
import os 
import talib
import mpl_finance as mpf
import seaborn as sns
#from fbprophet import Prophet

def kerr_conn(): # 本機Mysql 連線
    db = p.connect(
    host="127.0.0.1",
    user="root",
    passwd="password",
    database="STOCK_TEST",
    use_unicode=True,
    charset="utf8"
    )
    return db
def kerr_update2(db):# 找出對應號碼, update股價
    cur = db.cursor()
    for num in range(len(stock_Name)):
        sql = "UPDATE STOCK_TEST SET STOCK_CUR_MONREV = %s,STOCK_LAST_MONREV=%s,STOCK_LAST_YEARMONREV=%s, \
        STOCK_LAST_MONRATE=%s ,STOCK_LAST_YEARMONRATE=%s,STOCK_CUR_YEARREV=%s ,STOCK_LAST_YEARREV=%s ,\
        STOCK_YEARRATE=%s  ,STOCK_MEMO ='%s'  \
        WHERE STOCK_NUM = %s"%(stock_Name[num][3],stock_Name[num][4],stock_Name[num][5],stock_Name[num][6],
        stock_Name[num][7],stock_Name[num][8],stock_Name[num][9],stock_Name[num][10],stock_Name[num][11],
        stock_Name[num][1])
        print(sql)
        cur.execute(sql)
    db.commit()
    print("update完成")
    cur.close()

def stock_selectnum(db,stock_num):#找出股號, 然後傳到 twstock, 找出股價
    cur = db.cursor()
    sql = "SELECT * from STOCK_TEST where STOCK_NUM = %s"%stock_num
    cur.execute(sql)
    global stock_detail2
    stock_detail2 = {}
    rows = cur.fetchall()
    for tuple_ in rows:
        stock_detail2[stock_num] = list(tuple_)
    cur.close()

def stock_selectname(db,stock_name):#用名稱找出, 然後傳到 twstock, 找出股價
    cur = db.cursor()
    sql = "SELECT * from STOCK_TEST where STOCK_NAME = '%s'"%stock_name
    print(sql)
    cur.execute(sql)
    global stock_detail2
    stock_detail2 = {}
    rows = cur.fetchall()
    for tuple_ in rows:
        stock_detail2[stock_name] = list(tuple_)
    cur.close()

def stock_update(db,stock_prize,stock_num):# 找出對應號碼, update股價
    cur = db.cursor()
    sql = "UPDATE STOCK_TEST SET STOCK_Latest_Prize = %s  WHERE STOCK_NUM = %s"%(stock_prize,stock_num)
    cur.execute(sql)
    db.commit()
    print("%s update完成"%stock_num)
    cur.close()
def stock_select2(db,name):#頁面  營收 勾選
    cur = db.cursor()
    if len(name) ==1:# 頁面只有勾一個 
        sql = "select * from STOCK_TEST where %s > 100 order by %s  desc"%(name[0],name[0])
    else:#先pass,後續 用 tuple方式  來加參數
        sql = "select * from STOCK_TEST where %s > 100 \
        and %s >100"%tuple(name)
    cur.execute(sql)
    rows = cur.fetchall()
    global stock_detail3
    stock_detail3 = {}
    for num,tuple_ in enumerate(rows):
        stock_detail3[num] = list(tuple_)
    print(stock_detail3)
    cur.close()
def stock_search3(db):#法人篩選 ,- 法人 連續 買 
    cur= db.cursor()
    sql = "select  count(*),STOCK_TEST.STOCK_NAME,sum(STOCK_GOV.GOV_SELL) as sell \
    ,STOCK_TEST.STOCK_LAST_MONRATE \
    from STOCK_GOV inner join STOCK_TEST on STOCK_GOV.STOCK_NUM = STOCK_TEST.STOCK_NUM \
    where STOCK_GOV.GOV_SELL > 0 \
    group by STOCK_TEST.STOCK_NAME,STOCK_TEST.STOCK_LAST_MONRATE having count(*) >=5 \
    order by count(*) desc ,sell desc"
    cur.execute(sql)
    rows = cur.fetchall()
    global stock_detail3
    stock_detail3 = {}
    for num,tuple_ in enumerate(rows):
        stock_detail3[num] = list(tuple_)
    print(stock_detail3)
    cur.close()






def df_test(number):# 將股號傳回. 透過yahoo 回傳歷史股價, 並存圖
    plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    
    global now#現在時間
    now = datetime.datetime.now()# 獲取當下時間. 用來獲得最新股票價位用
    weekday = datetime.date.today().weekday()+1#現在時間 :周, 需加1 , 禮拜一為0
    if weekday == 6:
        now_day = now.day-1
    elif weekday ==7:
        now_day = now.day-2
    else:
        now_day = now.day
    print(weekday,now_day)
    now_date = datetime.datetime(now.year,now.month,now_day)#年月日
    df = pdr.DataReader(number+'.TW','yahoo',start=now_date)
    print(df)
    global latest_close,latest_open,latest_high,latest_low,latest_volume
    latest_close = round(df['Close'][0],2)#小數點後兩位移除,收盤
    latest_open = round(df['Open'][0],2)
    latest_high = round(df['High'][0],2)
    latest_low = round(df['Low'][0],2)
    latest_volume = df['Volume'][0]# 最新的量 ,不用小數點 

    global df_#回傳給test_forecast 預測方法用
    history = datetime.datetime(2018,1,1)
    df_ = pdr.DataReader(number+'.TW','yahoo',start=history)# 歷史股架
    
    plt.title(twstock.codes[number][2])
    
    plt.style.use('ggplot')
    close = df_['Adj Close']# adj_close 是 收盤參數 ,  後續可以使用 Volume 量 參數
    plt.ylabel('股價')

    volume = df_['Volume']
    close.plot(figsize=(10,8))
    path=os.path.abspath('.')
    path_img = ".\static\image\\%s.jpg"%number#path_img 為 圖片路竟
    print(path_img)
    if os.path.isfile(path_img):# 存在就先刪掉, 再存新的
        print('%s已存在,需刪除原本'%path_img) 
        os.remove(path_img)
        
    plt.savefig(path_img)
    plt.close()
    #print(test)
def df_test2(number):
    plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    plt.style.use('ggplot')
    start = datetime.datetime(2020,1,1)
    df_2330 = pdr.DataReader('%s.TW'%number, 'yahoo', start=start)
    df_2330.index = df_2330.index.format(formatter=lambda x: x.strftime('%Y-%m-%d')) 
    #plt.style.use('ggplot')
    fig = plt.figure(figsize=(24, 15))

    #ax = fig.add_subplot(1, 1, 1)
    ax = fig.add_axes([0,0.2,1,0.5])
    ax2 = fig.add_axes([0,0,1,0.2])
    ax.set_xticks(range(0, len(df_2330.index), 100))
    ax.set_xticklabels(df_2330.index[::100])#10唯一循環
    mpf.candlestick2_ochl(ax, df_2330['Open'], df_2330['Close'], df_2330['High'],
    df_2330['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75); 

    sma_10 = talib.SMA(np.array(df_2330['Close']), 10)
    sma_30 = talib.SMA(np.array(df_2330['Close']), 30)

    plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] 
    ax.plot(sma_10, label='10日均線')
    ax.plot(sma_30, label='30日均線')

    mpf.volume_overlay(ax2, df_2330['Open'], df_2330['Close'], df_2330['Volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)
    ax2.set_xticks(range(0, len(df_2330.index), 10))
    ax2.set_xticklabels(df_2330.index[::10])
    ax.legend()


    path_img = ".\static\image\\%s_test.jpg"%number#path_img 為 圖片路竟
    print(path_img)

    plt.savefig(path_img)
    plt.close()

def test_forecast():#預測走向,和實際對比
    new_df_ = pd.DataFrame(df_['Adj Close']).reset_index().rename(columns={'Date':'ds', 'Adj Close':'y'})
    new_df_['y'] = np.log(new_df_['y'])
    # 定義模型
    model = Prophet()

    # 訓練模型
    model.fit(new_df_)

    # 建構預測集
    future = model.make_future_dataframe(periods=365) #forecasting for 1 year from now.

    # 進行預測
    forecast = model.predict(future)

    figure=model.plot(forecast)

    df_close = pd.DataFrame(df_['Adj Close'])
    two_years = forecast.set_index('ds').join(df_close)

    two_years = two_years[['Adj Close','yhat','yhat_upper','yhat_lower']].dropna().tail(8000)
    two_years['yhat']=np.exp(two_years.yhat)
    two_years['yhat_upper']=np.exp(two_years.yhat_upper)
    two_years['yhat_lower']=np.exp(two_years.yhat_lower)
    two_years[['Adj Close','yhat']].plot(figsize=(10,6))
    plt.xlabel('日期')
    plt.ylabel('股價')




def soup_stock():# 抓取數據 , len_index  為抓到的東西 , date 為時間 ,格式 109_3
    now = datetime.datetime.now()
    print("執行時間: %s"%now)
    userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    urllib3.disable_warnings()#解決 會跳出 request InsecureRequestWarning問題
    header = {
            'User-Agent': userAgent,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
        }
    session = requests.Session()
    now = datetime.datetime.now()#年找出今年.  月和日做參數化.因為可能會找先前日棋
    year = now.year -1911# 換算民國
    month = now.month -1#抓上個月
    print('開始抓取營收')
    print("抓取%s月"%month)# 當月
    r = session.get('https://mops.twse.com.tw'+'/nas/t21/sii/t21sc03_%s_%s_0.html'
    %(year,month),headers=header,verify=False)
    r.encoding = 'Big5' #繁體編碼
    soup = BeautifulSoup(r.text,'lxml')
    #soup.encode('gb18030')
    #global len_index
    len_index = [i for i in soup.find_all('tr',{'align':'right'})]
    #print(len(len_index))
    global stock_Name
    stock_Name = [] #存放所有抓到的資訊
    stock_list =[]
    for number in range(len(len_index)-1):#先取出多少長度, -1 用意, 最後一行不是抓股資訊
        stock_list.append(number)# mysql 的 ID 欄位
        for text in len_index[number]:#再從len_index陣列,取出 每個index的資訊
            stock_list.append('0' if text.text.strip() in ['','合計']#strip()把空白部分去除
            else text.text.strip().replace(',',''))
        if stock_list[-1] == '0':#過濾 不是股票名稱的 
            pass
        else:
            for num,text in enumerate(stock_list):# 需判斷 各 欄位 型態, 因為要Inser進去 Mysql, 型態需和mysql 欄位一致
                if num in [0,1]:
                    text = int(text)
                elif num in [2,11]:
                    text = str(text)
                elif num in [6,7,10]:
                    text = float(text)
                else:
                    text = int(text)
                stock_list[num] = text
        if len(stock_list) != 12:# 這邊代表 抓到的 不是股名 那行,可能是 合計
            pass
        else:
            stock_Name.append(tuple(stock_list))# 轉成tuple用意 ,好insert資料進mysql
        stock_list= []
    print(len(stock_Name))
    kerr_update2(kerr_conn())# upadte資料
def schedule():
    scheduler = BlockingScheduler()    
    scheduler.add_job(soup_stock,'interval',days=1, start_date= time.strftime('%Y-%m-05 00:00:00'),end_date= time.strftime('%Y-%m-15 00:00:00'))
    scheduler.start()
def test_job():
    print("%s: 执行任务"  % time.asctime())
def test_sche():
    scheduler = BlockingScheduler()
    scheduler.add_job(test_job, 'interval', seconds=3)
    scheduler.start()