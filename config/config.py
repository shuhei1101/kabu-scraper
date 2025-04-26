import os

config_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(config_dir)
source_dir = os.path.join(project_dir, 'source')

# ファイル名
XLSX_NAME = '配当管理.xlsx'

# Excelファイルのパス
XLSX_PATH = os.path.join(source_dir, XLSX_NAME)

# 銘柄コードのカラム名
STOCK_CODE_COLUMN = '銘柄コード'


