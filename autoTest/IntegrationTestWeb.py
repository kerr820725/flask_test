import random
from datetime import datetime
import os
import unittest

from faker import Factory

from page_objects.BasePages import LoginPage, MainPage, BasePage
from page_objects.BetPages import BetPage_Xjssc, BetPage_Cqssc, BetPage_Hljssc, BetPage_Shssl, BetPage_Tjssc, \
    BetPage_Txffc, BetPage_Fhjlssc, BetPage_Fhcqc, BetPage_Fhxjc, BetPage_3605fc, BetPage_V3d, BetPage_Slmmc, \
    BetPage_Btcffc, BetPage_Llssc, BetPage_360ffc, BetPage_Jlffc
from page_objects.PersonalPages import Personal_AppCenterPage, BasePersonal
from utils import Config, Logger
from utils.Config import LotteryData
from utils.TestTool import trace_log


def date_time():  # 給查詢 獎期to_date時間用, 今天時間
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    format_day = '{:02d}'.format(day)
    return '%s-%s-%s' % (year, month, format_day)


def get_order_code_web(conn, user, lottery):  # webdriver頁面投注產生定單
    with conn.cursor() as cursor:
        sql = "select order_code from game_order where userid in \
        (select id from user_customer where account = '{user}' \
        and order_time > to_date('{time}','YYYY-MM-DD')and lotteryid = {lottery_id})".format(user=user,
                                                                                             time=date_time(),
                                                                                             lottery_id=
                                                                                                           LotteryData.lottery_dict[
                                                                                                               lottery][
                                                                                                               1])
        cursor.execute(sql)
        rows = cursor.fetchall()

        order_code = []
        for i in rows:  # i 生成tuple
            order_code.append(i[0])
    conn.close()
    return order_code


def select_user_url(conn, userid):
    with conn.cursor() as cursor:
        sql = "select url from user_url where url like '%{}%' and days = -1".format(userid)
        cursor.execute(sql)
        rows = cursor.fetchall()
        user_url = []

        for i in rows:
            user_url.append(i[0])
    conn.close()
    return user_url


logger = Logger.create_logger(r"\AutoTest", 'auto_test_integration')


