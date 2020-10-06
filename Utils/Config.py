from selenium.webdriver.chrome.options import Options
from enum import Enum
import os
import AutoTest

path1=os.path.abspath('.')
# ChromeDriver 取用路徑 (若環境參數無法獲取時取用)
chromeDriver_Path = path1 + "\\chromedriver.exe"
# report.html 絕對路徑
reportHtml_Path = path1 + "\\templates\\report.html"  

# ChromeDriver 設定參數
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 背景執行
chrome_options.add_argument("--start-maximized")  # 背景執行


class UserAgent(Enum):
    PC = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.100 Safari/537.36"
    ANDROID = "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36"
    IOS = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"


class EnvConfig:
    devDomains = ['dev02', 'dev03', 'fh82dev02', '88hlqpdev02', 'teny2020dev02']
    joyDomains = ['joy188', 'joy188.teny2020', 'joy188.195353', 'joy188.88hlqp']
    joySunDomains = ['joy188.fh888']
    hyDomains = ['maike2020']
    productDomains = ['fh968']

    env_domain = None

    def __init__(self, domain):
        try:
            if domain in self.devDomains + self.joySunDomains + self.joyDomains + self.hyDomains + self.productDomains:
                self.env_domain = domain
        except ValueError:
            raise Exception('無對應網域 請至 Config.EnvConfig 添加')

    def get_domain(self):
        return self.env_domain

    def get_post_url(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains + self.hyDomains + self.productDomains:
            return "http://www.%s.com" % self.env_domain
        elif self.env_domain in self.joyDomains:
            return "http://www2.%s.com" % self.env_domain
        elif self.env_domain in self.joySunDomains:
            return "http://www2.%s.bet" % self.env_domain
        else:
            raise Exception('無對應網域參數，請至Config envConfig()新增')

    def get_em_url(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.joySunDomains:
            return "http://em.%s.bet" % self.env_domain
        elif self.env_domain in self.devDomains + self.joyDomains + self.hyDomains + self.productDomains:
            return "http://em.%s.com" % self.env_domain
        else:
            raise Exception('無對應網域參數，請至Config envConfig()新增')

    def get_password(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains:
            return "123qwe"
        elif self.env_domain in self.joyDomains + self.hyDomains + self.joySunDomains:
            return "amberrd"
        elif self.env_domain in self.productDomains:
            return "tsuta0425"
        else:
            raise Exception('無對應網域參數，請至Config envConfig()新增')

    def get_env_id(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains:
            return 0
        elif self.env_domain in self.joyDomains + self.joySunDomains + self.hyDomains:
            return 1
        else:
            raise Exception('無對應網域參數，請至Config envConfig()新增')

    def get_admin_url(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains:
            return "http://admin.dev02.com"
        elif self.env_domain in self.joyDomains + self.joySunDomains:
            return "http://admin.joy188.com"
        else:
            raise Exception('無對應網域參數，請至Config envConfig()新增')

    def get_admin_data(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains:
            return {'username': 'cancus', 'password': '123qwe', 'bindpwd': 123456}
        elif self.env_domain in self.joyDomains + self.joySunDomains:
            return {'username': 'cancus', 'password': 'amberrd', 'bindpwd': 123456}
        else:
            raise Exception('無對應網域參數，請至Config envConfig()新增')
    
    def get_joint_venture(self,env,domain):
        AutoTest.Joy188Test.select_domainUrl(AutoTest.Joy188Test.get_conn(int(env)),domain)#先去全局 找是否有設定 該domain
        # 查詢後台是否有設置
        try:
            domain_type  = AutoTest.domain_url[0][5]# 判斷 該domain 再後台全局設定 的 joint_venture 是多少
            print("後台設置: %s"%domain_type)
            return domain_type
        except KeyError:
            print("全局後台沒設置")
            if self.env_domain is None:
                raise Exception('env 環境未初始化')
            elif self.env_domain in ['dev02', 'joy188']:
                return 0
            elif self.env_domain in ['fh82dev02', 'teny2020dev02', 'joy188.teny2020', 'joy188.195353']:
                return 1
            elif self.env_domain in ['joy188.88hlqp', '88hlqpdev02']:
                return 2
            else:
                raise Exception('無對應網域參數，請至Config envConfigApp()新增')


class EnvConfigApp(EnvConfig):
    def __init__(self, domain):
        super().__init__(domain)

    def get_iapi(self):
        print(self.env_domain)
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains:
            return "http://10.13.22.152:8199/"
        elif self.env_domain in self.joyDomains:
            return "http://iphong.joy188.com/"
        else:
            raise Exception('無對應網域參數，請至Config envConfigApp()新增')

    def get_uuid(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains:
            return "2D424FA3-D7D9-4BB2-BFDA-4561F921B1D5"
        elif self.env_domain in self.joyDomains:
            return "f009b92edc4333fd"
        else:
            raise Exception('無對應網域參數，請至Config envConfigApp()新增')

    def get_login_pass_source(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in self.devDomains:
            return "fa0c0fd599eaa397bd0daba5f47e7151"
        elif self.env_domain in self.joyDomains:
            return "3bf6add0828ee17c4603563954473c1e"
        else:
            raise Exception('無對應網域參數，請至Config envConfigApp()新增')

    def get_joint_venture(self):
        if self.env_domain is None:
            raise Exception('env 環境未初始化')
        elif self.env_domain in ['dev02', 'joy188']:
            return 0
        elif self.env_domain in ['fh82dev02', 'teny2020dev02', 'joy188.teny2020', 'joy188.195353']:
            return 1
        elif self.env_domain in ['joy188.88hlqp', '88hlqpdev02']:
            return 2
        else:
            raise Exception('無對應網域參數，請至Config envConfigApp()新增')
