import aiohttp
from bs4 import BeautifulSoup as bs


class MySoup:
    def __init__(self):
        self.host = 'https://mospolytech.ru/'
        self.url = "https://mospolytech.ru/news"

    async def download(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session)
            return await self.parser(html)

    async def fetch(self, session):
        async with session.get(self.url) as response:
            return await response.read()

    async def parser(self, html):
        soup = bs(html, 'lxml')
        html_file = soup.find("div", class_="card-news-wide-list")
        my_news_dict = {}
        list_of_news = reversed(html_file.find_all("div", class_="card-news-wide"))
        for news in list_of_news:
            myimgs = news.find("img")
            if myimgs:
                date = " ".join([part_of_date.text.strip() for part_of_date in news.find_all("span")])
                my_news_dict[myimgs["alt"]] = {
                    "href": self.host + news.find("a")["href"],
                    "img": self.host + myimgs["data-src"],
                    "text": myimgs["alt"],
                    "date": date
                }
        return my_news_dict
