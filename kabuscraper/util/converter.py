def to_unit_billion(value: str) -> str:
    """◯兆◯億円"や"◯億円"を○○億円の単位に変換

    1兆100億円→11,000億円
    100億円→100億円
    1,000億円→1000億円
    """
    # 兆を億に変換
    value = value.replace(",", "")  # カンマを削除
    trillion, billion = 0, 0
    if "兆" in value:
        parts = value.split("兆")
        trillion = int(parts[0]) * 10000
        if "億" in parts[1]:
            billion = int(parts[1].replace("億円", ""))
    elif "億" in value:
        billion = int(value.replace("億円", ""))

    total_billion = trillion + billion
    return f"{total_billion}億円"


def str_to_billion(s: str) -> float:
    """◯兆◯億円"や"◯億円"を数値型に変換 (小数点以下にも対応)"""
    try:
        s = s.replace(",", "")  # カンマを削除
        trillion, billion = 0, 0
        if "兆" in s:
            parts = s.split("兆")
            trillion = float(parts[0]) * 1000000000000
            if "億" in parts[1]:
                billion = float(parts[1].replace("億円", "")) * 100000000
        elif "億" in s:
            billion = float(s.replace("億円", "")) * 100000000

        return float(trillion + billion)
    except ValueError:
        # 変換できない場合は0.0を返す
        return 0.0


def str_to_float(s: str) -> float:
    """数値をfloat型に変換

    例: "1,234.56" → 1234.56
    例: "1,234" → 1234.0
    例: "ー" → 0.0
    """
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return 0.0


# 動作確認用
if __name__ == "__main__":
    # 例
    test_values = [
        "1兆100億円",
        "12兆1234.1億円",
    ]
    for value in test_values:
        print(f"Original: {value} -> Integer: {str_to_billion(value)}")
