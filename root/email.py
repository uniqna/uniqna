import requests
from root.settings import MG_KEY, MG_URL, MG_FROM, BASE_DIR
import os


def send_email(opts={}):
	if not opts:
		return "To, Subject and Body required to send the mail."
	else:
		return requests.post(
			MG_URL,
			auth=("api", MG_KEY),
			data={"from": MG_FROM, "to": opts["recipents"], "subject": opts["subject"], "html": opts["body"]},
		)


def test_send_email():
	template = open(os.path.join(BASE_DIR, "home", "templates", "email.html")).read()
	body = template % ("Jeremy answered your question 'How are you?'.")
	opts = {
		"recipents": "sriru1998@gmail.com",
		"subject": "You have got a new notification.",
		"body": body
	}
	send_email(opts)
