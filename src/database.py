from firebase_admin import firestore
import firebase_admin

creds = {
  "type": "service_account",
  "project_id": "news-app-f6aa6",
  "private_key_id": "39c531641d642e6f663fe245cb0a2b86645b08b9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCUw8lqpqbaNYAA\n1PspdbrVAEKMibdAQBTtdtnyXBB8NcHOSuQg3MoOvOmrHHVmellgq6OoVu7ftINl\njJ+O4IegQtWYvPL5xpaR3RCEEoCbuEfuLaWI3YNR3niV4a4h7JTRMBoaLwru4aZQ\nhyFoVORS8JP7GdfFwIdX2EMJPJcIPTqs/m4DcAh+tamFx/SRTLVcbDTNkJTfV+zp\nFVvGHCHGtWVcdb0uGLXlBYqxBNx5O46YBgXC9jj/qvIlap//pRvVq1vjyuY2pdVc\nadxaODHJmz5LHIGHppuA5iIBHHyObKnAvBrRxuJtYQaQ2ZjRLjPtfgiEc+N44xk1\n9YU9SFvBAgMBAAECggEABaOT24zfn3JBtnmPeUqmJcBk+JcyMNqwMGQkVMrnZERU\nliSoMXqzcHJgWFHm1vCYuYP02ylLoR0vK3oOHkglu/RsmX9bP0HA0vY409jKGTaX\nodA6Vk39ouyc6e/sPgr0UfQFBhMPn6IPQAqVpv/FlXZ0ryL51w9T0ged9H6tQ7mh\nO7KmZAdSQt7aufM7c0D4U6JdrZK3rJ2/h2m4XzmCMzSYx+Uj84bGuGwGFTy+nwBG\nicNLIXNdkpeTSSuXiyMjLNjZD0AtFkwtWY5Ilx+CfN07lAMfSPz01ET8uOGHpCAP\nZXNGMxNXnxPOEfvcr9xuMMbfw1QW+2OLI/zUymmvxQKBgQDKPFYGUtMPVfDA7wX5\nhTouZVKN2+v2UyupeCSLzy6h1ysqLOjLKvYDpH+zRxrkoa+05kgLagYMIdxGYlS0\n5O/IyAFRIH3//4J7gnYIMVXYyfbxqlWCytPoDOwGPtC8SxHdazBcsP+CzTgoGxYP\nc+gXDXUh4tQLndumDMhjBa7MpwKBgQC8UFpdj+nsN4Oi3Sqo/SYBg20Hl3lAHkGP\nOqXv1W2B7FM5TP14+194mvdkpkdOVAW0WDU4H0LCFszO2KgTGHQU1SYFuUz89iW3\nXfUsiSo8MCqh8yqyjPt8pc+XH/wZtLilD2wpouW48s3WwMA7TPWFeLAzV6taWgQ9\n7oB2kgeZVwKBgAqX+IWiRw4RmWfx3WVBtleB1T47G/QuTSY2deug8bdmlwtBiPxD\nhtmP/2R7wAvj8FlQisuWRTTTfT9unTNQnsLsvyzpv8/uKX6gyeAJ/Y46niXwn0QX\nrdwE+UQmfDaw1AG+QK1KVEgcyelH6fLrRmgWu2EICcWGAmCDYOfW/14XAoGAUjPB\nPpZTxol1LOLefGYE8SQts+KrSxHqDFvNk6PW6Z//tEOnYehZBIyg8Y6kEc0bsF3Q\n3W7H9XF+dcydkbha870Xm+gHc2T/kcux+n7lsOBVu9wqB0cDgKXguFd99Lqu316c\nGJDDNrjGobgCMeCmTF0ijUb3xbkFoQM7kIauSoECgYEAhjc+CHH/38z9uhTuMRLl\nSqMjMYFUqMkYfcxYO/q6wyAHOs4kQG/MoqQRMlPvJDRbh8VjghPlaPBaKBRVfhF/\n3UGrbxxyRs5J14OWis+1cqzFoZ0k1HQtKqf+pmuTJkzmDsTAmqTchO1SbPJQTCFq\nFrsC3JWcZP+TGM3gnqstCMk=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-a6ty8@news-app-f6aa6.iam.gserviceaccount.com",
  "client_id": "112058000407328415679",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-a6ty8%40news-app-f6aa6.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


def get_db():

    if not firebase_admin._apps:
        cred_object = firebase_admin.credentials.Certificate(creds)
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

