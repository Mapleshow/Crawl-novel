import requests
from lxml import html
etree = html.etree
url = "http://www.xbiquge.la"


class Spider_Crawl():
    # 获取数据
    def get_url(self, url):
        # 访问这个网址
        headers = {
            'Mozilla/5.0 ': '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69'
        }
        r = requests.get(url, headers=headers)
        # r.encoding = "utf-8"
        r.encoding = r.apparent_encoding
        html = r.text
        return html

    def myself_parse(self, html, x):
        # 提取主页面小说以及url
        r = etree.HTML(html)
        vote_name = r.xpath(x)
        return vote_name

    def parse(self, html):
        # 提取主页面小说以及url
        r = etree.HTML(html)
        # xpath进行匹配
        vote_name = r.xpath("//div[@id='newscontent']//div[@class='r']//li//span[@class='s2']//a/text()")
        # print("小说名:",vote_name)
        vote_url = r.xpath("//div[@id='newscontent']//div[@class='r']//li//span[@class='s2']//a/@href")
        # print("小说url:", vote_url)
        # 变成字典的数据
        d = dict(zip(vote_name, vote_url))
        # print('寻找到的数据', d)
        return d

    def detail_parse(self, html):
        # 每一个小说详细章节的解析
        r = etree.HTML(html)
        # xpath进行匹配
        vote_list_name = r.xpath("//div[@class='box_con']//dl//dd//a/text()")
        vote_list_url = r.xpath("//div[@class='box_con']//dl//dd//a/@href")
        # 编程字典的数据
        d = dict(zip(vote_list_name, vote_list_url))
        return d

    def read_parse(self, html):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        # xpath进行匹配
        content = r.xpath("//div[@class='content_read']//div[@id='content']/text()")
        # 定义一个空字符串
        h_str = ""
        for i in content:
            h_str += i
        return h_str


if __name__ == '__main__':
    spider = Spider_Crawl()
    html = spider.get_url(url)
    detail_vote = spider.parse(html)
    print(detail_vote)
