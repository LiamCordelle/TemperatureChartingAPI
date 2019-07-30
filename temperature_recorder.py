import temperature as temp
from datetime import datetime
import os
import pytz

#Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


TIMEZONE = pytz.timezone("NZ")

def recordTemperature(document):
    currentTemp = temp.get_pi_temperature()
    currentTime = datetime.now(TIMEZONE)
    
    currentTimeString = currentTime.strftime("%Y-%m-%d %H:%M:%S")

    document.set({
        unicode(currentTimeString, "utf-8"): currentTemp
    }, merge=True)
 
if __name__ == "__main__":
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    firebase_creds = credentials.Certificate('firebase_account.json')
    firebase_admin.initialize_app(firebase_creds)

    firebase_db = firestore.client()

    temperature_doc = firebase_db.collection(u'temperature_data').document(u'temperatures')

    recordTemperature(temperature_doc)
