import tkinter as tk
from tkinter import filedialog

def get_path_with_dialog():
    """ファイル選択ダイアログを表示して、選択されたファイルのパスを返す"""

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする

    file_path = filedialog.askopenfilename(
        title="'配当管理.xlsx'を選択してください",
        filetypes=[("Excel files", "*.xlsx")]
    )

    return file_path

def dialog_message(message):
    """ポップアップでメッセージを表示する"""

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする

    tk.messagebox.showinfo("メッセージ", message)

# 動作確認用
if __name__ == "__main__":
    # path = get_path_with_dialog()
    # print(f"選択されたファイルのパス: {path}")
    dialog_message("処理が完了しました。")