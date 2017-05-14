from root.settings import MG_KEY, MG_URL, MG_FROM, BASE_DIR
from django.template.loader import render_to_string
import requests
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


def render_email(template, context):
	temp = "email_templates/" + template
	return render_to_string(temp, context)


def test_send_email(to):
	context = {"header": "Hey Sriram, you have a new notificaiton.", "content": "Jeremy answered your question 'Timeline enlightment?' "}
	body = render_email("sample_email.html", context)
	opts = {
		"recipents": to,
		"subject": "You have got a new notification.",
		"body": body
	}
	send_email(opts)
