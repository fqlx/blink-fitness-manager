from os import getenv
from dotenv import load_dotenv
from Blink import Blink

load_dotenv()

blink = Blink(userId=getenv('USERID'), zipCode=getenv('ZIPCODE'))
blink.login()

blink.print_reservations()
blink.print_open_slots(days=0)
blink.print_open_slots(days=1)
blink.print_open_slots(days=2)

event_id = input("Enter event id to register or r for next 4 days: ")

if event_id == '':
    exit()

elif event_id == 'r':
    blink.register_next_4_days('15:30:00')
    blink.print_reservations()
    exit()

blink.register_slot(event_id)
