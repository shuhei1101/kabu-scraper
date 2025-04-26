import requests
from lxml import html

# XPathで値を抽出するスクレイパークラス
class LxmlScraper:
    def __init__(self, url):
        response = requests.get(url)
        self.tree = html.fromstring(response.content)

    # XPathを指定して要素を取得
    def get_value(self, xpath):
        result = self.tree.xpath(xpath)
        if isinstance(result, list):
            if len(result) == 0:
                return None
            value = result[0]
        else:
            value = result
        # 要素の場合はテキストに変換
        if hasattr(value, 'text'):
            value = value.text
        return value

if __name__ == "__main__":
    url = "https://kabutan.jp/stock/?code=9022"
    xpath = "//*[@id='kobetsu_left']/table[1]/tbody/tr[4]/td[1]"
    scraper = LxmlScraper(url)
    value = scraper.get_value(xpath)
    print(f"Value: {value}")
