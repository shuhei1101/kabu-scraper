import os
import pandas as pd

# stock_table.tsv のパス（定数）
src_dir = os.path.dirname(os.path.dirname(__file__))
project_root = os.path.dirname(src_dir)
input_dir = os.path.join(project_root, 'input')

TSV_PATH = os.path.join(input_dir, 'stock_table.tsv')

class StockTsvHandler:
    '''stock_table.tsv を操作するクラス'''

    def __init__(self):
        self.df = pd.read_csv(TSV_PATH, sep='\t')

    def get_record_by_id(self, stock_code: str):
        '''id（コード）を指定してレコード取得'''
        match = self.df[self.df['コード'].astype(str) == str(stock_code)]
        if match.empty:
            raise ValueError(f"コード '{stock_code}' のレコードが見つかりません。")
        record = match.iloc[0]
        return record

    def update_record(self, updated_record: pd.Series):
        '''レコードを渡して一行更新'''
        idx = self.df[self.df['コード'].astype(str) == str(updated_record['コード'])].index
        if idx.empty:
            raise ValueError(f"コード '{updated_record['コード']}' のレコードが存在しません。")
        self.df.loc[idx[0]] = updated_record
        self.df.to_csv(TSV_PATH, sep='\t', index=False)

# 動作確認用
if __name__ == "__main__":
    handler = StockTsvHandler()
    try:
        record = handler.get_record_by_id('2801')
        print("取得したレコード:", record)
        
        # 更新するレコードの例
        record['銘柄'] = 'test'
        handler.update_record(record)
    except ValueError as e:
        print(e)
