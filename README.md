# ![][logo]

_[Live link][link]_

drchrono Birthdays is a Django app for sending emails to patients on their birthday. drchrono Birthdays integrates with [drchrono][drchrono] to consume a user's patients through the drchrono API.

**Technologies used to build this application include:**
* Python 2.7
* Django 1.9
* jQuery

Additional Dependancies:
* Requests

**Additional Notes:**
* The `send_emails` command should be run daily to ensure all patients receive their birthday emails on the correct day.<br>
Run command with: `python manage.py send_emails`
* When run locally, drchrono Birthdays can only access the drchrono API if the server is run on localhost:8000.

[logo]: ./birthday_reminder/static/images/drchrono-lg.png
[link]: https://drchronobirthdays.herokuapp.com/
[drchrono]: https://www.drchrono.com/
