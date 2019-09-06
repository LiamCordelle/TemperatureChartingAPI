import temperature as temp
from datetime import datetime
import os
import pytz

#Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


TIMEZONE = pytz.timezone("NZ")

def record_temperature(collection):
    current_temp = temp.get_pi_temperature()
    current_time = datetime.now(TIMEZONE)
    
    current_date_time_unicode = unicode(current_time.strftime("%Y-%m-%d %H:%M:%S"), "utf-8")
    current_date_unicode = unicode(current_time.strftime("%Y-%m-%d"), "utf-8")
    current_time_unicode = unicode(current_time.strftime("%H:%M:%S"), "utf-8")

    document = collection.document(current_date_unicode)

    document.set({current_time_unicode: {
        u"timestamp": current_date_time_unicode, 
        u"temperature": current_temp
    }}, merge=True)
 
if __name__ == "__main__":
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    firebase_creds = credentials.Certificate('/home/pi/TemperatureChartingAPI/firebase_account.json')
    firebase_admin.initialize_app(firebase_creds)

    firebase_db = firestore.client()

    temperature_collection = firebase_db.collection(u'temperature_data_v3')

    record_temperature(temperature_collection)
