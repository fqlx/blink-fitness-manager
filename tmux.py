import time
from os import getenv
from dotenv import load_dotenv
from datetime import date
from Blink import Blink

load_dotenv()

blink = Blink(userId=getenv('USERID'), zipCode=getenv('ZIPCODE'))

while True:
    try:
        blink.login()
        blink.register_next_4_days('15:30:00')
        blink.register_next_4_days('15:40:00')
        blink.register_next_4_days('15:20:00')
        blink.register_next_4_days('15:10:00')
        blink.register_next_4_days('15:00:00')
    except Exception as e:
        print(e)
    time.sleep(60 * 15)
