from google.cloud import storage
from firebase import firebase
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="cred.json"
firebase = firebase.FirebaseApplication('https://s8project-test.appspot.com/')
client = storage.Client()
bucket = client.get_bucket('s8project-test.appspot.com')
# posting to firebase storage
imageBlob = bucket.blob("/")
# imagePath = [os.path.join(self.path,f) for f in os.listdir(self.path)]
imagePath = "frame['person'],1.jpg"
imageBlob = bucket.blob("yoo")
imageBlob.upload_from_filename(imagePath)