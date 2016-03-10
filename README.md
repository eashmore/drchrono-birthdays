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
* When run locally, you can use you're drchrono client information by setting `CLIENT_DATA` in `settings.py`.

		CLIENT_DATA = {
    		'client_id': client id,
			'client_secret': client secret',
    		'redirect_url': "http://your_site.com/handle_authentication"
		}
		
* You can use an email address of your choice my setting `EMAIL` information in `settings.py`. An example for a _gmail_ account:

		EMAIL_USE_TLS = True

		EMAIL_HOST = 'smtp.gmail.com

		EMAIL_HOST_USER = 'your_email@gmail.com'

		EMAIL_HOST_PASSWORD = email password

		EMAIL_PORT = 587

[logo]: ./birthday_reminder/static/images/drchrono-lg.png
[link]: https://drchronobirthdays.herokuapp.com/
[drchrono]: https://www.drchrono.com/
