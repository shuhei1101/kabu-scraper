import requests
from lxml import html
from bs4 import BeautifulSoup

from kabuscraper.util.converter import str_to_billion, str_to_float


# XPathで値を抽出するスクレイパークラス
class KabuScraper:
    """XPathで値を抽出するスクレイパークラス"""

    cache: dict[str, str] = {}  # URLとレスポンスをキャッシュする辞書

    def __init__(self, stock_code):
        self.stock_code = stock_code
        self._register_cache(f"https://kabutan.jp/stock/?code={self.stock_code}")
        self._register_cache(f"https://minkabu.jp/stock/{self.stock_code}/dividend")
        self._register_cache(f"https://minkabu.jp/stock/{self.stock_code}/yutai")

    def scrape(self, target):
        """対象を指定して値を取得"""

        try:
            result = None

            if target == "銘柄":
                url = f"https://kabutan.jp/stock/?code={self.stock_code}"
                xpath = '//*[@id="stockinfo_i1"]/div[1]/h2/text()'
                result = self._get_data(url, xpath)[0]

            elif target == "株価(円)":
                url = f"https://kabutan.jp/stock/?code={self.stock_code}"
                xpath = '//*[@id="kobetsu_left"]/table[1]/tbody/tr[4]/td[1]'
                td = self._get_data(url, xpath)[0]
                raw_value = td.text_content().strip()
                result = str_to_float(raw_value)

            elif target == "権利確定月":
                url = f"https://minkabu.jp/stock/{self.stock_code}/dividend"
                xpath = '//*[@id="contents"]/div[3]/section[1]/div[2]/div/div[3]/div[1]/table'
                table = self._get_data(url, xpath)[0]
                result = (
                    table.xpath(".//tr")[2].xpath(".//td")[0].text_content().strip()
                )

            elif target == "配当金(円／株)":
                url = f"https://minkabu.jp/stock/{self.stock_code}/dividend"
                soup = self._get_soup(url)
                # xpath = '//*[@id="dps_detail"]/div[2]/div/div[6]/table[2]/tbody/tr[1]/td[4]'
                raw_value = (
                    soup.find(id="dps_detail")
                    .find_all("table")[1]
                    .find_all("tbody")[0]
                    .find_all("tr")[0]
                    .find_all("td")[-1]
                    .text
                )
                result = str_to_float(raw_value)

            elif target == "予想配当金(円／株)":
                url = f"https://minkabu.jp/stock/{self.stock_code}/dividend"
                soup = self._get_soup(url)
                # xpath = '//*[@id="dps_detail"]/div[2]/div/div[6]/table[2]/tbody/tr[1]/td[4]'
                raw_value = (
                    soup.find(id="dps_detail")
                    .find_all("table")[0]
                    .find_all("tbody")[0]
                    .find_all("tr")[0]
                    .find_all("td")[-1]
                    .text
                )
                result = str_to_float(raw_value)

            elif target == "株主優待":
                url = f"https://minkabu.jp/stock/{self.stock_code}/yutai"
                xpath = '//*[@id="yutai_summary"]'
                h3 = self._get_data(url, xpath)[0]
                result = h3.text_content().strip()

            elif target == "時価総額":
                url = f"https://kabutan.jp/stock/?code={self.stock_code}"
                soup = self._get_soup(url)
                raw_value = (
                    soup.find(id="stockinfo_i3")
                    .find_all("table")[0]
                    .find_all("tbody")[0]
                    .find_all("tr")[1]
                    .find_all("td")[0]
                    .text
                )
                result = str_to_billion(raw_value)

            elif target == "URL":
                url = f'=HYPERLINK("https://minkabu.jp/stock/{self.stock_code}")'
                result = url

            else:
                raise ValueError(
                    f"モジュール'KabuScraper'に'{target}'の設定がありません。"
                )

            return result
        except ValueError as e:
            raise
        except Exception as e:
            raise

    def _get_data(self, url, xpath):
        """指定したURLのHTMLを取得し、XPathで値を抽出する"""
        response = self._get_response(url)
        tree = html.fromstring(response.content)
        return tree.xpath(xpath)

    def _get_soup(self, url):
        """指定したURLのHTMLを取得し、BeautifulSoupオブジェクトを返す"""
        response = self._get_response(url)
        return BeautifulSoup(response.content, "html.parser")

    def _get_response(self, url):
        if url in KabuScraper.cache:
            return KabuScraper.cache[url]
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(
                f"URL '{url}' にアクセスできません。ステータスコード: {response.status_code}"
            )
        KabuScraper.cache[url] = response
        self.cache[url] = response
        return response

    def _register_cache(self, url):
        """URLからレスポンスをキャッシュに登録する"""
        if url not in KabuScraper.cache:
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError(
                    f"URL '{url}' にアクセスできません。ステータスコード: {response.status_code}"
                )
            KabuScraper.cache[url] = response


# 動作確認用
if __name__ == "__main__":
    scraper = KabuScraper(stock_code="7261")
    try:
        result = scraper.scrape("URL")
        print(result)
        print(type(result))
    except ValueError as e:
        print(e)
