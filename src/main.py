import os
import sys
import traceback
import asyncio
import time  # 実行時間計測用

src_dir = os.path.dirname(__file__)
project_root = os.path.dirname(src_dir)
config_dir = os.path.join(project_root, 'config')
sys.path.append(config_dir)

import app_config
from config_manager.stock_xlsx_handler import StockXlsxHandler
from logger.my_logger import MyLogger
from kabu_scraper import KabuScraper

async def main():
    """メイン関数"""

    start_time = time.time()  # 開始時刻を記録
    try:
        print("\n" * 3)
        MyLogger().info(f"KabuScraper を実行")

        xlsx_path = app_config.XLSX_PATH
        if not os.path.exists(xlsx_path):
            print(f"`{app_config.XLSX_PATH}`にファイルが存在しません。config/config.pyを確認してください。")
            print("処理を終了します。")
            return

        MyLogger().info(f"選択されたファイル: {xlsx_path}")
        

        handler = StockXlsxHandler(
            xlsx_path=xlsx_path,
            key=app_config.ELXS_KEY,
        )
        nos = handler.get_keys()
        tasks = [
            process_row(no, handler)
            for no in nos
            if isinstance(no, float)
        ]
        await asyncio.gather(*tasks)

    except Exception:
        MyLogger().info(f"不明なエラーが発生しました。処理を終了します。")
        exc_type, exc_value, exc_tb = sys.exc_info()
        MyLogger().critical(traceback_to_json(exc_type, exc_value, exc_tb))
    
    finally:
        print("\n" * 3)
        MyLogger().info("KabuScraper の実行が完了")
        end_time = time.time()  # 終了時刻を記録
        elapsed_time = end_time - start_time
        MyLogger().info(f"合計処理時間: {elapsed_time:.2f} 秒")

    print("\n" * 3)

async def process_row(no, handler: StockXlsxHandler):
    """銘柄コードを非同期で処理"""
    try:
        record = handler.get_record(key=no)

        is_update = record["更新"] == "◯"
        if not is_update:   
            MyLogger().debug(f"No '{no}' は更新不要なため、スキップします。")
            return
        else:
            MyLogger().debug(f"No '{no}' のスクレイピングを開始します。")

        scraper = KabuScraper(record["銘柄コード"])

        tasks = [process_column(column, record["銘柄コード"], scraper) for column in record.index]
        results = await asyncio.gather(*tasks)

        for column, value in results:
            if value is not None:
                record[column] = value
        
        handler.update_record(record)
        MyLogger().debug(f"銘柄コード '{no}' のスクレイピングが完了しました。")
    except Exception:
        MyLogger().info(f"不明なエラーが発生しました。")
        exc_type, exc_value, exc_tb = sys.exc_info()
        MyLogger().critical(traceback_to_json(exc_type, exc_value, exc_tb))

async def process_column(column, stock_code, scraper: KabuScraper):
    """銘柄コードの各列を非同期で処理"""
    try:
        MyLogger().debug(f"銘柄コード '{stock_code}' の '{column}' をスクレイピング中...")
        value = await asyncio.to_thread(scraper.scrape, column)
    except ValueError as e:
        # 設定がない場合はスキップ
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
