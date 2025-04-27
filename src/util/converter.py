def to_unit_billion(value: str) -> str:
    '''◯兆◯億円"や"◯億円"を○○億円の単位に変換
    
    1兆100億円→11,000億円
    100億円→100億円
    1,000億円→1000億円
    '''
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


# 動作確認用
if __name__ == "__main__":
    # 1兆1,100億円→11000億円
    print(to_unit_billion("1兆1,100億円"))  # 11000億円
    # 100億円→100億円
    print(to_unit_billion("100億円"))  # 100億円
    # 1兆0億円→1000億円
    print(to_unit_billion("1兆0億円"))  # 1000億円
    # 0兆100億円→100億円
    print(to_unit_billion("0兆100億円"))  # 100億円