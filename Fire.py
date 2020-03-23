
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import datetime
import pycurl, json, re
now=datetime.datetime.now()
time=now.strftime("%H:%M")
print(time)
cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'testy')
tokens=[]
try:
    docs = doc_ref.stream()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
        if doc.to_dict() not in tokens:
        	tokens.append(doc.to_dict())
        	print('*********tokens:{}*********'.format(tokens))

except google.cloud.exceptions.NotFound:
    print(u'Missing data')
tokensnew='{}'.format(tokens)
print(tokensnew)

x=re.sub("token", "", tokensnew)
x=re.sub("]", "", x)
x=re.sub('\[', "", x)
x=re.sub("'", "", x)
x=re.sub("{", "", x)
x=re.sub("}", "", x)
x=re.sub(",", "", x)
x=re.split(" ",x)
x = list(filter(None, x))
print(x)
x=[i for i in x if i!=':']
for i in x:
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'https://fcm.googleapis.com/fcm/send')
	c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','Authorization: key=AAAAP1gySWk:APA91bEJogPOykWMPEc4hoFer2QXo0uOijVODd2AHrb0qHsIWFRLAFGEDw-YZfEVi0oC9G_zh2j2dZ4RIvMyJi-cf3kvo2gZMRHN8PFvYDMwzAFVk4qlLmo5NyQNXhZNvzlqP7w6pG20'])
	print('======================{}'.format(i))
	data = json.dumps({"notification":{"title":"GTFO","body":"frame{clas},{id}.jpg" .format(clas=class_names[0],id=int(track.track_id)),"icon":"/itwonders-web-logo.png",}, "to":"{}".format(i)})
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, data)
	c.setopt(pycurl.VERBOSE, 1)
	c.perform()
	print(c.getinfo(pycurl.RESPONSE_CODE))
	certinfo = c.getinfo(pycurl.INFO_CERTINFO)
	print(certinfo)
	c.close()


'''

'''
'''
import subprocess
subprocess.call('start /wait python fire.py', shell=True)
'''
'''
import pycurl, json
c = pycurl.Curl()
c.setopt(pycurl.URL, 'https://fcm.googleapis.com/fcm/send')
c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','Authorization: key=AAAAP1gySWk:APA91bEJogPOykWMPEc4hoFer2QXo0uOijVODd2AHrb0qHsIWFRLAFGEDw-YZfEVi0oC9G_zh2j2dZ4RIvMyJi-cf3kvo2gZMRHN8PFvYDMwzAFVk4qlLmo5NyQNXhZNvzlqP7w6pG20'])
data = json.dumps({"notification":{"title":"GTFO","body":"Knz Send you a message","icon":"/itwonders-web-logo.png",}, "to":"ezofMoRcf64:APA91bGzW4M0bq1NZQfp1u_mpn5Ieg8oZrer0OdA9oP0K-YNNlSv7MeN5_zk2pbJPiJJ1jVoC7ie-TCB_l_cg3jjvauGlZEnf3YObB3_IYiPkDZX2KaEVfS3U0_O_qWHh3V9yj4gEtAh"})
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, data)
c.setopt(pycurl.VERBOSE, 1)
c.perform()
print(c.getinfo(pycurl.RESPONSE_CODE))
certinfo = c.getinfo(pycurl.INFO_CERTINFO)
print(certinfo)
c.close()
'''



