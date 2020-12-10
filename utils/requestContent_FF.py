from utils import Logger

logger = Logger.create_logger(r"\utils", 'game_dict')

award_mode = None


def get_game_dict(game_list, _award_mode: int):
    """
    依照提供的玩法搜尋頭住內容，並替換t_a_w組成 balls 參數，同時統計總投注金額供 amount 使用.
    :param game_list: array, 取自 m/gameBet/***/dynamicConfig 回傳的 [data]['gamelimit'] 的 key
    :param _award_mode: award_mode
    :return: Array[Data, amount]`
    """
    data = []
    amount = 0
    for game_name in game_list:
        if game_name in game_dict:
            temp_data = game_dict[game_name]
            temp_data["awardMode"] = _award_mode
            data.append(temp_data)
            amount += temp_data["num"] * 2
        # else:
        #     print(f'發現未支援的玩法: {game_name}')
    return [data, amount]


game_dict = {
    # 時時彩系列
    'daxiaodanshuang.dxds.houer': {"id": 106, "ball": "双,大", "type": "daxiaodanshuang.dxds.houer", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'daxiaodanshuang.dxds.houyi': {"id": 105, "ball": "小", "type": "daxiaodanshuang.dxds.houyi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'daxiaodanshuang.dxds.qianer': {"id": 104, "ball": "小,双", "type": "daxiaodanshuang.dxds.qianer", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'daxiaodanshuang.dxds.qianyi': {"id": 103, "ball": "小", "type": "daxiaodanshuang.dxds.qianyi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'daxiaodanshuang.dxds.zonghe': {"id": 102, "ball": "小", "type": "daxiaodanshuang.dxds.zonghe", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer.zhixuan.danshi': {"id": 72, "ball": "49", "type": "houer.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer.zhixuan.fushi': {"id": 71, "ball": "-,-,-,3,6", "type": "houer.zhixuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer.zhixuan.hezhi': {"id": 73, "ball": "5", "type": "houer.zhixuan.hezhi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 6},
    'houer.zhixuan.kuadu': {"id": 74, "ball": "3", "type": "houer.zhixuan.kuadu", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 14},
    'houer.zuxuan.baodan': {"id": 78, "ball": "3", "type": "houer.zuxuan.baodan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 9},
    'houer.zuxuan.danshi': {"id": 76, "ball": "57", "type": "houer.zuxuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer.zuxuan.fushi': {"id": 75, "ball": "6,9", "type": "houer.zuxuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer.zuxuan.hezhi': {"id": 77, "ball": "17", "type": "houer.zuxuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer_2000.zhixuan.danshi': {"id": 94, "ball": "65", "type": "houer_2000.zhixuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer_2000.zhixuan.fushi': {"id": 93, "ball": "-,-,-,5,9", "type": "houer_2000.zhixuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer_2000.zhixuan.hezhi': {"id": 95, "ball": "14", "type": "houer_2000.zhixuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 5},
    'houer_2000.zhixuan.kuadu': {"id": 96, "ball": "5", "type": "houer_2000.zhixuan.kuadu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 10},
    'houer_2000.zuxuan.baodan': {"id": 100, "ball": "8", "type": "houer_2000.zuxuan.baodan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 9},
    'houer_2000.zuxuan.danshi': {"id": 98, "ball": "25", "type": "houer_2000.zuxuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer_2000.zuxuan.fushi': {"id": 97, "ball": "1,8", "type": "houer_2000.zuxuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'houer_2000.zuxuan.hezhi': {"id": 99, "ball": "13", "type": "houer_2000.zuxuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 3},
    'housan.budingwei.ermabudingwei': {"id": 62, "ball": "1,2", "type": "housan.budingwei.ermabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.budingwei.yimabudingwei': {"id": 61, "ball": "5", "type": "housan.budingwei.yimabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.zhixuan.danshi': {"id": 51, "ball": "561", "type": "housan.zhixuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.zhixuan.fushi': {"id": 50, "ball": "-,-,3,6,4", "type": "housan.zhixuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.zhixuan.hezhi': {"id": 52, "ball": "9", "type": "housan.zhixuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 55},
    'housan.zhixuan.kuadu': {"id": 53, "ball": "3", "type": "housan.zhixuan.kuadu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 126},
    'housan.zuxuan.baodan': {"id": 58, "ball": "9", "type": "housan.zuxuan.baodan", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 54},
    'housan.zuxuan.hezhi': {"id": 54, "ball": "26", "type": "housan.zuxuan.hezhi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.zuxuan.hunhezuxuan': {"id": 57, "ball": "125", "type": "housan.zuxuan.hunhezuxuan", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.zuxuan.zuliu': {"id": 56, "ball": "2,3,9", "type": "housan.zuxuan.zuliu", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.zuxuan.zuliudanshi': {"id": 60, "ball": "078", "type": "housan.zuxuan.zuliudanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan.zuxuan.zusan': {"id": 55, "ball": "1,2", "type": "housan.zuxuan.zusan", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 2},
    'housan.zuxuan.zusandanshi': {"id": 59, "ball": "577", "type": "housan.zuxuan.zusandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.budingwei.ermabudingwei': {"id": 92, "ball": "2,7", "type": "housan_2000.budingwei.ermabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.budingwei.yimabudingwei': {"id": 91, "ball": "7", "type": "housan_2000.budingwei.yimabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zhixuan.danshi': {"id": 94, "ball": "65", "type": "houer_2000.zhixuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zhixuan.fushi': {"id": 93, "ball": "-,-,-,5,9", "type": "houer_2000.zhixuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zhixuan.hezhi': {"id": 95, "ball": "14", "type": "houer_2000.zhixuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 5},
    'housan_2000.zhixuan.kuadu': {"id": 96, "ball": "5", "type": "houer_2000.zhixuan.kuadu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 10},
    'housan_2000.zuxuan.baodan': {"id": 100, "ball": "8", "type": "houer_2000.zuxuan.baodan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 9},
    'housan_2000.zuxuan.hezhi': {"id": 99, "ball": "13", "type": "houer_2000.zuxuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 3},
    'housan_2000.zuxuan.danshi': {"id": 98, "ball": "25", "type": "houer_2000.zuxuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zuxuan.fushi': {"id": 97, "ball": "1,8", "type": "houer_2000.zhixuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zuxuan.hunhezuxuan': {"id": 87, "ball": "024", "type": "housan_2000.zuxuan.hunhezuxuan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zuxuan.zuliu': {"id": 86, "ball": "2,5,9", "type": "housan_2000.zuxuan.zuliu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zuxuan.zuliudanshi': {"id": 90, "ball": "047", "type": "housan_2000.zuxuan.zuliudanshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'housan_2000.zuxuan.zusan': {"id": 85, "ball": "5,9", "type": "housan_2000.zuxuan.zusan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 2},
    'housan_2000.zuxuan.zusandanshi': {"id": 89, "ball": "336", "type": "housan_2000.zuxuan.zusandanshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'longhu.longhudou.fushi': {"id": 107, "ball": "-,-,-,-,-,-,-,-,龙,-", "type": "longhu.longhudou.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'qianer.zhixuan.danshi': {"id": 16, "ball": "67", "type": "qianer.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'qianer.zhixuan.fushi': {"id": 63, "ball": "2,9,-,-,-", "type": "qianer.zhixuan.fushi", "moneyunit": "1", "multiple": 1 ,"awardMode": award_mode, "num": 1},
    'qianer.zhixuan.hezhi': {"id": 65, "ball": "13", "type": "qianer.zhixuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 6},
    'qianer.zhixuan.kuadu': {"id": 66, "ball": "4", "type": "qianer.zhixuan.kuadu", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 12},
    'qianer.zuxuan.baodan': {"id": 70, "ball": "7", "type": "qianer.zuxuan.baodan", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 9},
    'qianer.zuxuan.danshi': {"id": 68, "ball": "27", "type": "qianer.zuxuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'qianer.zuxuan.fushi': {"id": 67, "ball": "1,6", "type": "qianer.zuxuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'qianer.zuxuan.hezhi': {"id": 69, "ball": "8", "type": "qianer.zuxuan.hezhi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 4},
    'qiansan.budingwei.ermabudingwei': {"id": 36, "ball": "1,2", "type": "qiansan.budingwei.ermabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'qiansan.budingwei.yimabudingwei': {"id": 35, "ball": "5", "type": "qiansan.budingwei.yimabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'qiansan.zhixuan.danshi': {"id": 25, "ball": "037", "type": "qiansan.zhixuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'qiansan.zhixuan.fushi': {"id": 24, "ball": "9,6,9,-,-", "type": "qiansan.zhixuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'qiansan.zhixuan.hezhi': {"id": 26, "ball": "2", "type": "qiansan.zhixuan.hezhi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 6},
    'qiansan.zhixuan.kuadu': {"id": 27, "ball": "6", "type": "qiansan.zhixuan.kuadu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 144},
    'qiansan.zuxuan.baodan': {"id": 32, "ball": "9", "type": "qiansan.zuxuan.baodan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 54},
    'qiansan.zuxuan.hezhi': {"id": 28, "ball": "14", "type": "qiansan.zuxuan.hezhi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 15},
    'qiansan.zuxuan.hunhezuxuan': {"id": 31, "ball": "159", "type": "qiansan.zuxuan.hunhezuxuan", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'qiansan.zuxuan.zuliu': {"id": 30, "ball": "0,5,7", "type": "qiansan.zuxuan.zuliu", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'qiansan.zuxuan.zuliudanshi': {"id": 34, "ball": "147", "type": "qiansan.zuxuan.zuliudanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'qiansan.zuxuan.zusan': {"id": 29, "ball": "2,3", "type": "qiansan.zuxuan.zusan", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 2},
    'qiansan.zuxuan.zusandanshi': {"id": 33, "ball": "599", "type": "qiansan.zuxuan.zusandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    # # 'shuangmienpan.housan.banshun': ['],
    # # 'shuangmienpan.housan.baozi': ['],
    # # 'shuangmienpan.housan.duizi': ['],
    # # 'shuangmienpan.housan.shunzi': ['],
    # # 'shuangmienpan.housan.zaliu': ['],
    # # 'shuangmienpan.qiansan.banshun': ['],
    # # 'shuangmienpan.qiansan.baozi': ['],
    # # 'shuangmienpan.qiansan.duizi': ['],
    # # 'shuangmienpan.qiansan.shunzi': ['],
    # # 'shuangmienpan.qiansan.zaliu': ['],
    # # 'shuangmienpan.shiuanma.chiuhao': ['],
    # # 'shuangmienpan.shiuanma.danshuang': ['],
    # # 'shuangmienpan.shiuanma.daxiao': ['],
    # # 'shuangmienpan.zhongsan.banshun': ['],
    # # 'shuangmienpan.zhongsan.baozi': ['],
    # # 'shuangmienpan.zhongsan.duizi': ['],
    # # 'shuangmienpan.zhongsan.shunzi': ['],
    # # 'shuangmienpan.zhongsan.zaliu': ['],
    # # 'shuangmienpan.zonghe.danshuang': ['],
    # # 'shuangmienpan.zonghe.daxiao': ['],
    # # 'shuangmienpan.zonghe.longhuhe': ['],
    'sixing.budingwei.ermabudingwei': {"id": 23, "ball": "1,9", "type": "sixing.budingwei.ermabudingwei", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'sixing.budingwei.yimabudingwei': {"id": 22, "ball": "8", "type": "sixing.budingwei.yimabudingwei", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'sixing.zhixuan.danshi': {"id": 17, "ball": "6266", "type": "sixing.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'sixing.zhixuan.fushi': {"id": 16, "ball": "-,9,4,6,4", "type": "sixing.zhixuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'sixing.zuxuan.zuxuan12': {"id": 19, "ball": "9,04", "type": "sixing.zuxuan.zuxuan12", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'sixing.zuxuan.zuxuan24': {"id": 18, "ball": "3,4,5,8", "type": "sixing.zuxuan.zuxuan24", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'sixing.zuxuan.zuxuan4': {"id": 21, "ball": "5,0", "type": "sixing.zuxuan.zuxuan4", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'sixing.zuxuan.zuxuan6': {"id": 20, "ball": "6,7", "type": "sixing.zuxuan.zuxuan6", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.budingwei.ermabudingwei': {"id": 10, "ball": "3,7", "type": "wuxing.budingwei.ermabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.budingwei.sanmabudingwei': {"id": 11, "ball": "3,4,8", "type": "wuxing.budingwei.sanmabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.budingwei.yimabudingwei': {"id": 9, "ball": "6", "type": "wuxing.budingwei.yimabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.quwei.haoshichengshuang': {"id": 13, "ball": "7", "type": "wuxing.quwei.haoshichengshuang", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.quwei.sanxingbaoxi': {"id": 14, "ball": "8", "type": "wuxing.quwei.sanxingbaoxi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.quwei.sijifacai': {"id": 15, "ball": "8", "type": "wuxing.quwei.sijifacai", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.quwei.yifanfengshun': {"id": 12, "ball": "4", "type": "wuxing.quwei.yifanfengshun", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zhixuan.danshi': {"id": 2, "ball": "32077", "type": "wuxing.zhixuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zhixuan.fushi': {"id": 1, "ball": "1,7,1,0,6", "type": "wuxing.zhixuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zuxuan.zuxuan10': {"id": 7, "ball": "0,4", "type": "wuxing.zuxuan.zuxuan10", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zuxuan.zuxuan120': {"id": 3, "ball": "1,2,5,6,8", "type": "wuxing.zuxuan.zuxuan120", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zuxuan.zuxuan20': {"id": 6, "ball": "4,79", "type": "wuxing.zuxuan.zuxuan20", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zuxuan.zuxuan30': {"id": 5, "ball": "01,3", "type": "wuxing.zuxuan.zuxuan30", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zuxuan.zuxuan5': {"id": 8, "ball": "2,7", "type": "wuxing.zuxuan.zuxuan5", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'wuxing.zuxuan.zuxuan60': {"id": 4, "ball": "4,078", "type": "wuxing.zuxuan.zuxuan60", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'yixing.dingweidan.fushi': {"id": 79, "ball": "-,-,-,-,1", "type": "yixing.dingweidan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'yixing_2000.dingweidan.fushi': {"id": 101, "ball": "-,3,-,-,-", "type": "yixing_2000.dingweidan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.budingwei.ermabudingwei': {"id": 49, "ball": "2,4", "type": "zhongsan.budingwei.ermabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.budingwei.yimabudingwei': {"id": 48, "ball": "6", "type": "zhongsan.budingwei.yimabudingwei", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.zhixuan.danshi': {"id": 38, "ball": "402", "type": "zhongsan.zhixuan.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.zhixuan.fushi': {"id": 37, "ball": "-,5,2,4,-", "type": "zhongsan.zhixuan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.zhixuan.hezhi': {"id": 39, "ball": "17", "type": "zhongsan.zhixuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 63},
    'zhongsan.zhixuan.kuadu': {"id": 40, "ball": "7", "type": "zhongsan.zhixuan.kuadu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 126},
    'zhongsan.zuxuan.baodan': {"id": 45, "ball": "2", "type": "zhongsan.zuxuan.baodan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 54},
    'zhongsan.zuxuan.hezhi': {"id": 41, "ball": "20", "type": "zhongsan.zuxuan.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 8},
    'zhongsan.zuxuan.hunhezuxuan': {"id": 44, "ball": "018", "type": "zhongsan.zuxuan.hunhezuxuan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.zuxuan.zuliu': {"id": 43, "ball": "0,4,9", "type": "zhongsan.zuxuan.zuliu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.zuxuan.zuliudanshi': {"id": 47, "ball": "179", "type": "zhongsan.zuxuan.zuliudanshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'zhongsan.zuxuan.zusan': {"id": 42, "ball": "0,9", "type": "zhongsan.zuxuan.zusan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 2},
    'zhongsan.zuxuan.zusandanshi': {"id": 46, "ball": "002", "type": "zhongsan.zuxuan.zusandanshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    # 快三
    'erbutonghao.biaozhun.biaozhuntouzhu': {"id": 8, "ball": "2,4", "type": "erbutonghao.biaozhun.biaozhuntouzhu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    # 'erbutonghao.biaozhun.dantuotouzhu': {},
    'ertonghaodanxuan.ertonghaodanxuan.ertonghaodanxuan': {"id": 7, "ball": "11#3", "type": "ertonghaodanxuan.ertonghaodanxuan.ertonghaodanxuan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'ertonghaofuxuan.ertonghaofuxuan.ertonghaofuxuan': {"id": 6, "ball": "55*", "type": "ertonghaofuxuan.ertonghaofuxuan.ertonghaofuxuan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'hezhi.hezhi.hezhi': {"id": 1, "ball": "14", "type": "hezhi.hezhi.hezhi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'sanbutonghao.biaozhun.biaozhuntouzhu': {"id": 4, "ball": "1,2,6", "type": "sanbutonghao.biaozhun.biaozhuntouzhu", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    # 'sanbutonghao.biaozhun.dantuotouzhu': {},
    'sanlianhaotongxuan.sanlianhaotongxuan.sanlianhaotongxuan': {"id": 5, "ball": "123 234 345 456", "type": "sanlianhaotongxuan.sanlianhaotongxuan.sanlianhaotongxuan", "moneyunit": "1","multiple": 1, "awardMode": award_mode, "num": 1},
    'santonghaodanxuan.santonghaodanxuan.santonghaodanxuan': {"id": 3, "ball": "111", "type": "santonghaodanxuan.santonghaodanxuan.santonghaodanxuan", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'santonghaotongxuan.santonghaotongxuan.santonghaotongxuan': {"id": 2, "ball": "111 222 333 444 555 666", "type": "santonghaotongxuan.santonghaotongxuan.santonghaotongxuan", "moneyunit": "1","multiple": 1, "awardMode": award_mode, "num": 1},
    'yibutonghao.yibutonghao.yibutonghao': {"id": 9, "ball": "6", "type": "yibutonghao.yibutonghao.yibutonghao", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    # 115
    'quwei.normal.caizhongwei': {"id": 37, "ball": "03", "type": "quwei.normal.caizhongwei", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'quwei.normal.dingdanshuang': {"id": 36, "ball": "4单1双", "type": "quwei.normal.dingdanshuang", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanba.renxuanbazhongwu.danshi': {"id": 34, "ball": "01 03 05 06 08 09 10 11", "type": "xuanba.renxuanbazhongwu.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanba.renxuanbazhongwu.dantuo': {"id": 35, "ball": "[胆02]  01,05,06,08,09,10,11", "type": "xuanba.renxuanbazhongwu.dantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanba.renxuanbazhongwu.fushi': {"id": 33, "ball": "01,02,03,05,06,07,08,10", "type": "xuanba.renxuanbazhongwu.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.qianerzhixuan.zhixuandanshi': {"id": 6, "ball": "02 04", "type": "xuaner.qianerzhixuan.zhixuandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.qianerzhixuan.zhixuanfushi': {"id": 5, "ball": "07,02,-,-,-", "type": "xuaner.qianerzhixuan.zhixuanfushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.qianerzuxuan.zuxuandanshi': {"id": 8, "ball": "06 07", "type": "xuaner.qianerzuxuan.zuxuandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.qianerzuxuan.zuxuandantuo': {"id": 9, "ball": "[胆 01] 08", "type": "xuaner.qianerzuxuan.zuxuandantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.qianerzuxuan.zuxuanfushi': {"id": 7, "ball": "02,03", "type": "xuaner.qianerzuxuan.zuxuanfushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.renxuanerzhonger.renxuandanshi': {"id": 11, "ball": "09 10", "type": "xuaner.renxuanerzhonger.renxuandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.renxuanerzhonger.renxuandantuo': {"id": 12, "ball": "[胆 10] 09", "type": "xuaner.renxuanerzhonger.renxuandantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuaner.renxuanerzhonger.renxuanfushi': {"id": 10, "ball": "02,06", "type": "xuaner.renxuanerzhonger.renxuanfushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanliu.renxuanliuzhongwu.danshi': {"id": 28, "ball": "01 04 05 07 09 10", "type": "xuanliu.renxuanliuzhongwu.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanliu.renxuanliuzhongwu.dantuo': {"id": 29, "ball": "[胆10]  01,03,06,08,09", "type": "xuanliu.renxuanliuzhongwu.dantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanliu.renxuanliuzhongwu.fushi': {"id": 27, "ball": "01,03,05,06,09,10", "type": "xuanliu.renxuanliuzhongwu.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanqi.renxuanqizhongwu.danshi': {"id": 31, "ball": "01 02 04 05 06 10 11", "type": "xuanqi.renxuanqizhongwu.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanqi.renxuanqizhongwu.dantuo': {"id": 32, "ball": "[胆01]  04,05,08,09,10,11", "type": "xuanqi.renxuanqizhongwu.dantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanqi.renxuanqizhongwu.fushi': {"id": 30, "ball": "02,03,06,08,09,10,11", "type": "xuanqi.renxuanqizhongwu.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.qiansanzhixuan.zhixuandanshi': {"id": 14, "ball": "08 09 06", "type": "xuansan.qiansanzhixuan.zhixuandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.qiansanzhixuan.zhixuanfushi': {"id": 13, "ball": "10,01,02,-,-", "type": "xuansan.qiansanzhixuan.zhixuanfushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.qiansanzuxuan.zuxuandanshi': {"id": 16, "ball": "01 04 09", "type": "xuansan.qiansanzuxuan.zuxuandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.qiansanzuxuan.zuxuandantuo': {"id": 17, "ball": "[胆02]  06,08", "type": "xuansan.qiansanzuxuan.zuxuandantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.qiansanzuxuan.zuxuanfushi': {"id": 15, "ball": "03,08,09", "type": "xuansan.qiansanzuxuan.zuxuanfushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.renxuansanzhongsan.renxuandanshi': {"id": 19, "ball": "01 07 08", "type": "xuansan.renxuansanzhongsan.renxuandanshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.renxuansanzhongsan.renxuandantuo': {"id": 20, "ball": "[胆02]  01,11", "type":  "xuansan.renxuansanzhongsan.renxuandantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansan.renxuansanzhongsan.renxuanfushi': {"id": 18, "ball": "02,05,10", "type": "xuansan.renxuansanzhongsan.renxuanfushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansi.renxuansizhongsi.danshi': {"id": 22, "ball": "03 07 08 10", "type": "xuansi.renxuansizhongsi.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansi.renxuansizhongsi.dantuo': {"id": 23, "ball": "[胆10]  03,08,09", "type": "xuansi.renxuansizhongsi.dantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuansi.renxuansizhongsi.fushi': {"id": 21, "ball": "02,03,04,06", "type": "xuansi.renxuansizhongsi.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanwu.renxuanwuzhongwu.danshi': {"id": 25, "ball": "01 03 06 07 09", "type": "xuanwu.renxuanwuzhongwu.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanwu.renxuanwuzhongwu.dantuo': {"id": 26, "ball": "[胆10]  01,05,07,11", "type": "xuanwu.renxuanwuzhongwu.dantuo", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanwu.renxuanwuzhongwu.fushi': {"id": 24, "ball": "03,04,06,09,11", "type": "xuanwu.renxuanwuzhongwu.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanyi.dingweidan.fushi': {"id": 2, "ball": "04,-,-,-,-", "type": "xuanyi.dingweidan.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanyi.qiansanyimabudingwei.fushi': {"id": 1, "ball": "02", "type": "xuanyi.qiansanyimabudingwei.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanyi.renxuanyizhongyi.danshi': {"id": 4, "ball": "05", "type": "xuanyi.renxuanyizhongyi.danshi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    'xuanyi.renxuanyizhongyi.fushi': {"id": 3, "ball": "05", "type": "xuanyi.renxuanyizhongyi.fushi", "moneyunit": "1", "multiple": 1, "awardMode": award_mode, "num": 1},
    # 趣味
    'caipaiwei.dingweidan.houfushi' :{"id": 22, "ball": "-,-,-,-,-,01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,01 02 03 04 05", "type": "caipaiwei.dingweidan.houfushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 50, "num": 25},
    # 'daxiaodanshuang.dxds.fushi': {},
    'guanya.caiguanya.danshi': {"id": 6, "ball": "01 02","type": "guanya.caiguanya.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 2, "num": 1},
    'guanya.caiguanya.fushi': {"id": 5,"ball": "01 02 03 04 05,01 02 03 04 05,-,-,-,-,-,-,-,-", "type": "guanya.caiguanya.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 40, "num": 20},
    'guanya.hezhi.fushi': {"id": 4, "ball": "3,4,5,6,7,8,9,10,11", "type": "guanya.hezhi.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 100, "num": 50},
    'guanya.zhixuan.danshi': {"id": 1, "ball": "01 02", "type": "guanya.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 2, "num": 1},
    # 'guanya.zhixuan.fushi': {},
    'guanya.zuxuan.danshi': {"id": 3, "ball": "01 02", "type": "guanya.zuxuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 2, "num": 1},
    'guanya.zuxuan.fushi': {"id": 2, "ball": "01,02,03,04,05", "type": "guanya.zuxuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 20, "num": 10},
    'guanyaji.caiguanyaji.danshi': {"id": 12, "ball": "05 06 07", "type": "guanyaji.caiguanyaji.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 2, "num": 1},
    'guanyaji.caiguanyaji.fushi': {"id": 11, "ball": "01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,-,-,-,-,-,-,-", "type": "guanyaji.caiguanyaji.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 120, "num": 60},
    'guanyaji.zhixuan.danshi': {"id": 8, "ball": "05 06 07", "type": "guanyaji.zhixuan.danshi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 2, "num": 1},
    'guanyaji.zhixuan.fushi': {"id": 7, "ball": "01 02 03 04 05,01 02 03 04 05,01 02 03 04 05,-,-,-,-,-,-,-", "type": "guanyaji.zhixuan.fushi", "moneyunit": 1, "multiple": 1, "awardMode": award_mode, "amount": 120, "num": 60},
    'guanyaji.zuxuan.danshi':{"id":10,"ball":"050607","type":"guanyaji.zuxuan.danshi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":2,"num":1},
    'guanyaji.zuxuan.fushi':{"id":9,"ball":"01,02,03,04,05","type":"guanyaji.zuxuan.fushi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":20,"num":10},
    'qiansi.zhixuan.danshi':{"id":14,"ball":"06070809","type":"qiansi.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":2,"num":1},
    'qiansi.zuxuan.fushi':{"id":15,"ball":"02,04,06,08,10","type":"qiansi.zuxuan.fushi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":10,"num":5},
    'qianwu.zhixuan.danshi':{"id":18,"ball":"0104050607","type":"qianwu.zhixuan.danshi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":2,"num":1},
    'qianwu.zhixuan.fushi':{"id":17,"ball":"0204060810,0204060810,0204060810,0204060810,0204060810,-,-,-,-,-","type":"qianwu.zhixuan.fushi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":240,"num":120},
    'qianwu.zuxuan.danshi':{"id":20,"ball":"0206070809","type":"qianwu.zuxuan.danshi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":2,"num":1},
    'qianwu.zuxuan.fushi':{"id":19,"ball":"06,07,08,09,10","type":"qianwu.zuxuan.fushi","moneyunit":1,"multiple":1,"awardMode":award_mode,"amount":2,"num":1},

}