class IntegrationTestWeb(unittest.TestCase):
    u"瀏覽器功能測試"
    env_config = None
    user = None
    red_type = None
    driver = None
    post_url = None
    em_url = None
    pageObject = None

    def setUp(self):
        logger.info('IntegrationTestWeb setUp : {}'.format(self._testMethodName))

    def __init__(self, case, env_config, user, red_type):
        super().__init__(case)
        self.env_config = env_config
        self.user = user
        self.red_type = red_type

    # def mul_submit(self):  # 追號
    #     try:
    #         if self.driver.find_element_by_xpath('//*[@id="J-redenvelope-switch"]/label/input').is_selected():
    #             self.driver.find_element_by_xpath('//*[@id="J-redenvelope-switch"]/label/input').click()  # 取消紅包追號
    #     except:
    #         pass
    #     self.id_element('randomone')  # 先隨機一住
    #     self.id_element('J-trace-switch')  # 追號
    #

    # def mul_submit(self):  # 追號
    #     try:
    #         if self.driver.find_element_by_xpath('//*[@id="J-redenvelope-switch"]/label/input').is_selected():
    #             self.driver.find_element_by_xpath('//*[@id="J-redenvelope-switch"]/label/input').click()  # 取消紅包追號
    #     except:
    #         pass
    #     self.id_element('randomone')  # 先隨機一住
    #     self.id_element('J-trace-switch')  # 追號
    #

    def test_cqssc(self):
        """
        重慶時時彩測試
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Cqssc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('重慶時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('重慶時時彩投注失敗.')
            raise e

    def test_hljssc(self):
        """
        黑龍江時時彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Hljssc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('黑龍江時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('黑龍江時時彩投注失敗.')
            raise e

    def test_shssl(self):
        """
        上海時時樂
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Shssl(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('上海時時樂投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('上海時時樂投注失敗.')
            raise e

    def test_tjssc(self):
        """
        天津時時彩測試
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Tjssc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('天津時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('天津時時彩投注失敗.')
            raise e

    def test_txffc(self):
        """
        騰訊時時彩測試
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Txffc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('騰訊時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('騰訊時時彩投注失敗.')
            raise e

    def test_fhjlssc(self):
        """
        鳳凰吉利時時彩測試
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Fhjlssc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('鳳凰吉利時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('鳳凰吉利時時彩投注失敗.')
            raise e

    def test_fhcqc(self):
        """
        鳳凰時時彩測試
        :return:
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Fhcqc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('鳳凰時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('鳳凰時時彩投注失敗.')
            raise e

    def test_fhxjc(self):
        """
        新疆全球彩測試
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Fhxjc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('新疆全球彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            print('新疆全球彩投注失敗.')
            raise e

    def test_3605fc(self):
        """
        360五分彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_3605fc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('360五分彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('360五分彩投注失敗.')
            raise e

    def test_v3d(self):
        """
        勝利3D彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_V3d(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('勝利3D彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('勝利3D彩投注失敗.')
            raise e

    def test_slmmc(self):
        """
        順利秒秒彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Slmmc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('順利秒秒彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('順利秒秒彩投注失敗.')
            raise e

    def test_btcffc(self):
        """
        比特幣時時彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Btcffc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('比特幣時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('比特幣時時彩投注失敗.')
            raise e

    def test_llssc(self):
        """
        樂利時時彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Llssc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('樂利時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('樂利時時彩投注失敗.')
            raise e

    def test_360ffc(self):
        """
        360分分彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_360ffc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('360分分彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('360分分彩投注失敗.')
            raise e

    def test_jlffc(self):
        """
        吉利時時彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Jlffc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('吉利時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('吉利時時彩投注失敗.')
            raise e

    def test_xjssc(self):
        """
        新疆時時彩
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password())  # 初始化與登入
            self.pageObject = BetPage_Xjssc(self.pageObject)  # 前往彩種投注頁
            self.pageObject.go_to().add_all_random()
            self.pageObject.submit_trace()
            self.getImage()
            print('新疆時時彩投注成功.')
        except Exception as e:
            logger.error(trace_log(e))
            self.getImage()
            print('新疆時時彩投注失敗.')
            raise e

    def test_change_password(self):
        """
        修改密碼測試
        :return: None
        """
        try:
            self.pageObject = LoginPage(env_config=self.env_config) \
                .login(user=self.user, password=self.env_config.get_password()) \
                .jump_to(page=MainPage.buttons_personal.safe_center) \
                .jump_to(button=Personal_AppCenterPage.buttons.id_change_password) \
                .set_safe_password(password=self.env_config.get_password())
            url = self.pageObject.get_current_url()
            self.getImage()
            assert '/login' in url
        except Exception as e:
            from utils.TestTool import trace_log
            logger.error(e)
            self.getImage()
            raise e

    def getImage(self):
        """
        截取图片,并保存在images文件夹
        :return: 无
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(Config.project_path + r'\static\image\screenshot\{}.png'.format(str(timestamp)))
        try:
            driver = self.pageObject.get_driver()
            driver.save_screenshot(imgPath)
            print('screenshot:{}.png'.format(timestamp))
        except Exception as e:
            logger.error(e)

    def test_applycenter(self):
        """開戶中心/安全中心/綁卡"""

        try:
            self.pageObject = LoginPage(self.env_config) \
                .login(self.user, self.env_config.get_password()) \
                .dir_jump_to(BasePage.CustomPages.register)  # 初始化、登入並跳轉註冊頁
            self.pageObject = self.pageObject.random_register()  # 亂數註冊並返回首頁
            print('新用戶創建成功')
            self.getImage()
        except Exception:
            logger.error(Exception)
            print('新用戶創建失敗')
            self.getImage()
            raise Exception

        try:
            self.pageObject = self.pageObject \
                .jump_to(MainPage.buttons_personal.safe_center) \
                .jump_to(Personal_AppCenterPage.buttons.id_set_safe_password)  # 跳轉首頁>安全中心>設置安全密碼
            self.pageObject.set_safe_password(self.env_config.get_safe_password())  # 完成設置
            print('安全密碼設置成功')
            self.getImage()
        except Exception:
            logger.error(Exception)
            print('安全密碼設置失敗')
            self.getImage()
            raise Exception

        try:
            self.pageObject = self.pageObject \
                .personal_jump_to(BasePersonal.personal_elements.save_center_button) \
                .jump_to(Personal_AppCenterPage.buttons.id_set_question)  # 點側邊安全中心 > 設置安全問題
            self.pageObject.set_questions(self.env_config.get_safe_password())  # 設置安全問題 *暫同安全密碼
            print('安全問題設置成功')
            self.getImage()
        except Exception:
            logger.error(Exception)
            print('安全問題設置失敗')
            self.getImage()
            raise Exception

        try:
            fake = Factory.create()
            self.pageObject = self.pageObject.personal_jump_to(
                BasePersonal.personal_elements.bind_card_button)  # 跳轉銀行卡頁
            self.pageObject.to_bind_first_card(bankNumber=fake.credit_card_number(card_type='visa16'),
                                               securityPassword=self.env_config.get_safe_password())
            print('銀行卡綁定成功')
            self.getImage()
        except Exception:
            logger.error(Exception)
            print('銀行卡綁定失敗')
            self.getImage()
            raise Exception

        try:
            self.pageObject.to_bind_first_usdt_card(walletAddr=random.randint(1000, 1000000000),
                                                    securityPassword=self.env_config.get_safe_password())
            print('USDT銀行卡綁定成功')
            self.getImage()
        except Exception:
            logger.error(Exception)
            print('USDT銀行卡綁定失敗')
            self.getImage()
            raise Exception

    def tearDown(self) -> None:
        driver = self.pageObject.get_driver()
        driver.quit()
