import requests
from bs4 import BeautifulSoup
import json


"""catch keywords by using requests"""
# base of Url
base_url = 'http://news.baidu.com/n?m=rddata&v=hot_word'
hot_type = '0'

parameters = {'type': hot_type}

# Get Json data
r = requests.get(base_url, params=parameters)
print(r.url)

hot_words_dict = r.json()

# print hot words
for hot_word in hot_words_dict.get('data'):
    print(hot_word.get('query_word'))

""" Add date"""
#  YYYYMMDD: 20171122

hot_type = '2'   # 国内
hot_date = '20171122'

parameters = {'type': hot_type, 'date': hot_date}

# Get Json data
r = requests.get(base_url, params=parameters)
print(r.url)

hot_words_dict = r.json()

# print hot words
for hot_word in hot_words_dict.get('data'):
    print(hot_word.get('query_word'))


"""fetch news by using keywords"""
# base of url: [http://news.baidu.com/ns?tn=news](http://news.baidu.com/ns?tn=news)， parameters: word。

query_word = '留学生'
news_base_url = 'http://news.baidu.com/ns?tn=news'

parameters = {'word': query_word}

# Get Json data
r = requests.get(news_base_url, params=parameters)
print(r.url)

soup = BeautifulSoup(r.text, 'lxml')   # lxml change to other parser packages
news_html_list = soup.select('div.result')
news_list = []
for news_html in news_html_list:
    news = {}
    news['标题'] = news_html.a.get_text().strip()
    news['链接'] = news_html.a['href']
    source = news_html.find('p', 'c-author').get_text().strip().replace('\xa0\xa0', ' ').split(' ')
    news['来源'] = source[0]
    news['发布日期'] = source[1]

    news_list.append(news)

for news in news_list:
    print(json.dumps(news, ensure_ascii=False))
