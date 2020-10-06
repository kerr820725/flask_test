import logging
import pathlib

from datetime import datetime

dir_path = project_path = str(pathlib.Path(__file__).parent.parent.absolute()) + r"\logs"

filename = "{:%Y-%m-%d}".format(datetime.now()) + '.log'  # 設定檔名


def create_logger(log_folder, log_name):
    # config
    logging.captureWarnings(True)  # 捕捉 py waring message
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    my_logger = logging.getLogger(log_name)  # 捕捉 py waring message
    my_logger.setLevel(logging.INFO)

    # # 若不存在目錄則新建
    # if not os.path.exists(dir_path + log_folder):
    #     os.makedirs(dir_path + log_folder)
    #
    # # file handler
    # fileHandler = logging.FileHandler(dir_path + log_folder + '/' + filename, 'w', 'utf-8')
    # fileHandler.setFormatter(formatter)
    # my_logger.addHandler(fileHandler)

    # console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(formatter)
    my_logger.addHandler(consoleHandler)

    return my_logger
