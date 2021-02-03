# Blink Fitness

Sick of the reservation bullshit at Blink Fitness?
I reversed engineered the app to manage your gym hours and automatically schedule your workouts.

- A command line tool to view and edit reversation
- A cronjob so my gym time is always reserved

Setup:
 - Python 3.7+
 - pip3 install -r requirements.txt
 - cp .env.example .env
 - Add your user id and zipcode you signed up with, this is needed to manage the account

To manage gym time:
 - python3 run.py

To setup the cronjob to run everyday:
 - Run "chmod +x cronjob.py" to make the file executable by cron
 - Run "crontab -e" to edit cron jobs
 - Add "0 6 * * * /usr/bin/python3 ~/Code/blink/cronjob.py >> ~/Code/blink/logs 2>&1" so the job runs 6am daily and logs the output
 - Note: Run "which python" if you are unsure what python path to use
