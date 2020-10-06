from enum import Enum

from page_objects import BasePages


class BasePersonal(BasePages.BasePage):
    @staticmethod
    class personal_elements(Enum):
        query_orders_button = "(//dl[@class='side-bet']//a)[1]"  # 投注紀錄
        query_plans_button = "(//dl[@class='side-bet']//a)[2]"  # 追號紀錄
        query_fund_detail_button = "(//dl[@class='side-bet']//a)[3]"  # 帳戶明細
        save_center_button = "(//dl[@class='side-safe']//a)[1]"  # 安全中心
        bind_card_button = "(//dl[@class='side-safe']//a)[2]"  # 銀行卡管理
        personal_info_button = "(//dl[@class='side-safe']//a)[3]"  # 個人資料
        safe_code_edit_button = "(//dl[@class='side-safe']//a)[4]"  # 密碼管理
        query_bonus_details_button = "(//dl[@class='side-safe']//a)[5]"  # 獎金詳情

    def personal_jump_to(self, button_name):
        if button_name in self.personal_elements:
            self.driver.find_element_by_xpath(button_name.value).click()
            if button_name == self.personal_elements.save_center_button:
                return Personal_AppCenterPage(self)
            elif button_name == self.personal_elements.bind_card_button:
                return Personal_BindCardPage(self)


class Personal_AppCenterPage(BasePersonal):
    """安全中心"""

    @staticmethod
    class buttons(Enum):
        id_change_password = 'changePWBtn'  # 修改密碼
        id_change_safe_password = 'changeSafePW'  # 修改安全密碼
        id_set_safe_password = 'setSafePW'  # 設置安全密碼
        id_get_safe_password = 'getSafePW'  # 尋找密碼
        id_set_safe_question = 'setSafeQuestion'  # 設置安全問題
        id_change_question = 'changeSafeQuestion'  # 修改安全問題
        id_set_question = 'setSafeQuestion'  # 修改安全問題
        id_set_email = 'setEmail'  # 綁定信箱
        id_change_email = 'changeEmail'  # 修改綁定信箱

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/safepersonal/safecenter'
        self.go_to()

    def jump_to(self, button):
        """
        :param button: self.buttons(Enum)
        :return: other page of module
        """
        self.logger.info('Personal_AppCenterPage.jump_to : {}'.format(button.value))
        if button in self.buttons:
            self.driver.find_element_by_id(button.value).click()
            if button == self.buttons.id_change_password:
                return Personal_ChangePasswordPage(self)
            elif button == self.buttons.id_change_safe_password:
                return Personal_ChangeSavePasswordPage(self)
            elif button == self.buttons.id_set_safe_password:
                return Personal_SetSafePasswordPage(self)
            elif button == self.buttons.id_set_question:
                return Personal_SetQuestionPage(self)
        else:
            raise Exception('無對應按鈕')


class Personal_ChangePasswordPage(BasePersonal):
    """修改密碼頁"""

    @staticmethod
    class elements(Enum):
        old_password_input = 'J-password'
        new_password_input = 'J-password-new'
        confirm_password_input = 'J-password-new2'
        submit_button = 'J-button-submit-password'
        result_text = "//*[@id='Idivs']//*[@class='pop-text']"

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/safepersonal/safecodeedit'

    def change_password(self, password: str) -> BasePages.LoginPage:
        """
        修改密碼腳本，含結果文字驗證
        :param password: 新密碼
        :return: 返還登入頁
        """
        self.logger.info('change_password(password = {})'.format(password))
        expected = '恭喜您密码修改成功，请重新登录。'
        self.driver.find_element_by_id(self.elements.old_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.new_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.confirm_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.submit_button.value).click()
        pop_up_text = self.driver.find_element_by_xpath(self.elements.result_text.value).get_attribute('innerHTML')
        assert pop_up_text == expected
        print('彈窗提示：{}'.format(pop_up_text))
        self.driver.find_element_by_id('closeTip1').click()
        from page_objects.BasePages import LoginPage
        return LoginPage(last_page=self)


class Personal_SetSafePasswordPage(BasePersonal):
    """
    設置安全密碼頁
    """

    @staticmethod
    class elements(Enum):
        id_new_safe_password_input = 'J-safePassword'
        id_confirm_safe_password_input = 'J-safePassword2'
        id_submit_button = 'J-button-submit'
        xpath_result_text = "//div[@class='txt']/h4"

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/safepersonal/safecodeset'

    def set_safe_password(self, password: str):
        """
        設置安全密碼腳本，含結果文字驗證
        :param: password: 新密碼
        :return: 返還登入頁
        """
        self.logger.info('change_password(password = {})'.format(password))
        expected = '恭喜您安全密码设置成功！'
        self.driver.find_element_by_id(self.elements.id_new_safe_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.id_confirm_safe_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.id_submit_button.value).click()
        pop_up_text = self.driver.find_element_by_xpath(self.elements.xpath_result_text.value).get_attribute(
            'innerHTML')
        try:
            assert pop_up_text == expected
            print('彈窗提示：{}'.format(pop_up_text))
        except Exception:
            print('設置安全密碼失敗')
        self.logger.error(Exception)


