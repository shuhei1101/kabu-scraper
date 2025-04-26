import os
import pandas as pd

src_dir = os.path.dirname(os.path.dirname(__file__))
project_root = os.path.dirname(src_dir)
config_dir = os.path.join(project_root, 'config')

CONFIG_PATH = os.path.join(config_dir, 'column_config.csv')

class ColumnConfigReader:
    # 設定ファイルのパス（定数）

    def __init__(self):
        self.df = pd.read_csv(CONFIG_PATH)

    # 指定カラムの設定行を取得（複数あっても1件目だけ返す）
    def get_config_by_column(self, column: str, stock_code: str) -> pd.Series:
        '''
        :raise 
        '''
        match = self.df[self.df['column'] == column]
        if match.empty:
            return None
        record = match.iloc[0].copy()

        # URL内の{stock_code}を置換
        record['url'] = record['url'].format(stock_code=stock_code)
        return record

# 動作確認
if __name__ == "__main__":
    reader = ColumnConfigReader()
    try:
        config = reader.get_config_by_column("株価", "7203")
        print(f"URL: {config['url']}, XPath: {config['xpath']}")
    except ValueError as e:
        print(e)