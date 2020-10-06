import random
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.Connection import OracleConnection
from utils.Logger import create_logger
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from enum import Enum
from utils import Config
from utils.TestTool import trace_log


class BasePage:
    logger = create_logger(r'\AutoTest', 'base_page')
    driver = None
    env_config = None
    link = None
    user = None
    password = None

    @staticmethod
    class CustomPages(Enum):  # 部分需直接跳轉頁面
        register = "register"

    def __init__(self, last_page=None, env_domain=None):
        """
        POM物件初始化
        可能情況：
        1. 網頁新建 -> LoginPage('Dev02') -> __init__(env)
        2. 網頁移動 -> MainPage(self) -> __init__(self)
        :param env_domain:　指定測試網域，用於初始POM物件，同時新創建driver
        :param last_page: 上一個頁面的POM物件，需繼承自BasePage，若不為空則以此物件參數進行初始化、沿用參數
        """
        if last_page:
            self.env_config = last_page.env_config
            self.driver = last_page.driver
            self.user = last_page.user
            self.password = last_page.password
            self.logger = last_page.logger
        else:
            if type(env_domain) is Config.EnvConfig:
                self.env_config = env_domain
            else:
                self.env_config = Config.EnvConfig(env_domain)
            self.driver = self.get_driver()

    def get_driver(self) -> webdriver:
        self.logger.info('BasePage.get_driver : self.driver = {}'.format(self.driver))
        if self.driver is None:
            try:
                if 'ChromeDriver' in locals() or 'ChromeDriver' in globals():
                    self.driver = webdriver.Chrome(chrome_options=Config.chrome_options)
                else:
                    self.driver = webdriver.Chrome(Config.chromeDriver_Path, chrome_options=Config.chrome_options)
                self.driver.implicitly_wait(10)
                self.driver.set_page_load_timeout(30)
            except Exception as e:
                self.logger.error(trace_log(e))
        return self.driver

    def go_to(self):
        self.driver.get(self.env_config.get_post_url() + self.link)

    def check_driver_state(self):
        try:
            self.driver.execute(Command.STATUS)
            return True
        except Exception as e:
            self.logger.error(trace_log(e))
            return False

    def get_visibal_elements(self, elements):
        tempElements = []
        for element in elements:
            if element.get_attribute('style') != 'display:none':
                tempElements += element
        return tempElements

    def dir_jump_to(self, page_name: Enum):
        if page_name in self.CustomPages:
            if page_name == self.CustomPages.register:
                return RegPage(self)

    def get_current_url(self) -> str:
        if not self.driver:
            raise Exception('未能取得瀏覽器')
        return self.driver.current_url


class MainPage(BasePage):
    """首頁"""

    i_user_header = 'headerUsername'

    @staticmethod
    class buttons_personal(Enum):
        bet_record = 'betRecord'
        account_detail = 'accountDetail'
        proxy_center = 'proxyCenter'
        query_report = 'queryReport'
        front_score_mall = 'frontScoreMall'
        safe_center = 'safeCenter'

    def __init__(self, last_page: BasePage):
        """
        首頁初始化。
        針對彈窗進行等待與點擊
        :param last_page:
        """
        self.logger.info('{} init started.'.format(self.__class__.__name__))
        super().__init__(last_page=last_page)
        self.link = "/"
        self.go_to()
        while True:
            close_result = self.close_pop_up()
            if not close_result:
                break
        self.logger.info('{} init ended.'.format(self.__class__.__name__))

    def jump_to(self, page: Enum):
        """
        點擊對應連結按鈕
        :param page: self.Personal / self.Bet
        :return: 對應頁面 Class
        """
        if page in self.buttons_personal:
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_id(self.i_user_header)).perform()
            self.driver.find_element_by_id(page.value).click()
            if page == self.buttons_personal.safe_center:
                from page_objects.PersonalPages import Personal_AppCenterPage
                self.driver.switch_to.window(self.driver.window_handles[-1])  # 因新開分頁，切換至最新分頁
                # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'W')
                return Personal_AppCenterPage(self)
            else:
                raise Exception('POM尚未建立')
        else:
            raise Exception('無對應對象')

    def close_pop_up(self) -> bool:
        try:
            element = WebDriverWait(self.driver, 10) \
                .until(
                method=EC.presence_of_element_located(By.XPATH("//div[contains(@class,'close-popup-activity')]")))
            element.click()
            return True
        except:
            return False


