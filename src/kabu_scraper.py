import requests
from lxml import html
from bs4 import BeautifulSoup

# XPathで値を抽出するスクレイパークラス
class KabuScraper:

    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.cache = {}  # URLとレスポンスをキャッシュする辞書

    def scrape(self, target):
        """対象を指定して値を取得"""

        try:
            result = None

            if target == '銘柄':
                url = f"https://kabutan.jp/stock/?code={self.stock_code}"
                xpath = '//*[@id="stockinfo_i1"]/div[1]/h2/text()'
                result = self._get_data(url, xpath)[0]

            elif target == '株価(円)':
                url = f"https://kabutan.jp/stock/?code={self.stock_code}"
                xpath = '//*[@id="kobetsu_left"]/table[1]/tbody/tr[4]/td[1]'
                td = self._get_data(url, xpath)[0]
                result = td.text_content().strip()

            elif target == '権利確定月':
                url = f"https://minkabu.jp/stock/{self.stock_code}/dividend"
                xpath = '//*[@id="contents"]/div[3]/section[1]/div[2]/div/div[3]/div[1]/table'
                table = self._get_data(url, xpath)[0]
                result = table.xpath('.//tr')[2].xpath('.//td')[0].text_content().strip()

            elif target == '配当金(円／株)':
                url = f"https://kabutan.jp/stock/?code={self.stock_code}"
                xpath = '//*[@id="kobetsu_right"]/div[3]/table[1]/tbody/tr[3]/td[5]'
                td = self._get_data(url, xpath)[0]
                result = td.text_content().strip()

            elif target == '株主優待':
                url = f"https://minkabu.jp/stock/{self.stock_code}/yutai"
                xpath = '//*[@id="yutai_summary"]'
                h3 = self._get_data(url, xpath)[0]
                result = h3.text_content().strip()

            elif target == '時価総額':
                url = f"https://kabutan.jp/stock/?code={self.stock_code}"
                soup = self._get_soup(url)
                result = soup.find(id='stockinfo_i3').find_all('table')[0].find_all('tbody')[0].find_all('tr')[1].find_all('td')[0].text

            else:
                raise ValueError(f"モジュール'KabuScraper'に'{target}'の設定がありません。")
                
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
        return BeautifulSoup(response.content, 'html.parser')
    
    def _get_response(self, url):
        """URLに対するレスポンスをキャッシュから取得または新規取得する"""
        if url in self.cache:
            return self.cache[url]
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to load page: {url}")
        self.cache[url] = response
        return response
    

# 動作確認用
if __name__ == "__main__":
    scraper = KabuScraper(stock_code="4042")
    try:
        result = scraper.scrape('銘柄')
        print(result)
    except ValueError as e:
        print(e)
