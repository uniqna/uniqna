from root.settings import MG_KEY, MG_URL, MG_FROM
from django.template.loader import render_to_string
from root.settings import DEBUG
from django.shortcuts import get_object_or_404
import requests

from threads.models import Answer

# Uncomment this if you wanna check out mails in action in debug mode
# DEBUG = False


def send_email(opts={}):
	# (Dictionary: opts)
	# Base email function to send emails.
	# opts MUST contain recipents, subject and body
	# body will be rendered by render_email()
	if not opts:
		return "To, Subject and Body required to send the mail."

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
		return requests.post(
			MG_URL,
			auth=("api", MG_KEY),
			data={
				"from": MG_FROM,
				"to": opts["recipents"],
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
	context = {}
	body = render_email("invite.html", context)
	opts = {
		"recipents": to,
		"subject": "You have got a new notification.",
		"body": body
	}
	print(send_email(opts))


def send_notification_email(notification):
	url = "https://uniqna.com" + notification.get_absolute_url()
	answer = get_object_or_404(Answer, id=notification.object_id)
	context = {
		"from_user": answer.answer_author,
		"description": notification.description,
		"timestamp": notification.notification_time,
		"url": url
	}
	body = render_email("notification.html", context)
	opts = {
		"recipents": notification.user.email,
		"subject": "Notification from @" + str(answer.answer_author),
		"body": body
	}
	print(send_email(opts))
