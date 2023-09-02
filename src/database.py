from firebase_admin import firestore
import firebase_admin


def get_db():

    if not firebase_admin._apps:
        cred_object = firebase_admin.credentials.Certificate('./creds.json')
        firebase_admin.initialize_app(cred_object)

    db = firestore.client()

    return db


def get_sources():

    db = get_db()

    collection = db.collection('websites')
    websites = collection.stream()

    websites = [{
        'id':website.id,
        'lang':website.to_dict()['lang'],
        'url':website.to_dict()['url']
    } for website in websites]


    return websites


def create_source(website):

    source = {'url':str(website)}
    db = get_db()

    create_time, website = db.collection('websites').add(source)

    return website.id


def delete_source(source_id):

    db = get_db()
    response = db.collection('websites').document(str(source_id)).delete()

    return {'status':'success', 'delete_time':response}

