from src.database import get_db
from src.get_news import get_articles
from datetime import datetime
from loguru import logger

def add_article(document, article):

    db = get_db()
    created_time, response = db.collection(document).add(article)

    return response.id
    

def fetch_articles(document_id):

    db = get_db()
    collection = db.collection(document_id)
    documents = collection.stream()
    response = [document.to_dict() for document in documents]

    return response



def create_newsletter():

    logger.info(f"Creating Newsletter at {datetime.now()}")

    today = datetime.today().strftime("%Y-%m-%d")
    articles = get_articles()

    for article in articles:
        article_added = add_article(today, article)
        logger.info(f'{article_added} added to {today} Documents!!!')



def get_newsletter():

    today = datetime.today().strftime("%Y-%m-%d")
    newsletter = fetch_articles(today)

    return newsletter
