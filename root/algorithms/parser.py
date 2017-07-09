from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def get_user(token):
	# Remove last char if it is a punctuation.
	if not token[-1].isalnum():
		token = token[:-1]
	try:
		u = User.objects.get(username=token)
		return u
	except:
		return False


def parse_user_mentions(string):
	string = string.strip()
	if string == "":
		return ""
	word_list = string.split(' ')
	new_word_list = []
	for word in word_list:
		if word[0] == '@':
			user = get_user(word[1:])
			if user:
				username = user.username
				url = reverse('user', args=[username])
				word = "<a href='{}'>{}</a>".format(url, word)
		new_word_list.append(word)
	new_string = " ".join(new_word_list)
	return new_string
