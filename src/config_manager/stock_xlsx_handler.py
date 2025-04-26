import pandas as pd

class StockXlsxHandler:
    '''stock_table.xlsx を操作するクラス'''

    def __init__(self, xlsx_path, key):
        '''
        :raise ValueError: 指定したキーが存在しない場合
        '''
        self.xlsx_path = xlsx_path
        self.key = key
        self.df = pd.read_excel(xlsx_path, engine='openpyxl')

        # キーの存在確認
        if self.key not in self.df.columns:
            raise ValueError(f"キー '{self.key}' は存在しません。")

    def get_record(self, key: str):
        '''id（コード）を指定してレコード取得'''
        match = self.df[self.df[self.key].astype(str) == str(key)]
        if match.empty:
            raise ValueError(f"コード '{key}' のレコードが見つかりません。")
        record = match.iloc[0]
        return record
    
    def get_key_data(self):
        '''キーのデータを取得'''
        if self.key not in self.df.columns:
            raise ValueError(f"キー '{self.key}' は存在しません。")
        return self.df[self.key].tolist()
    
    def get_column_data(self, column_name: str):
        '''指定したカラムのデータを取得'''
        if column_name not in self.df.columns:
            raise ValueError(f"カラム '{column_name}' は存在しません。")
        return self.df[column_name].tolist()

    def update_record(self, updated_record: pd.Series):
        '''レコードを渡して一行更新'''
        idx = self.df[self.df[self.key].astype(str) == str(updated_record[self.key])].index
        if idx.empty:
            raise ValueError(f"コード '{updated_record[self.key]}' のレコードが存在しません。")
        self.df.loc[idx[0]] = updated_record
        self.df.to_excel(self.xlsx_path, index=False, engine='openpyxl')

# 動作確認用
if __name__ == "__main__":
    handler = StockXlsxHandler(
        xlsx_path='input/配当管理.xlsx',
        key='銘柄コード'  # 銘柄コードをキーに指定
    )
    try:
        record = handler.get_record('2801')
        print("取得したレコード:", record)
        
        stock_codes = handler.get_key_data()
        print("銘柄コードのリスト:", stock_codes)

        # 更新するレコードの例
        # record['銘柄'] = 'testest'
        # handler.update_record(record)
    except ValueError as e:
        print(e)
