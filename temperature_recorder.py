import temperature as temp
from datetime import datetime
import os
import pytz

#Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


TIMEZONE = pytz.timezone("NZ")

def recordTemperature(collection):
    currentTemp = temp.get_pi_temperature()
    currentTime = datetime.now(TIMEZONE)
    
    currentTimeString = unicode(currentTime.strftime("%Y-%m-%d %H:%M:%S"), "utf-8")

    document = collection.document(currentTimeString)

    document.set({
        u"timestamp": currentTimeString, 
        u"temperature": currentTemp
    })
 
if __name__ == "__main__":
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    firebase_creds = credentials.Certificate('/home/pi/TemperatureChartingAPI/firebase_account.json')
    firebase_admin.initialize_app(firebase_creds)

    firebase_db = firestore.client()

    temperature_collection = firebase_db.collection(u'temperature_data_v2')

    recordTemperature(temperature_collection)
