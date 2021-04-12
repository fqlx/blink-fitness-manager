import requests
import time
from datetime import date, timedelta, datetime


class Blink:
    SPOOFED_UA = 'Blink Fitness/2.24.0 (iPhone; iOS 13.6.1; Scale/3.00)'
    API_KEY = 'nPFjzhoIsK3GIP52G7Xqx9KCozCg6HmS8VbhSmYD'
    HOST = 'https://uzkvhe2t35.execute-api.us-west-2.amazonaws.com'

    userId = None
    zipCode = None

    name = None
    businessUnitCode = None

    headers = None

    def __init__(self, userId: str, zipCode: str):
        self.userId = userId
        self.zipCode = zipCode
        self.headers = {
            'x-api-key': self.API_KEY,
            'User-Agent': self.SPOOFED_UA,
        }

    def register_next_4_days(self, time: str):
        reservations = list(
            map(
                lambda reservation: datetime.strptime(
                    reservation['StartDate'],
                    '%Y-%m-%dT%H:%M:%S%z').strftime("%Y-%m-%d"),
                self._get_reservations()))

        for d in range(0, 4):
            day = date.today() + timedelta(days=d)
            if str(day) in reservations:
                print(day, ': Registered')
                continue

            slots = self._get_slots(day)
            remainingSpots = list(
                filter(
                    lambda slot: slot['remainingSpots'] > 0,
                    slots))
            open_slot = list(
                filter(
                    lambda spot: spot['startTime'] == time,
                    remainingSpots))

            if not len(open_slot):
                print(day, ': No slots')
                continue

            event_id = open_slot[0]['eventInstanceId']
            print('Register:', day, event_id)
            self.register_slot(event_id)

    def register_slot(self, event_id: str):
        url = self.HOST + '/prod/reservations/register'
        payload = {
            'eventInstanceId': event_id
        }
        result = requests.post(url, headers=self.headers, json=payload).json()
        print(result)

    def print_open_slots(self, days):
        day = date.today() + timedelta(days=days)
        print('====', day, '====')

        slots = self._get_slots(day)
        remainingSpots = list(
            filter(
                lambda slot: slot['remainingSpots'] > 0,
                slots))

        if not len(remainingSpots):
            print('......')
            return

        startTimes = list(
            map(lambda spot:
                [spot['eventInstanceId'], spot['startTime']],
                remainingSpots))
        list(map(print, startTimes))

    def _get_slots(self, day):
        unixtime = str(int(time.mktime(day.timetuple())))
        url = self.HOST + '/prod/reservations/slots'
        payload = {
            'businessUnitCode': self.businessUnitCode,
            'date': unixtime,
        }
        result = requests.get(url, headers=self.headers, params=payload).json()
        return result['slots']

    def print_reservations(self):
        print('---', self.name, '---')
        reservations = self._get_reservations()
        times = list(map(lambda reservation:
                         datetime.strptime(
                             reservation['StartDate'],
                             '%Y-%m-%dT%H:%M:%S%z'
                         ).strftime("%Y-%m-%d %r"), reservations))
        list(map(print, times))
        print()

    def _get_reservations(self):
        url = self.HOST + '/prod/reservations/member'
        payload = {
            'fromDate': date.today().strftime("%m%d%Y")
        }
        result = requests.get(url, headers=self.headers, params=payload).json()
        return result['registrations']

    def login(self):
        url = self.HOST + '/prod/auth/login'
        payload = {
            'authType': 'zip',
            'userId': self.userId,
            'password': self.zipCode,
        }
        result = requests.post(url, headers=self.headers, json=payload).json()
        self.headers['Authorization'] = 'Bearer {}'.format(result['token'])
        self.businessUnitCode = result['member']['Location']['Code']
        self.name = result['member']['Location']['Name']