class LoginPage(BasePage):
    @staticmethod
    class elements(Enum):
        id_input_account = 'J-user-name'
        id_input_password = 'J-user-password'
        id_button_login = 'J-form-submit'
        xpath_button_sign_up = '//*[@id="J-button-submitDev"]/li[3]/a'
        id_button_free_trial = 'freeTrial'
        id_button_save_login = 'safeLogin'
        xpath_button_forget_password = '//*[@id="J-button-submitDev"]/li[1]/a'
        xpath_fhlm_logo = "//img[@class='fhlm-logo']"
        id_j_dl_apple = 'J-download-apple'
        id_j_dl_android = 'J-download-android'
        id_safeLogin = 'safeLogin'

    def __init__(self, env_config=None, last_page=None):
        """
        登入頁初始化，多於測試初使時呼叫。env_config / last_page需給予其一
        :param env_config: 初始化用網域參數，見 Config.EnvConfig
        :param last_page: 前一網頁，POM架構，需繼承自 BasePage
        """
        if last_page:
            super().__init__(last_page=last_page)
            self.env_config = last_page.env_config
        else:
            super().__init__(env_domain=env_config)
        self.logger.info('{} init started.'.format(self.__class__.__name__))
        self.link = "/login"
        self.go_to()
        self.logger.info('{} init ended.'.format(self.__class__.__name__))

    def login(self, user: str, password: str) -> MainPage:
        self.logger.info('login(user = {}, password = {})'.format(user, password))
        self.user = user
        self.password = password
        try:
            self.driver.find_element_by_id(self.elements.id_input_account.value).send_keys(user)
            self.driver.find_element_by_id(self.elements.id_input_password.value).send_keys(password)
            self.driver.find_element_by_id(self.elements.id_button_login.value).click()
        except NoSuchElementException as e:
            self.logger.warring(e)
            raise e
        except:
            raise Exception('未知錯誤')
        sleep(3)
        return MainPage(self)

    def jump_to(self, element: elements):
        if element not in (self.elements.id_safeLogin, self.elements.id_button_free_trial):
            raise NoSuchElementException('Wrong element.')
        if element is self.elements.id_safeLogin:
            return ShowSecLoginPage(self)

    def mouse_action(self, element: elements):
        if element in (self.elements.id_j_dl_android, self.elements.id_j_dl_apple):
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_id(element.value)).perform()
        elif element == self.elements.xpath_fhlm_logo:
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(element.value)).perform()


class ShowSecLoginPage(BasePage):
    @staticmethod
    class elements(Enum):
        id_input_account = 'J-user-name'
        id_button_login = 'J-form-submit'
        id_return_normal = 'normalLogin'
        id_j_dl_apple = 'J-download-apple'
        id_j_dl_android = 'J-download-android'
        xpath_fhlm_logo = "//img[@class='fhlm-logo']"

    def __init__(self, last_page: BasePage):
        """
        安全登入頁
        :param last_page: 前一網頁，POM架構，需繼承自 BasePage
        """
        super().__init__(last_page=last_page)
        self.logger.info('{} init started.'.format(self.__class__.__name__))
        self.link = "/login/showsectlogin"
        self.go_to()
        self.logger.info('{} init ended.'.format(self.__class__.__name__))

    def jump_to(self, element: elements):
        if element is not self.elements.id_return_normal:
            return 'Wrong element.'
        return LoginPage(last_page=self)

    def mouse_action(self, element: elements):
        if element in (self.elements.id_j_dl_android, self.elements.id_j_dl_apple):
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_id(element.value)).perform()
        elif element == self.elements.xpath_fhlm_logo:
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(element.value)).perform()


class RegPage(BasePage):
    @staticmethod
    class elements(Enum):
        id_user_name_input = 'J-input-username'
        id_password_input = 'J-input-password'
        id_password_confirm = 'J-input-password2'
        id_submit = 'J-button-submit'

    def __init__(self, last_page: BasePage):
        super().__init__(last_page=last_page)
        conn = OracleConnection(self.env_config.get_env_id())
        user_id = conn.get_sql_exec("select id from user_customer where account = '{}'".format(self.user))
        self.logger.info("user_id = {}".format(user_id[0]))
        reg_url = conn.get_sql_exec("select url from user_url where days = -1 and creator = '{}'".format(user_id[0]))
        self.logger.info("reg_url = {}".format(reg_url[0]))
        self.link = "/register?{url}".format(url=reg_url[0])

    def random_register(self) -> MainPage:
        self.go_to()
        _random = random.randint(1, 100000)
        new_user = self.user + str(_random)
        self.driver.find_element_by_id(self.elements.id_user_name_input.value).send_keys(new_user)
        self.driver.find_element_by_id(self.elements.id_password_input.value).send_keys(self.password)
        self.driver.find_element_by_id(self.elements.id_password_confirm.value).send_keys(self.password)
        self.driver.find_element_by_id(self.elements.id_submit.value).click()
        sleep(5)
        self.user = new_user
        assert '/index' in self.driver.current_url
        return MainPage(self)
