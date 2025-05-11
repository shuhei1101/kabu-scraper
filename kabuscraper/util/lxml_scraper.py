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
        if hasattr(value, "text"):
            value = value.text
        return value

    def get_table(self, xpath):
        tables = self.tree.xpath(xpath)
        if not tables:
            return None
        table = tables[0]  # 最初のtableを対象
        rows = []
        for tr in table.xpath(".//tr"):
            row = [td.text_content().strip() for td in tr.xpath(".//th|.//td")]
            rows.append(row)
        return rows


if __name__ == "__main__":
    url = "https://minkabu.jp/stock/9022/dividend"
    xpath = '//*[@id="contents"]/div[3]/section[1]/div[2]/div/div[3]/div[1]/table'
    scraper = LxmlScraper(url)
    # value = scraper.get_value(xpath)
    value = scraper.get_table(xpath)
    print(f"Value: {value}")
