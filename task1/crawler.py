import requests
import os
from lxml import etree
from io import StringIO


def parse(url):
    resp = requests.get(url, headers={'Content-Type': 'text/html'})
    return resp.text


html = parse('https://www.notebookcheck-ru.com/Novosti.news.0.html?&items_per_page=100')
htmlparser = etree.HTMLParser()
tree = etree.parse(StringIO(html), htmlparser)
links = tree.xpath('//a[@class="introa_large introa_news"]/@href')

os.makedirs("data", exist_ok=True)
index = open("data/index.txt", "w+", encoding='utf-8')
for i, link in enumerate(links):
    html_source = parse(link)
    with open("data/" + str.format("{}.html".format(i)), 'w', encoding='utf-8') as f:
        f.write(html_source)
    index.write("{} - {}\n".format(i, link))

index.close()
