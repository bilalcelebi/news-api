from flask import Flask, request
from src.database import delete_source, create_source
from src.newsletter import get_newsletter
from apscheduler.schedulers.background import BackgroundScheduler
from src.newsletter import create_newsletter

app = Flask(__name__)

@app.route("/news")
def main():
    news = get_newsletter()
    return news


@app.route("/deletesource", methods = ['GET'])
def deletesource():
    args = request.args

    response = delete_source(str(args.get("id")))

    return response


@app.route("/createsource", methods = ['GET'])
def createsource():

    args = request.args
    source_url = args.get("url")

    response = create_source(website = source_url)

    return response



scheduler = BackgroundScheduler()
scheduler.add_job(create_newsletter, 'cron', hour=7, minute=0)


if __name__ == '__main__':

    scheduler.start()
    app.run(host = '0.0.0.0', port = 5000, debug = False)
