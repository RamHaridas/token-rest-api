from firebase_admin import credentials, initialize_app, storage
import random,string,os

class FireBaseService:

    cred = credentials.Certificate("besafe-caeb8-firebase-adminsdk-chhkw-9e14998b89.json")
    initialize_app(cred, {'storageBucket': 'besafe-caeb8.appspot.com'})    

    def uploadFile(self,file):
        # Put your local file path 
        #fileName = "myImage.jpg"
        bucket = storage.bucket()
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 7)) 
        filename = res+file.filename
        blob = bucket.blob('musics/'+filename)
        blob.upload_from_file(file)
        # Opt : if you want to make public access from the URL
        blob.make_public()

        print("your file url", blob.public_url)
        os.remove(file)
        return str(blob.public_url)