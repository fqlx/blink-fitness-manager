from os import getenv
from dotenv import load_dotenv
from datetime import date
from Blink import Blink

print('Date:', date.today())

load_dotenv()

blink = Blink(userId=getenv('USERID'), zipCode=getenv('ZIPCODE'))
blink.login()
blink.register_next_4_days('15:30:00')
