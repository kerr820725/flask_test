game_default = '{"lotteryType":"","currIssueNo":"","stopOnWon":"","totalAmount":"",' \
               '"issueList":[],"schemeList":[],"timeZone":"GMT+8","isWap":false,"online":true}'
_iapi_default = '{"callType":"","content":{"passwd":"","account":"","uuid":""},' \
                '"clientInfo":{"appType":"teemo","clientType":"android","clientVersion":"3.0.0"},' \
                '"timeZone":"Asia/Taipei"}'

link_default = '{"rebateList": ' \
               '[{"lotteryType": "ssc","playType": "lmp","rebatePercent": "r_percent","bonusGroup": 1900},' \
               '{"lotteryType": "ssc","playType": "normal","rebatePercent": "r_percent","bonusGroup": 1800},' \
               '{"lotteryType": "k3","playType": "lmp","rebatePercent": "r_percent","bonusGroup": 1900},' \
               '{"lotteryType": "k3","playType": "normal","rebatePercent": "r_percent","bonusGroup": 1700},' \
               '{"lotteryType": "syxw","playType": "lmp","rebatePercent": "r_percent","bonusGroup": 1900},' \
               '{"lotteryType": "syxw","playType": "normal","rebatePercent": "r_percent","bonusGroup": 1800},' \
               '{"lotteryType": "sdpl35","playType": "lmp","rebatePercent": "r_percent","bonusGroup": 1900},' \
               '{"lotteryType": "sdpl35","playType": "normal","rebatePercent": "r_percent","bonusGroup": 1700},' \
               '{"lotteryType": "pk10","playType": "normal","rebatePercent": "r_percent","bonusGroup": 1900},' \
               '{"lotteryType": "pk10","playType": "lmp","rebatePercent": "r_percent","bonusGroup": 1900},' \
               '{"lotteryType": "kl8","playType": "normal","rebatePercent": "0","bonusGroup": 1700},' \
               '{"lotteryType": "kl8","playType": "lmp","rebatePercent": "r_percent","bonusGroup": 1900},' \
               '{"lotteryType": "lhc","playType": "normal","rebatePercent": "r_percent","bonusGroup": 1800},' \
               '{"lotteryType": "lhc","playType": "lmp","rebatePercent": "r_percent","bonusGroup": 1900}],' \
               '"type": "a","timeZone": "GMT+8","isWap": false,"online": true}'

