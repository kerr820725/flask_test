from enum import Enum
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page_objects import BasePages
from utils.Logger import create_logger
from utils.TestTool import trace_log

logger = create_logger(r'\AutoTest', 'base_bet_page')


class BaseBetPage(BasePages.BasePage):
    """
        提供投注頁基本功能
    """
    game_types = None  # 普通 超級2000 趣味
    game_method = None  # 五星 四星 etc

    _retry_times = 0
    _max_retry = 10
    _waitTime = 0.2

    id_submit = "J-submit-order"
    id_random_one = "randomone"
    id_random_five = "randomfive"
    id_trace_switch = "J-trace-switch"

    xpath_get_types = "//*[@id='change']/ul[@style='display: block;'][1]/li"  # 普通/超級2000/趣味玩法測標籤
    xpath_current_methods = "//*[@id='change']/ul[2]/li[@style!='display: none;']"  # 五星/四星玩法組
    xpath_current_games = "//ul[@class='play-select-content clearfix']/li[contains(@class,'current')]//dd"  # 複式/和值等玩法
    xpath_visible_games = "//ul[@class='play-select-content clearfix']/li[contains(@class,'current')]//dd"  # 可點選遊戲清單
    xpath_submit_bet = "//a[@class='btn confirm' and @style!='display:none']"  # 確認按鈕
    xpath_bet_success = "//*[text()='恭喜您投注成功~!']"  # 投注結果訊息
    xpath_use_red = '//*[@id="J-redenvelope-switch"]/label/input'  # 使用紅包開關

    xpath_close_period_popup = "//a[@class='btn closeTip' and @style != 'display:none']"  # 提示彈窗關閉鈕預設(時彩系列)

    @staticmethod
    class GamePages(Enum):
        CQSSC = "CQSSC"
        JLFFC = "JLFFC"
        FFC360 = "360FFC"
        XJSSC = "XJSSC"
        HLJSSC = "HLJSSC"
        SHSSL = "SHSSL"
        TJSSC = "TJSSC"
        TXFFC = "TSFFC"
        FHJLSSC = "FHJLSSC"
        FHCQC = "FHCQC"
        FHXJC = "FHXJC"
        F5C360 = "3605FC"
        V3D = "V3D"
        SLMMC = "SLMMC"
        BTCFFC = "BTCFFC"
        LLSSC = "LLSSC"

    def go_to(self):
        self.driver.get(self.env_config.get_em_url() + self.link)
        return self

    def check_prize_select_popup(self):
        try:
            title = self.driver.find_element_by_class_name('text-title').text
            if title.find('选择一个奖金组'):  # 若顯示獎金組選擇彈窗
                self.driver.find_elements_by_name('radionGourp')[0].click()  # 選擇首個獎金組
                self.driver.find_element_by_xpath("//a[@class='btn confirm' and @style!='display:none']").click()
        except:
            pass

    def get_types(self):
        self.game_types = self.driver.find_elements_by_xpath(self.xpath_get_types)

    def get_current_methods(self):
        return self.driver.find_elements_by_xpath(self.xpath_current_methods)

    def get_current_games(self):
        return self.driver.find_elements_by_xpath(self.xpath_current_games)

    def add_random_bet_1(self):
        try:
            self.driver.find_element_by_id(self.id_random_one).click()
        except Exception as e:
            self.logger.error(trace_log(e))

    def add_random_bet_5(self):
        try:
            self.driver.find_element_by_id(self.id_random_five)
        except Exception as e:
            self.logger.error(trace_log(e))

    def submit_trace(self):
        if self.driver.find_element_by_xpath(self.xpath_use_red).is_selected():  # 若使用紅包為勾選
            self.driver.find_element_by_xpath(self.xpath_use_red).click()  # 取消紅包追號
        self.driver.find_element_by_id(self.id_trace_switch).click()
        self.submit_bet()

    def submit_bet(self):
        self.driver.find_element_by_id(self.id_submit).click()
        self.driver.find_element_by_xpath(self.xpath_submit_bet).click()
        try:
            WebDriverWait(self.driver, 30).until(
                expected_conditions.presence_of_element_located((By.XPATH, self.xpath_bet_success)))
            print('投注結果驗證通過')
        except Exception as e:
            logger.info(trace_log(e))
            print('取得投注結果失敗')
            raise e

    def add_all_random(self, index_t=0, index_m=0, index_g=0):
        """
        投注所有彩種，考量因跨期導致彈窗中段的可能，添加三個參數供接續測試。
        :param index_t: 起始type **呼叫時不需帶參**
        :param index_m: 起始method　**呼叫時不需帶參**
        :param index_g: 起始game　**呼叫時不需帶參**
        """
        _temp_t = index_t  # 紀錄當前type
        _temp_m = index_m  # 紀錄當前method
        _temp_g = index_g  # 紀錄當前game
        self.get_types()
        print('self.game_types = {}'.format(self.game_types))
        try:
            if len(self.game_types) > 0:
                self.logger.debug("len(self.gameTypes) : %s" % len(self.game_types))
                for gType in range(index_t, len(self.game_types)):
                    _temp_t = gType
                    # self.logger.debug("_temp_t:%s" % _temp_t)
                    # self.logger.info(">>>>>%s" % self.game_types[gType].get_attribute('innerHTML'))
                    self.game_types[gType].click()
                    self._add_all_random(index_m, index_g)
                    index_m = 0  # 當本輪皆添加後需初始話避免後續短少
            else:
                self._add_all_random(index_m, index_g)
        except Exception as e:
            self.logger.error(trace_log(e))
            self.check_period_popup()  # 排除臨時顯示彈窗
            self.logger.warning("Retry bet all with type:%s, method:%s, game:%s" % (index_t, index_m, index_g))
            if self._retry_times < self._max_retry:
                self._retry_times += 1
                self.add_all_random(_temp_t, _temp_m, _temp_g)  # 從中斷點再次運行
            else:
                raise e

    def _add_all_random(self, index_m=0, index_g=0):
        _temp_m = index_m  # 紀錄當前method
        _temp_g = index_g  # 紀錄當前game
        try:
            methods = self.get_current_methods()
            for method in range(index_m, len(methods)):
                _temp_m = method
                self.logger.debug("_temp_m:%s" % _temp_m)
                methods[method].click()
                self.logger.info(">>>%s method clicked" % methods[method].get_attribute('innerHTML'))
                sleep(self._waitTime)  # 供JS運行時間
                games = self.get_current_games()
                for game in range(index_g, len(games)):
                    _temp_g = game
                    self.logger.debug("_temp_g:%s" % _temp_g)
                    if self.link == '/gameBet/jlffc':
                        methods[method].click()  # 為配合吉利分分彩新增
                        self.logger.info(">>>%s method clicked." % methods[method].get_attribute('innerHTML'))
                    games[game].click()
                    self.logger.info(">%s game clicked." % games[game].get_attribute('innerHTML'))
                    sleep(0.1)
                    self.add_random_bet_1()
                    sleep(self._waitTime)
                index_g = 0  # 當本輪皆添加後需初始話避免後續短少
        except Exception as e:
            self.logger.error(trace_log(e))
            self.check_period_popup()  # 排除臨時顯示彈窗
            self.logger.warning("Retry bet all with method:%s, game:%s" % (index_m, index_g))
            if self._retry_times < self._max_retry:
                self._retry_times += 1
                self._add_all_random(_temp_m, _temp_g)  # 從中斷點再次運行
            else:
                raise e

    def check_period_popup(self):
        try:
            element = self.driver.find_element_by_xpath(self.xpath_close_period_popup)
            element.click()
        except:
            pass

    def jump_to_game(self, page_name):
        if page_name in self.GamePages:
            if page_name == self.GamePages.JLFFC:
                return BetPage_Jlffc(self)
            elif page_name == self.GamePages.CQSSC:
                return BetPage_Cqssc(self)
            elif page_name == self.GamePages.FFC360:
                return BetPage_360ffc(self)
            elif page_name == self.GamePages.BTCFFC:
                return BetPage_Btcffc(self)
            elif page_name == self.GamePages.F5C360:
                return BetPage_3605fc(self)
            elif page_name == self.GamePages.FHCQC:
                return BetPage_Fhcqc(self)
            elif page_name == self.GamePages.FHJLSSC:
                return BetPage_Fhjlssc(self)
            elif page_name == self.GamePages.HLJSSC:
                return BetPage_Hljssc(self)
            elif page_name == self.GamePages.LLSSC:
                return BetPage_Llssc(self)
            elif page_name == self.GamePages.FHXJC:
                return BetPage_Fhxjc(self)
            elif page_name == self.GamePages.SHSSL:
                return BetPage_Shssl(self)
            elif page_name == self.GamePages.SLMMC:
                return BetPage_Slmmc(self)
            elif page_name == self.GamePages.TJSSC:
                return BetPage_Tjssc(self)
            elif page_name == self.GamePages.TXFFC:
                return BetPage_Txffc(self)
            elif page_name == self.GamePages.V3D:
                return BetPage_V3d(self)
            elif page_name == self.GamePages.XJSSC:
                return BetPage_Xjssc(self)


