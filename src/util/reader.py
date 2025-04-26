import tkinter as tk
from tkinter import filedialog

def get_path_with_dialog():
    """ファイル選択ダイアログを表示して、選択されたファイルのパスを返す"""

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする

    file_path = filedialog.askopenfilename(
        title="ファイルを選択してください",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )

    return file_path

# 動作確認用
if __name__ == "__main__":
    path = get_path_with_dialog()
    print(f"選択されたファイルのパス: {path}")