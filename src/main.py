import os
import sys

from config_manager.column_config_reader import ColumnConfigReader
from lxml_scraper import LxmlScraper
from my_logger import MyLogger

src_dir = os.path.dirname(__file__)
project_root = os.path.dirname(src_dir)
config_dir = os.path.join(project_root, 'config')
sys.path.append(config_dir)
import config

from config_manager.stock_xlsx_handler import StockXlsxHandler
from util.reader import get_path_with_dialog


def main():
    """メイン関数"""

    # ファイル選択ダイアログを表示して、選択されたファイルのパスを取得
    xlsx_path = get_path_with_dialog()
    
    # StockXlsxHandler を初期化
    handler = StockXlsxHandler(
        xlsx_path=xlsx_path,
        key=config.STOCK_CODE_COLUMN,
    )

    stock_codes = handler.get_key_data()

    column_config_reader = ColumnConfigReader()

    for stock_code in stock_codes:
        # コードを指定してレコードを取得
        try:
            MyLogger().debug(f"'{stock_code}' のレコードを取得中...")
            record = handler.get_record(key=stock_code)

            for column in record.index:
                # カラムの設定情報を取得
                column_info = column_config_reader.get_config_by_column(
                    column=column,
                    stock_code=stock_code
                )
                if column_info is None:
                    MyLogger().debug(f"カラム '{column}' の設定が見つかりません。")
                    continue
                if column_info['is_enable'] == 0:
                    MyLogger().debug(f"カラム '{column}' をスキップします。")
                    continue

                # スクレイピングを使用し、データを取得
                value = LxmlScraper(column_info['url']).get_value(column_info['xpath'])
                MyLogger().debug(f"'{column}' のデータを取得しました。値: {value}")

                # 取得した値が None の場合はスキップ
                if value is None:
                    MyLogger().debug(f"取得した値が None です。スキップします。")
                    continue

                # 取得した値を更新
                record[column] = value
                
            # レコードを更新
            handler.update_record(record)

        except ValueError as e:
            MyLogger().error(e)

if __name__ == "__main__":
    main()