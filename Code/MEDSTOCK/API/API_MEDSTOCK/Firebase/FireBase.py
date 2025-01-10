
from dotenv import load_dotenv
import os
import pyrebase

load_dotenv()

apiKey= os.getenv('FIRE_APIKEY')
authDomain= os.getenv('FIRE_AUTHDOMAIN')
databaseURL = os.getenv('FIRE_DATABASE_URL')
projectId= os.getenv('FIRE_PROJECTID')
storageBucket= os.getenv('FIRE_STORAGEBUCKET')



firebaseConfig = {
    'apiKey': apiKey,
    'authDomain': authDomain,
    'databaseURL' :databaseURL,
    'projectId': projectId,
    'storageBucket': storageBucket,
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth_firebase = firebase.auth()


def login(email, password):
    try:
        login= auth_firebase.sign_in_with_email_and_password(email,password)
        return login
    except:
        return False


def singup(email, password):
    
    try:
        auth_firebase.create_user_with_email_and_password(email, password)
        return True
    except:
        return False


def resetpassword(email):
    try:
        auth_firebase.send_password_reset_email(email)
        return True
    except:
        return False

