import datetime
import os
import unittest
import HTMLTestRunner

from autoTest.ApiTestApp import ApiTestApp, ApiTestAPP_YFT
from autoTest.ApiTestPC import ApiTestPC, ApiTestPC_YFT
from autoTest.IntegrationTestWeb import IntegrationTestWeb
from utils import Config
from utils.Connection import PostgresqlConnection, OracleConnection, MysqlConnection
from utils.Logger import create_logger
from utils.TestTool import trace_log

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 避免抓出oracle中文 為問號


def date_time():  # 給查詢 獎期to_date時間用, 今天時間
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    format_day = f'{day:02d}'
    return f'{year}-{month}-{format_day}'


def suite_test(test_cases, user_name, test_env, is_use_red, money_unit, award_mode):
    """
    autoTest 初始化
    :param award_mode: 獎金模式 (0:預設 / 1:高獎金 / 2:高獎金)
    :param money_unit: 元角分模式 (1 / 0.1 / 0.01)
    :param test_cases: Array[][]; 測試項目，為二維矩陣。第一維區分測試類型（PC_API、APP_API、PC整合），二維紀錄測試method名稱
    :param user_name: String; 就是個用戶名
    :param test_env: String; 網域名稱，用於Config.encConfig初始化
    :param is_use_red: String; yse or no; 目前未使用
    :return: 
    """
    logger = create_logger(r'\AutoTest', 'auto_test')
    logger.info("suite_test 初始化")
    _env_config = Config.EnvConfig(test_env)
    _env_config_app = Config.EnvConfigApp(test_env)
    _env_app_config = Config.EnvConfigApp(test_env)
    _suite_list = []
    _test_list = ['cqssc', 'xjssc', 'hljssc', 'shssl', 'tjssc', 'txffc', 'fhjlssc', 'fhcqc', 'fhxjc', '3605fc',
                  'btcffc', 'llssc', '360ffc', 'jlffc', 'v3d']
    logger.debug(f'autoTest test_cases : {test_cases}')
    try:
        suite = unittest.TestSuite()
        _conn = None
        _conn2 = None

        logger.info(f"suite_test with test_cases : {test_cases}")

        if _env_config.get_env_id() in (0, 1):
            _conn = OracleConnection(_env_config.get_env_id())
            _conn2 = MysqlConnection(_env_config.get_env_id())
            for case in test_cases[0]:
                _suite_list.append(
                    ApiTestPC(case=case, env_config=_env_config, _user=user_name, red_type=is_use_red,
                              money_unit=money_unit, award_mode=award_mode, oracle=_conn, mysql=_conn2))
            for case in test_cases[1]:
                _suite_list.append(ApiTestApp(case_=case, env_config=_env_config_app, user=user_name,
                                              red_type=is_use_red, oracle=_conn, mysql=_conn2))
            for case in test_cases[2]:
                if case == 'test_plan':
                    for lottery in _test_list:
                        _suite_list.append(
                            IntegrationTestWeb(case=f'test_{lottery}', env_config=_env_config, user=user_name,
                                               red_type=is_use_red))
                else:
                    _suite_list.append(
                        IntegrationTestWeb(case=case, env_config=_env_config, user=user_name, red_type=is_use_red))
        elif _env_config.get_env_id() == 11:  # 若為YFT測試案例
            _conn = PostgresqlConnection()  # 建立共用的DB連線
            for case in test_cases[0]:
                _suite_list.append(ApiTestPC_YFT(case=case, env_config=_env_config, user=user_name,
                                                 money_unit=money_unit, _award_mode=award_mode, conn=_conn))
            for case in test_cases[1]:
                _suite_list.append(ApiTestAPP_YFT(case=case, env_config=_env_config, user=user_name,
                                                  money_unit=money_unit, award_mode=award_mode, conn=_conn))

        logger.info(f"測試內容 suite_list : {_suite_list}")

        suite.addTests(_suite_list)
        logger.info(f"測試內容Suite suite_api_pc : {suite}")

        filename = Config.reportHtml_Path  # now + u'自動化測試' + '.html'
        fp = open(filename, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'測試報告',
            description=f'環境: {_env_config.get_domain()},　　帳號: {user_name}',
        )
        logger.debug(">>>>>>>>Test Start.<<<<<<<<")
        runner.run(suite)
        logger.debug(">>>>>>>>Test End.<<<<<<<<")

        fp.close()
        _conn.close_conn()
        if _conn2 is not None:
            _conn2.close_conn()
    except Exception as e:
        logger.error(trace_log(e))
