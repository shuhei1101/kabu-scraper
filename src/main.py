import os
import sys
import traceback
import asyncio

src_dir = os.path.dirname(__file__)
project_root = os.path.dirname(src_dir)
config_dir = os.path.join(project_root, 'config')
sys.path.append(config_dir)

import config
from config_manager.stock_xlsx_handler import StockXlsxHandler
from logger.my_logger import MyLogger
from kabu_scraper import KabuScraper

async def main():
    """メイン関数"""
    try:
        print("\n" * 3)
        MyLogger().info(f"KabuScraper を実行")

        xlsx_path = config.XLSX_PATH
        if not os.path.exists(xlsx_path):
            print(f"`{config.XLSX_PATH}`にファイルが存在しません。config/config.pyを確認してください。")
            print("処理を終了します。")
            return

        print(f"選択されたファイル: {xlsx_path}")
        

        handler = StockXlsxHandler(
            xlsx_path=xlsx_path,
            key=config.STOCK_CODE_COLUMN,
        )
        stock_codes = handler.get_key_data()

        tasks = [
            process_stock_code(stock_code, handler)
            for stock_code in stock_codes
        ]
        print(f"スクレイピング中...")
        await asyncio.gather(*tasks)

        MyLogger().info("KabuScraper の実行が完了")
        

    except Exception as e:
        print(f"不明なエラーが発生しました。処理を終了します。")
        exc_type, exc_value, exc_tb = sys.exc_info()
        MyLogger().critical(traceback_to_json(exc_type, exc_value, exc_tb))
    
    print("\n" * 3)

async def process_stock_code(stock_code, handler: StockXlsxHandler):
    """銘柄コードを非同期で処理"""
    MyLogger().debug(f"銘柄コード '{stock_code}' のスクレイピングを開始します。")

    scraper = KabuScraper(stock_code)
    record = handler.get_record(key=stock_code)

    async def process_column(column):
        try:
            MyLogger().debug(f"銘柄コード '{stock_code}' の '{column}' をスクレイピング中...")
            value = await asyncio.to_thread(scraper.scrape, column)
        except ValueError as e:
            MyLogger().debug(e)
            return column, None
        except Exception as e:
            MyLogger().debug(f"'{stock_code}' の '{column}' のスクレイピングに失敗しました。空白で初期化します。")
            return column, ""

        if value is None:
            MyLogger().debug(f"取得した値が None です。スキップします。")
            return column, None

        MyLogger().debug(f"銘柄コード'{stock_code}' の '{column}' を '{value}' に更新しました。")
        return column, value

    tasks = [process_column(column) for column in record.index]
    results = await asyncio.gather(*tasks)

    for column, value in results:
        if value is not None:
            record[column] = value
    
    MyLogger().debug(f"銘柄コード '{stock_code}' のスクレイピングが完了しました。")

    try:
        handler.update_record(record)
    except ValueError as e:
        MyLogger().debug(e)

def traceback_to_json(exc_type, exc_value, exc_tb):
    """スタックトレースをjson形式に変換する"""
    stack_trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    return {
        "type": str(exc_type),
        "value": str(exc_value),
        "traceback": stack_trace
    }

if __name__ == "__main__":
    asyncio.run(main())
