import logging
import os

src_dir = os.path.dirname(__file__)
project_root = os.path.dirname(src_dir)
log_dir = os.path.join(project_root, 'log')


# logger
class MyLogger:
    '''シングルトンでロガーを管理するクラス'''
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MyLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'logger'):
            return
        # ログディレクトリが存在しない場合は作成
        os.makedirs(log_dir, exist_ok=True)

        # ログファイルのパスを指定
        log_file_path = os.path.join(log_dir, 'app.log')

        # ロガーの設定
        self.logger = logging.getLogger('MyLogger')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # コンソール出力の設定
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # ch.setFormatter(formatter)
        # self.logger.addHandler(ch)

        # ファイル出力の設定
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# 動作確認
if __name__ == "__main__":
    MyLogger().info("This is an info message.")
    MyLogger().error("This is an error message.")
    MyLogger().debug("This is a debug message.")
    MyLogger().warning("This is a warning message.")
    MyLogger().critical("This is a critical message.")