from firebase_admin import credentials, initialize_app, storage
import random,string,os

class FireBaseService:

    cred = credentials.Certificate("chat-app-6f482-firebase-adminsdk-61a9c-ae3120aa3a.json")
    initialize_app(cred, {'storageBucket': 'chat-app-6f482.appspot.com'})    

    def uploadFile(self,file):
        # Put your local file path 
        #fileName = "myImage.jpg"
        bucket = storage.bucket()
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 7)) 
        filename = res+file.filename
        blob = bucket.blob('yavatmal_execs/'+filename)
        blob.upload_from_file(file)
        # Opt : if you want to make public access from the URL
        blob.make_public()

        #print("your file url", blob.public_url)
        #os.remove(file)
        return str(blob.public_url)