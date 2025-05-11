from setuptools import setup, find_packages

setup(
    name="kabu-scraper",  # パッケージ名
    version="0.1",  # バージョン番号（公開しない場合は削除可能）
    packages=find_packages(
        exclude=["tests", "tests.*"]  # テスト関連のパッケージを除外
    ),
    test_suite="tests",  # テストスイートの指定
)