game_dict = {
    """時時彩系列"""
    # 兩面
    'pt136bt02': [
        {"playType": "pt136", "betType": "bt02", "betItem": "1234567#1234#1234#1234#1234#1234#12345#12345#12345",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 84],
    # 牛牛
    'pt137bt02': [
        {"playType": "pt137", "betType": "bt02",
         "betItem": "0,1@1,1#1,2,3,4@1,1,1,1#0,1,2,3,4,5,6,7,8,9@1,1,1,1,1,1,1,1,1,1", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 16],
    # 五星複式
    'pt100bt02': [
        {"playType": "pt100", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 200000],
    # 五星單式
    'pt100bt01': [
        {"playType": "pt100", "betType": "bt01", "betItem": "12345", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 五星組合
    'pt100bt04': [
        {"playType": "pt100", "betType": "bt04", "betItem": "0123456789#0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        1000000],
    # 五星組選120
    'pt101bt23': [
        {"playType": "pt101", "betType": "bt23", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        504],
    # 五星組選60
    'pt101bt24': [
        {"playType": "pt101", "betType": "bt24", "betItem": "0123456789@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        1680],
    # 五星組選60
    'pt101bt25': [
        {"playType": "pt101", "betType": "bt25", "betItem": "0123456789@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        720],
    # 五星組選20
    'pt101bt26': [
        {"playType": "pt101", "betType": "bt26", "betItem": "0123456789@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        720],
    # 五星組選10
    'pt101bt27': [
        {"playType": "pt101", "betType": "bt27", "betItem": "0123456789@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],
    # 五星組選5
    'pt101bt28': [
        {"playType": "pt101", "betType": "bt28", "betItem": "0123456789@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],
    # 一帆風順
    'pt102bt02': [
        {"playType": "pt102", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 好事成双
    'pt103bt02': [
        {"playType": "pt103", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 三星报喜
    'pt104bt02': [
        {"playType": "pt104", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 四季发财
    'pt105bt02': [
        {"playType": "pt105", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 四星複式
    'pt106bt02': [
        {"playType": "pt106", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        20000],
    # 四星單式
    'pt106bt01': [
        {"playType": "pt106", "betType": "bt01", "betItem": "1234", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 四星組合
    'pt106bt04': [
        {"playType": "pt106", "betType": "bt04", "betItem": "0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        80000],
    # 四星組選24
    'pt107bt29': [
        {"playType": "pt107", "betType": "bt29", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        420],
    # 四星組選12
    'pt107bt30': [
        {"playType": "pt107", "betType": "bt30", "betItem": "0123456789@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        720],
    # 四星組選6
    'pt107bt31': [
        {"playType": "pt107", "betType": "bt31", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 四星組選4
    'pt107bt32': [
        {"playType": "pt107", "betType": "bt32", "betItem": "0123456789@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],
    # 前三複式
    'pt108bt02': [
        {"playType": "pt108", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        2000],
    # 前三單式
    'pt108bt01': [
        {"playType": "pt108", "betType": "bt01", "betItem": "123", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 前三組合
    'pt108bt04': [
        {"playType": "pt108", "betType": "bt04", "betItem": "0123456789#0123456789#0123456789", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        6000],
    # 前三和值
    'pt108bt05': [
        {"playType": "pt108", "betType": "bt05",
         "betItem": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        2000],
    # 前三跨度
    'pt108bt06': [
        {"playType": "pt108", "betType": "bt06", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        2000],
    # 前三組三複式
    'pt109bt20': [
        {"playType": "pt109", "betType": "bt20", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],
    # 前三組六複式
    'pt109bt21': [
        {"playType": "pt109", "betType": "bt21", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        240],
    # 前三組選單式
    'pt109bt22': [
        {"playType": "pt109", "betType": "bt22", "betItem": "123", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 前三組選包膽
    'pt109bt07': [
        {"playType": "pt109", "betType": "bt07", "betItem": "0", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        108],
    # 前三組選和值
    'pt109bt05': [
        {"playType": "pt109", "betType": "bt05",
         "betItem": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        420],

    # 中三複式
    'pt110bt02': [
        {"playType": "pt110", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        2000],
    # 中三單式
    'pt110bt01': [
        {"playType": "pt110", "betType": "bt01", "betItem": "123", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 中三組合
    'pt110bt04': [
        {"playType": "pt110", "betType": "bt04", "betItem": "0123456789#0123456789#0123456789", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        6000],
    # 中三和值
    'pt110bt05': [
        {"playType": "pt110", "betType": "bt05",
         "betItem": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        2000],
    # 中三跨度
    'pt110bt06': [
        {"playType": "pt110", "betType": "bt06", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        2000],
    # 中三組三複式
    'pt111bt20': [
        {"playType": "pt111", "betType": "bt20", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],
    # 中三組六複式
    'pt111bt21': [
        {"playType": "pt111", "betType": "bt21", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        240],
    # 中三組選單式
    'pt111bt22': [
        {"playType": "pt111", "betType": "bt22", "betItem": "123", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 中三組選包膽
    'pt111bt07': [
        {"playType": "pt111", "betType": "bt07", "betItem": "0", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        108],
    # 中三組選和值
    'pt111bt05': [
        {"playType": "pt111", "betType": "bt05",
         "betItem": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        420],

    # 後三複式
    'pt112bt02': [
        {"playType": "pt112", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        2000],
    # 後三單式
    'pt112bt01': [
        {"playType": "pt112", "betType": "bt01", "betItem": "123", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 後三組合
    'pt112bt04': [
        {"playType": "pt112", "betType": "bt04", "betItem": "0123456789#0123456789#0123456789", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        6000],
    # 後三和值
    'pt112bt05': [
        {"playType": "pt112", "betType": "bt05",
         "betItem": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        2000],
    # 後三跨度
    'pt112bt06': [
        {"playType": "pt112", "betType": "bt06", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        2000],
    # 後三組三複式
    'pt113bt20': [
        {"playType": "pt113", "betType": "bt20", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],
    # 後三組六複式
    'pt113bt21': [
        {"playType": "pt113", "betType": "bt21", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        240],
    # 後三組選單式
    'pt113bt22': [
        {"playType": "pt113", "betType": "bt22", "betItem": "123", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 後三組選包膽
    'pt113bt07': [
        {"playType": "pt113", "betType": "bt07", "betItem": "0", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        108],
    # 後三組選和值
    'pt113bt05': [
        {"playType": "pt113", "betType": "bt05",
         "betItem": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        420],

    # 前二直選複式
    'pt114bt02': [
        {"playType": "pt114", "betType": "bt02", "betItem": "0123456789#0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        200],
    # 前二直選單式
    'pt114bt01': [
        {"playType": "pt114", "betType": "bt01", "betItem": "12", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 前二直選和值
    'pt114bt05': [
        {"playType": "pt114", "betType": "bt05", "betItem": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        196],
    # 前二直選跨度
    'pt114bt06': [
        {"playType": "pt114", "betType": "bt06", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        200],
    # 前二組選複式
    'pt115bt02': [
        {"playType": "pt115", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 前二組選單式
    'pt115bt01': [
        {"playType": "pt115", "betType": "bt01", "betItem": "12", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 前二組選和值
    'pt115bt05': [
        {"playType": "pt115", "betType": "bt05", "betItem": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        90],
    # 前二組選包膽
    'pt115bt07': [
        {"playType": "pt115", "betType": "bt07", "betItem": "0", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        18],

    # 後二直選複式
    'pt116bt02': [
        {"playType": "pt116", "betType": "bt02", "betItem": "0123456789#0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        200],
    # 後二直選單式
    'pt116bt01': [
        {"playType": "pt116", "betType": "bt01", "betItem": "12", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 後二直選和值
    'pt116bt05': [
        {"playType": "pt116", "betType": "bt05", "betItem": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        196],
    # 後二直選跨度
    'pt116bt06': [
        {"playType": "pt116", "betType": "bt06", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        200],
    # 後二組選複式
    'pt117bt02': [
        {"playType": "pt117", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 後二組選單式
    'pt117bt01': [
        {"playType": "pt117", "betType": "bt01", "betItem": "12", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 後二組選和值
    'pt117bt05': [
        {"playType": "pt117", "betType": "bt05", "betItem": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        90],
    # 後二組選包膽
    'pt117bt07': [
        {"playType": "pt117", "betType": "bt07", "betItem": "0", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        18],

    # 定位膽
    'pt118bt02': [
        {"playType": "pt118", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        100],
    # 前三一码不定位
    'pt119bt02': [
        {"playType": "pt119", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 前三二码不定位
    'pt120bt02': [
        {"playType": "pt120", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 中三一码不定位
    'pt121bt02': [
        {"playType": "pt121", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 中三二码不定位
    'pt122bt02': [
        {"playType": "pt122", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 後三一码不定位
    'pt123bt02': [
        {"playType": "pt123", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 後三二码不定位
    'pt124bt02': [
        {"playType": "pt124", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 後四一码不定位
    'pt125bt02': [
        {"playType": "pt125", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        20],
    # 後四二码不定位
    'pt126bt02': [
        {"playType": "pt126", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 五星二码不定位
    'pt127bt02': [
        {"playType": "pt127", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 五星三码不定位
    'pt128bt02': [
        {"playType": "pt128", "betType": "bt02", "betItem": "0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        240],

    # 任二直選複式
    'pt130bt02': [
        {"playType": "pt130", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2000],
    # 任二直選單式
    'pt130bt01': [
        {"playType": "pt130", "betType": "bt01", "betItem": "45@01,02", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        4],
    # 任二直選和值
    'pt130bt05': [
        {"playType": "pt130", "betType": "bt05", "betItem": "45@0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        200],
    # 任二組選複式
    'pt131bt02': [
        {"playType": "pt131", "betType": "bt02", "betItem": "45@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 任二組選單式
    'pt131bt01': [
        {"playType": "pt131", "betType": "bt01", "betItem": "45@12", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 任二組選和值
    'pt131bt05': [
        {"playType": "pt131", "betType": "bt05", "betItem": "45@1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        90],
    # 任三直選複式
    'pt132bt02': [
        {"playType": "pt132", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        20000],
    # 任三直選單式
    'pt132bt01': [
        {"playType": "pt132", "betType": "bt01", "betItem": "345@123", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        2],
    # 任三直選和值
    'pt132bt05': [
        {"playType": "pt132", "betType": "bt05",
         "betItem": "345@0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        2000],
    # 任三组三复式
    'pt133bt20': [
        {"playType": "pt133", "betType": "bt20", "betItem": "345@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],
    # 任三组六复式
    'pt133bt21': [
        {"playType": "pt133", "betType": "bt21", "betItem": "345@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        240],
    # 任三组選單式
    'pt133bt22': [
        {"playType": "pt133", "betType": "bt22", "betItem": "345@123,112", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        4],
    # 任三组選單式
    'pt133bt05': [
        {"playType": "pt133", "betType": "bt05",
         "betItem": "345@1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"},
        420],

    # 任四直選複式
    'pt134bt02': [
        {"playType": "pt134", "betType": "bt02", "betItem": "0123456789#0123456789#0123456789#0123456789#0123456789",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        100000],
    # 任四直選單式
    'pt134bt01': [
        {"playType": "pt134", "betType": "bt01", "betItem": "2345@1234", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        2],
    # 任四組選24
    'pt135bt29': [
        {"playType": "pt135", "betType": "bt29", "betItem": "2345@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        420],
    # 任四組選12
    'pt135bt30': [
        {"playType": "pt135", "betType": "bt30", "betItem": "2345@0123456789,0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        720],
    # 任四組選6
    'pt135bt31': [
        {"playType": "pt135", "betType": "bt31", "betItem": "2345@0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        90],
    # 任四組選4
    'pt135bt32': [
        {"playType": "pt135", "betType": "bt32", "betItem": "2345@0123456789,0123456789", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"},
        180],

    """11選5系列"""
    # 前三选一不定位
    'pt200bt02': [
        {"playType": "pt200", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 22],
    # 前三选一定位
    'pt201bt02': [
        {"playType": "pt201", "betType": "bt02",
         "betItem": "01,02,03,04,05,06,07,08,09,10,11#01,02,03,04,05,06,07,08,09,10,11#01,02,03,04,05,06,07,08,09,10,11",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 66],
    # 任选一-普通
    'pt202bt02': [
        {"playType": "pt202", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 22],
    # 前二-直选普通
    'pt203bt02': [
        {"playType": "pt203", "betType": "bt02",
         "betItem": "01,02,03,04,05,06,07,08,09,10,11#01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 220],
    # 前二-直选单式
    'pt203bt01': [
        {"playType": "pt203", "betType": "bt01", "betItem": "01#02", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 前二-组选普通
    'pt204bt02': [
        {"playType": "pt204", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 110],
    # 前二-组选单式
    'pt204bt01': [
        {"playType": "pt204", "betType": "bt01", "betItem": "01,02", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 任选二-普通
    'pt205bt02': [
        {"playType": "pt205", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 110],
    # 任选二-单式
    'pt205bt01': [
        {"playType": "pt205", "betType": "bt01", "betItem": "01,02", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 前三-直选普通
    'pt206bt02': [
        {"playType": "pt206", "betType": "bt02",
         "betItem": "01,02,03,04,05,06,07,08,09,10,11#01,02,03,04,05,06,07,08,09,10,11#01,02,03,04,05,06,07,08,09,10,11",
         "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 1980],
    # 前三-直选单式
    'pt206bt01': [
        {"playType": "pt206", "betType": "bt01", "betItem": "01#02#03", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 前三-组选普通
    'pt207bt02': [
        {"playType": "pt207", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 330],
    # 前三-组选单式
    'pt207bt01': [
        {"playType": "pt207", "betType": "bt01", "betItem": "01,02,03", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 任选三-普通
    'pt208bt02': [
        {"playType": "pt208", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 330],
    # 任选三-单式
    'pt208bt01': [
        {"playType": "pt208", "betType": "bt01", "betItem": "01,02,03", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 任选四-普通
    'pt209bt02': [
        {"playType": "pt209", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 660],
    # 任选四-单式
    'pt209bt01': [
        {"playType": "pt209", "betType": "bt01", "betItem": "01,02,03,04", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 任选五-普通
    'pt210bt02': [
        {"playType": "pt210", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 924],
    # 任选五-单式
    'pt210bt01': [
        {"playType": "pt210", "betType": "bt01", "betItem": "01,02,03,04,05", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 任选六-普通
    'pt211bt02': [
        {"playType": "pt211", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 924],
    # 任选六-单式
    'pt211bt01': [
        {"playType": "pt211", "betType": "bt01", "betItem": "01,02,03,04,05,06", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 任选七-普通
    'pt212bt02': [
        {"playType": "pt212", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 660],
    # 任选七-单式
    'pt212bt01': [
        {"playType": "pt212", "betType": "bt01", "betItem": "01,02,03,04,05,06,07", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 任选八-普通
    'pt213bt02': [
        {"playType": "pt213", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10,11", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 330],
    # 任选八-单式
    'pt213bt01': [
        {"playType": "pt213", "betType": "bt01", "betItem": "01,02,03,04,05,06,07,08", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 2],
    # 兩面盤
    'pt216bt02': [
        {"playType": "pt216", "betType": "bt02",
         "betItem": "123457#1234#1234#1234#1234#1234#3456789#05,04,03,02,01,00,15,14,13,12,11,10", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 90],

    """快三系列"""
    # 和值
    'pt300bt02': [
        {"playType": "pt300", "betType": "bt02", "betItem": "3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 32],
    # 三同号通选
    'pt301bt01': [
        {"playType": "pt301", "betType": "bt01", "betItem": "777", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 三同号单选
    'pt302bt02': [
        {"playType": "pt302", "betType": "bt02", "betItem": "123456", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 12],
    # 三不同号
    'pt303bt02': [
        {"playType": "pt303", "betType": "bt02", "betItem": "123456", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 40],
    # 三连号通选
    'pt304bt01': [
        {"playType": "pt304", "betType": "bt01", "betItem": "789", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 二同号复选
    'pt305bt02': [
        {"playType": "pt305", "betType": "bt02", "betItem": "123456", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 12],
    # 二同号单选
    'pt306bt02': [
        {"playType": "pt306", "betType": "bt02", "betItem": "123@456", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 18],
    # 二不同號
    'pt307bt02': [
        {"playType": "pt307", "betType": "bt02", "betItem": "123456", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 30],
    # (快三)總和大小单双
    'pt309bt02': [
        {"playType": "pt309", "betType": "bt02", "betItem": "1234#123456", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 20],

    """PK10系列"""
    # 大小單雙龍虎
    'pt330bt02': [
        {"playType": "pt330", "betType": "bt02",
         "betItem": "123457#123457#123457#123457#123457#1234#1234#1234#1234#1234#1234", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 108],
    # 牛牛
    'pt333bt02': [[
        {"playType": "pt333", "betType": "bt02", "betItem": "5@5", "betTimes": 1, "potType": "Y", "doRebate": "no"},
        {"playType": "pt333", "betType": "bt02", "betItem": "4@5", "betTimes": 1, "potType": "Y", "doRebate": "no"},
        {"playType": "pt333", "betType": "bt02", "betItem": "3@5", "betTimes": 1, "potType": "Y", "doRebate": "no"},
        {"playType": "pt333", "betType": "bt02", "betItem": "2@5", "betTimes": 1, "potType": "Y", "doRebate": "no"},
        {"playType": "pt333", "betType": "bt02", "betItem": "1@5", "betTimes": 1, "potType": "Y", "doRebate": "no"}],
        5],
    # 冠軍
    'pt320bt02': [
        {"playType": "pt320", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10", "betTimes": 1,
         "potType": "Y", "doRebate": "yes"}, 20],
    # 冠亞直選
    'pt321bt02': [
        {"playType": "pt321", "betType": "bt02",
         "betItem": "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10", "betTimes": 1, "potType": "Y",
         "doRebate": "yes"}, 180],
    # 冠亞直選單式
    'pt321bt01': [
        {"playType": "pt321", "betType": "bt01", "betItem": "01#02", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 冠亞組選
    'pt322bt02': [{"playType": "pt322", "betType": "bt02", "betItem": "01,02,03,04,05,06,07,08,09,10", "betTimes": 1,
                   "potType": "Y", "doRebate": "yes"}, 90],
    # 冠亞組選單式
    'pt322bt01': [
        {"playType": "pt322", "betType": "bt01", "betItem": "01,02", "betTimes": 1, "potType": "Y", "doRebate": "yes"},
        2],
    # 冠亞和值
    'pt323bt02': [{"playType": "pt323", "betType": "bt02", "betItem": "3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19",
                   "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 34],
    # 前三直選
    'pt325bt02': [{"playType": "pt325", "betType": "bt02",
                   "betItem": "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10#"
                              "01,02,03,04,05,06,07,08,09,10",
                   "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 1440],
    # 前三直選單式
    'pt325bt01': [{"playType": "pt325", "betType": "bt01",
                   "betItem": "01#02#03",
                   "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 2],
    # 前四直選
    'pt326bt02': [{"playType": "pt326", "betType": "bt02",
                   "betItem": "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10#"
                              "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10",
                   "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 10080],
    # 前四直選單式
    'pt326bt01': [{"playType": "pt326", "betType": "bt01",
                   "betItem": "01#02#03#04",
                   "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 2],
    # 定位膽
    'pt327bt02': [{"playType": "pt327", "betType": "bt02",
                   "betItem": "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10#"
                              "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10#"
                              "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10#"
                              "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10#"
                              "01,02,03,04,05,06,07,08,09,10#01,02,03,04,05,06,07,08,09,10",
                   "betTimes": 1, "potType": "Y", "doRebate": "yes"}, 200]
}