class BetPage_Cqssc(BaseBetPage):
    """
    重慶時時彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/cqssc'
        self.check_guide()
        self.check_prize_select_popup()

    def check_guide(self):
        try:
            element = self.driver.find_element_by_class_name('guide20000-close')
            element.click()
        except Exception:
            pass


class BetPage_Xjssc(BaseBetPage):
    """
    新疆時時彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/xjssc'
        self.check_guide()
        self.check_prize_select_popup()

    def check_guide(self):
        try:
            element = self.driver.find_element_by_class_name('guide20000-close')
            element.click()
        except Exception:
            pass


class BetPage_Hljssc(BaseBetPage):
    """
    黑龍江時時彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/hljssc'
        self.check_guide()
        self.check_prize_select_popup()

    def check_guide(self):
        try:
            element = self.driver.find_element_by_class_name('guide20000-close')
            element.click()
        except Exception:
            pass


class BetPage_Shssl(BaseBetPage):
    """
    上海時時樂彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/shssl'
        self.check_prize_select_popup()


class BetPage_Tjssc(BaseBetPage):
    """
    天津時時彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/tjssc'
        self.check_prize_select_popup()


class BetPage_Txffc(BaseBetPage):
    """
    騰訊分分彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/txffc'
        self.check_prize_select_popup()


