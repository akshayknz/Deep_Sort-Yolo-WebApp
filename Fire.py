import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import datetime
now=datetime.datetime.now()
time=now.strftime("%H:%M")
print(time)
cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'testy')

try:
    docs = doc_ref.stream()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')



doc_ref = store.collection(u'testy')
doc_ref.add({u'name': u'test', u'added': time})