class Personal_SetQuestionPage(BasePersonal):
    """
    設置安全密碼頁
    """

    @staticmethod
    class elements(Enum):
        xpath_answer_input = '(//*[@id="J-safe-question-select"]//input)[{}]'
        xpath_quest_select = '(//*[@id="J-safe-question-select"]/li/select/option[2])[{}]'
        id_submit_button = 'J-button-submit'
        id_confirm_submit_button = "J-safequestion-submit"
        xpath_result_text = "//div[@class='txt']/h4"

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/safepersonal/safecodeset'

    def set_questions(self, answer: str):
        """
        設置安全問題
        :param: password: 問題答案
        :return: 返還登入頁
        """
        self.logger.info('Personal_SetQuestionPage(password = {})'.format(answer))
        expected = '恭喜您安全问题设置成功！'
        self.driver.find_element_by_xpath(self.elements.xpath_quest_select.value.format(1)).click()
        self.driver.find_element_by_xpath(self.elements.xpath_quest_select.value.format(2)).click()
        self.driver.find_element_by_xpath(self.elements.xpath_quest_select.value.format(3)).click()
        self.driver.find_element_by_xpath(self.elements.xpath_answer_input.value.format(1)).send_keys(answer)
        self.driver.find_element_by_xpath(self.elements.xpath_answer_input.value.format(2)).send_keys(answer)
        self.driver.find_element_by_xpath(self.elements.xpath_answer_input.value.format(3)).send_keys(answer)
        self.driver.find_element_by_id(self.elements.id_submit_button.value).click()
        self.driver.find_element_by_id(self.elements.id_confirm_submit_button.value).click()
        pop_up_text = self.driver.find_element_by_xpath(self.elements.xpath_result_text.value).get_attribute(
            'innerHTML')
        try:
            assert pop_up_text == expected
            print('彈窗提示：{}'.format(pop_up_text))
        except Exception:
            print('設置安全問題失敗')
        self.logger.error(Exception)


class Personal_BindCardPage(BasePersonal):
    """
    設置安全密碼頁
    """

    class elements(Enum):
        xpath_bind_card_now = "//*[text()='立即绑定']"
        xpath_bank_list = '//*[@id="bankid"]/option[{}]'
        xpath_province_list = '//*[@id="province"]/option[{}]'
        id_branchAddr = 'branchAddr'
        id_bankAccount = 'bankAccount'
        id_bankNumber = 'bankNumber'
        id_bankNumber2 = 'bankNumber2'
        id_securityPassword = 'securityPassword'
        id_submit = 'J-Submit'
        xpath_bind_result = "//div[@class='pop-success']/h4"
        id_close_pop = 'CloseDiv2'

        xpath_to_usdt = '//*[@id="J-form"]//li[text()="数字货币钱包管理"]'
        id_usdt_walletAddr = 'walletAddr'

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/bindcard'

    def to_bind_first_card(self, branchAddr="測試支行", bankAccount='測試用戶', bankNumber='0000000000000000',
                           securityPassword=None):
        expected = '银行卡绑定成功！'
        if securityPassword is None:
            securityPassword = self.env_config.get_safe_password()
        self.driver.find_element_by_xpath(self.elements.xpath_bind_card_now.value).click()
        self.driver.find_element_by_xpath(self.elements.xpath_bank_list.value.format(2)).click()
        self.driver.find_element_by_xpath(self.elements.xpath_province_list.value.format(2)).click()
        self.driver.find_element_by_id(self.elements.id_branchAddr.value).send_keys(branchAddr)
        self.driver.find_element_by_id(self.elements.id_bankAccount.value).send_keys(bankAccount)
        self.driver.find_element_by_id(self.elements.id_bankNumber.value).send_keys(bankNumber)
        self.driver.find_element_by_id(self.elements.id_bankNumber2.value).send_keys(bankNumber)
        self.driver.find_element_by_id(self.elements.id_securityPassword.value).send_keys(securityPassword)
        self.driver.find_element_by_id(self.elements.id_submit.value).click()
        assert self.driver.find_element_by_xpath(self.elements.xpath_bind_result.value).get_attribute(
            'innerHTML') == expected
        self.driver.find_element_by_id(self.elements.id_close_pop.value).click()
        return self

    def to_bind_first_usdt_card(self, walletAddr='USDT測試地址', securityPassword=None):
        expected = '数字货币钱包账户绑定成功！'
        if securityPassword is None:
            securityPassword = self.env_config.get_safe_password()
        self.driver.find_element_by_xpath(self.elements.xpath_to_usdt.value).click()
        self.driver.find_element_by_xpath(self.elements.xpath_bind_card_now.value).click()
        self.driver.find_element_by_id(self.elements.id_usdt_walletAddr.value).send_keys(walletAddr)
        self.driver.find_element_by_id(self.elements.id_securityPassword.value).send_keys(securityPassword)
        self.driver.find_element_by_id(self.elements.id_submit.value).click()
        assert self.driver.find_element_by_xpath(self.elements.xpath_bind_result.value).get_attribute(
            'innerHTML') == expected
        self.driver.find_element_by_xpath("//div[@class = 'pop-btn']/a[@class='btn btn-important']").click()


class Personal_ChangeSavePasswordPage(BasePersonal):
    """修改安全密碼頁"""

    @staticmethod
    class elements(Enum):
        old_safe_password_input = 'J-safePassword'
        new_safe_password_input = 'J-safePassword-new'
        confirm_safe_password_input = 'J-safePassword-new2'
        submit_button = 'J-button-submit-safePassword'

    def __init__(self, last_page):
        super().__init__(last_page=last_page)
        self.link = '/safepersonal/safecodeedit?issafecode=1'
        if self.env_config.get_env_id() == 0:
            self.safe_pass = 'hsieh123'
        elif self.env_config.get_env_id() == 1:
            self.safe_pass = 'kerr123'
        else:
            raise Exception('無對應安全密碼，請至test_applycenter新增')

    def change_safe_password(self, password):
        expected = '安全密码修改成功'
        self.driver.find_element_by_id(self.elements.old_safe_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.new_safe_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.confirm_safe_password_input.value).send_keys(password)
        self.driver.find_element_by_id(self.elements.submit_button.value).click()
        # assert self.driver.find_element_by_xpath("//*[@id='Idivs']//*[@class='pop-text']").text == expected
