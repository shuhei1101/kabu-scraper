import os
import sys
import traceback

src_dir = os.path.dirname(__file__)
project_root = os.path.dirname(src_dir)
config_dir = os.path.join(project_root, 'config')
sys.path.append(config_dir)

import config
from config_manager.stock_xlsx_handler import StockXlsxHandler
from util.reader import dialog_message, get_path_with_dialog
from logger.my_logger import MyLogger
from kabu_scraper import KabuScraper

def main():
    """メイン関数"""

    try:
        # ファイル選択ダイアログを表示して、選択されたファイルのパスを取得
        xlsx_path = get_path_with_dialog()

        if not xlsx_path:
            MyLogger().info("ファイルが選択されませんでした。処理を終了します。")
            return
        
        handler = StockXlsxHandler(
            xlsx_path=xlsx_path,
            key=config.STOCK_CODE_COLUMN,
        )
        # スクレイピング対象の銘柄コード一覧を取得
        stock_codes = handler.get_key_data()

        print("\n" * 3)
        MyLogger().info(f"--- KabuScraperを実行します。---")
         
        for i, stock_code in enumerate(stock_codes, start=1):
            # 進捗をログに出力
            print(f"処理中({i}/{len(stock_codes)})")
            
            # コードを指定してレコードを取得
            record = handler.get_record(key=stock_code)
            scraper = KabuScraper(stock_code)

            for column in record.index:
                # スクレイピングを実行
                try:
                    value = scraper.scrape(column)
                except ValueError as e:
                    MyLogger().debug(e)
                    continue
                except Exception as e:
                    # スクレイピングに失敗した場合は、空文字で初期化
                    MyLogger().debug(f"'{stock_code}' の '{column}' のスクレイピングに失敗しました。空白で初期化します。")
                    value = ""

                if value is None:
                    MyLogger().debug(f"取得した値が None です。スキップします。")
                    continue

                # 取得した値を更新
                record[column] = value
                MyLogger().debug(f"銘柄コード'{stock_code}' の '{column}' を '{value}' に更新しました。")
                
            # レコードを更新
            handler.update_record(record)
        MyLogger().info("--- KabuScraperの実行が完了しました。 ---")
        
        # ポップアップで完了とダイアログを表示
        dialog_message("--- KabuScraperの実行が完了しました。 ---")
        
    except Exception as e:
        # 例外のスタックトレースを取得
        exc_type, exc_value, exc_tb = sys.exc_info()
        # スタックトレースをログに出力
        MyLogger().critical(traceback_to_json(exc_type, exc_value, exc_tb))

def traceback_to_json(exc_type, exc_value, exc_tb):
    """スタックトレースをjson形式に変換する"""
    stack_trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    return {
        "type": str(exc_type),
        "value": str(exc_value),
        "traceback": stack_trace
    }

if __name__ == "__main__":
    main()