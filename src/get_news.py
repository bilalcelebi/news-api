from pygooglenews import GoogleNews
from newspaper import Article
from src.database import *
from loguru import logger

def get_keywords(text):

    keywords = str(text).split(',')
    keywords = [kr.replace(' ','') for kr in keywords]
    keywords = [str(kr).upper() for kr in keywords]
    
    if len(keywords) > 0:
        return keywords
    else:
        return None



def get_new(link, source, source_id):

    article = Article(link)
    article.download()
    article.parse()

    data = {
        'title':article.title,
        'text':article.text,
        'keywords':get_keywords(article.meta_data['keywords']),
        'date':article.publish_date,  
        'summary':article.summary,
        'authors':article.authors,
        'source':source,
        'source_id':source_id,
        'news_link':article.canonical_link
    }

    return data


def get_turkish(url):

    gn = GoogleNews(lang = 'tr', country = 'tr')
    news = gn.search(query = f'{url}', when = '1d')

    return news


def get_english(url):

    gn = GoogleNews(lang = 'en')
    news = gn.search(query = f'{url}', when = '1d')

    return news


def get_articles():

    sources = get_sources()

    all_news = []

    for source in sources:
        source_url = source['url']
        source_id = source['id']
        source_lang = source['lang']

        if source_lang == 'tr':
            news = get_turkish(source_url)
        else:
            news = get_english(source_url)


        for article in news['entries']:

            try:
                url = str(article['links'][0]['href'])
                page = get_new(link = url, source = source_url, source_id = source_id)

                if page not in all_news:
                    all_news.append(page)
                    
            except Exception as e:
                logger.exception(e)
    

    return all_news
