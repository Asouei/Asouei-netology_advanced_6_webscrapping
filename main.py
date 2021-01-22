import requests
from bs4 import BeautifulSoup
import re


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
main_link = requests.get('https://habr.com/ru/all/').text
soup = BeautifulSoup(main_link, 'html.parser')


for article in soup.find_all('article', class_="post post_preview"):
    poster = False
    title = article.find(class_='post__title_link').text.lower()
    article_link = article.find('a', class_="post__title_link", href=True)['href']
    for word in KEYWORDS:
        if word in title.split(' '):
            poster = True
    if not poster:
        hubs = article.find_all('a', class_="inline-list__item-link hub-link")
        hubs_text = list(map(lambda x: x.text, hubs))
        for word in KEYWORDS:
            if word in hubs_text:
                poster = True
    if not poster:
        article_full = requests.get(article_link).text
        soup2 = BeautifulSoup(article_full, 'html.parser')
        article_body_text = soup2.find(id="post-content-body").text.lower()
        for word in KEYWORDS:
            if re.findall(word, article_body_text):
                poster = True
    if poster:
        text = f'{title}  -->  {article_link}'
        print(text)
        with open('results.txt', 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')