class BetPage_Fhjlssc(BaseBetPage):
    """
    吉利時時彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/fhjlssc'
        self.check_guide()
        self.check_prize_select_popup()

    def check_guide(self):
        try:
            element = self.driver.find_element_by_class_name('guide20000-close')
            element.click()
        except Exception:
            pass


class BetPage_Fhcqc(BaseBetPage):
    """
    重慶全球彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/fhcqc'
        self.check_guide()
        self.check_prize_select_popup()

    def check_guide(self):
        try:
            element = self.driver.find_element_by_class_name('guide20000-close')
            element.click()
        except Exception:
            pass


class BetPage_Fhxjc(BaseBetPage):
    """
    新疆全球彩彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/fhxjc'
        self.check_prize_select_popup()


class BetPage_3605fc(BaseBetPage):
    """
    360五分彩彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/3605fc'
        self.check_prize_select_popup()


class BetPage_V3d(BaseBetPage):
    """
    勝利3D投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.currentMethodsXpath = "//*[@id='change']/ul[2]/li"
        self.link = '/gameBet/v3d'
        self.check_prize_select_popup()
        self.xpath_current_methods = "//*[@id='change']/ul[2]/li"


class BetPage_Slmmc(BaseBetPage):
    """
    順利秒秒彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/slmmc'
        self.check_prize_select_popup()

    def check_guide(self):
        """
        處理秒秒彩加注說明彈窗
        :return: None
        """
        try:
            element = self.driver.find_element_by_class_name('guide20000-close guide20000-close2')
            element.click()
        except Exception:
            pass


class BetPage_Btcffc(BaseBetPage):
    """
    比特幣分分彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/btcffc'
        self.check_prize_select_popup()

    def go_to(self):
        super(BetPage_Btcffc, self).go_to()
        js = "var aa=document.getElementsByClassName('countdown countdown-current')[0];aa.parentNode.removeChild(aa)"
        self.driver.execute_script(js)  # 刪除倒數浮窗
        return self

class BetPage_Llssc(BaseBetPage):
    """
    樂利時時彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/llssc'
        self.check_prize_select_popup()


class BetPage_360ffc(BaseBetPage):
    """
    360分分彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/360ffc'
        self.check_prize_select_popup()


class BetPage_Jlffc(BaseBetPage):
    """
    吉利分分彩投注頁
    """

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/gameBet/jlffc'
        self.check_prize_select_popup()
        self.closePeriodPopupXpath = "//div[@class='j-ui-miniwindow pop w-9' and contains(@style,'display: " \
                                     "block')]//a[@class='close closeBtn'] "
