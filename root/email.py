from root.settings import MG_KEY, MG_URL, MG_FROM, BASE_DIR
from django.template.loader import render_to_string
from root.settings import DEBUG
import requests
import os

# Uncomment this if you wanna check out mails in action in debug mode
DEBUG = False


def send_email(opts={}):
	# (Dictionary: opts)
	# Base email function to send emails.
	# opts MUST contain recipents, subject and body
	# body will be rendered by render_email()
	if not opts:
		return "To, Subject and Body required to send the mail."

	return requests.post(
		MG_URL,
		auth=("api", MG_KEY),
		data={
			"from": MG_FROM,
			"to": "uniqnamail@gmail.com",
			"bcc": opts["recipents"],
			"subject": opts["subject"],
			"html": opts["body"]
		})


def render_email(template, context):
	# (String: template, Dictionary: context)
	# Pass in a template name and a context
	# Returns the rendered html output.
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
	print(send_email(opts))


def send_notification_email(notification):
	# (Object: Notification)
	to = notification.user.email
	uname = notification.user.username
	content = notification.content
	url = "https://uniqna.com" + notification.get_absolute_url()
	context = {
		"header": "Hey {}, you have a new notificaiton.".format(uname),
		"content": content,
		"url": url
	}
	body = render_email("sample_email.html", context)
	opts = {
		"recipents": to,
		"subject": "Knock Knock. Mail from uniqna.",
		"body": body
	}
	if DEBUG:
		# Don't send emails if we are in debug mode
		# Instead print them in the console
		print("\n\n\n")
		print("---------------------------------------")
		print(opts)
		print("---------------------------------------")
		print("\n\n\n")
		return True
	else:
		print(send_email(opts))
