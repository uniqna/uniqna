from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from mptt.querysets import TreeQuerySet

import re
from markdown2 import markdown


def get_user(token):
	try:
		u = User.objects.get(username=token)
		return u
	except:
		return False


def parse_match(match):
	token = match.group()
	username = match.group(2)
	user = get_user(username)
	if user:
		url = reverse('user', args=[user.username])
		return " <a href='{}'>@{}</a>".format(url, username)
	else:
		return token


def parse_user_mentions(string):
	string = string.strip()
	if string == "":
		return ""
	new_string = re.sub(r'(\s|^)@([\w_]+)', parse_match, string)
	return new_string


def parse_markdown(string):
	return markdown(string, extras=["tables", "cuddled-lists"])


def parse(queryset):
	# queryset => either question or answer object
	# takes in a queryset/object  and returns a queryset/object with parsed descriptions
	if type(queryset) == QuerySet or type(queryset) == TreeQuerySet:
		for obj in queryset:
			obj.description = parse_user_mentions(obj.description)
			obj.description = parse_markdown(obj.description)
		return queryset
	else:
		# Else it's a single object
		q = queryset
		q.description = parse_user_mentions(q.description)
		q.description = parse_markdown(q.description)
		return q
