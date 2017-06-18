from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from threads.models import Answer
from root.email import send_notification_email


class student(models.Model):
	course_choices = (
		("B.Tech", "B.Tech"),
		("M.Tech", "M.Tech"),
		("F.Tech", "F.Tech"),
		("B.Law", "B.Law"),
	)
	school_choices = (
		("SCSE", "SCSE"),
		("SENSE", "SENSE"),
		("SAS", "SAS"),
		("SELECT", "SELECT"),
		("SMBS", "SMBS"),
		("VITBS", "VITBS"),
		("VITSOL", "VITSOL"),
		("VFIT", "VFIT"),
		("V-SPARC", "V-SPARC"),
		("SBST", "SBST"),
		("SCALE", "SCALE"),
		("SCOPE", "SCOPE"),
		("SITE", "SITE"),
		("SMEC", "SMEC"),
		("SSL", "SSL"),
		("LAW", "LAW"),
	)
	grad_year_choices = (
		("2017", "2017"),
		("2018", "2018"),
		("2019", "2019"),
		("2020", "2020"),
	)

	university_choices = (
		("Vellore Institute of Technology, Chennai", "Vellore Institute of Technology, Chennai"),
		("Vellore Institute of Technology, Vellore", "Vellore Institute of Technology, Vellore"),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=240, blank=True, default="")
	course = models.CharField(
		max_length=6, choices=course_choices, default="B.Tech")
	school = models.CharField(
		max_length=6, choices=school_choices, default="SCSE")
	grad_year = models.CharField(
		max_length=6, choices=grad_year_choices, default="2020")
	university = models.CharField(max_length=100, choices=university_choices)


class NotificationExtender(models.Manager):
	def unread_count(self):
		unread_list = [1 for o in self.all() if not o.read]
		unread_count = int(sum(unread_list))
		return unread_count

	def sort_read(self):
		unsorted = self.all()
		srted = sorted(unsorted, key=lambda x: (
			x.notification_time, x.read), reverse=True)
		return srted

	def create_answer_notification(self, user, answer):
		notif_template = "{0} answered to your question \"{1}\"."
		notification = self.create(
			user=user,
			content=notif_template.format(answer.answer_author, answer.question.title[:40]),
			notification_type="answered",
			object_id=answer.pk
		)
		send_notification_email(notification)

	def create_reply_notification(self, user, reply):
		notif_template = "{0} replied to your answer \"{1}\"."
		notification = self.create(
			user=user,
			content=notif_template.format(reply.answer_author, reply.parent.description),
			notification_type="replied",
			object_id=reply.pk
		)
		send_notification_email(notification)


class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	read = models.BooleanField(default=False)
	object_id = models.IntegerField()
	notification_type = models.CharField(max_length=50)
	notification_time = models.DateTimeField(default=timezone.now)
	content = models.CharField(max_length=300)
	objects = NotificationExtender()

	def __str__(self):
		return self.content

	def get_absolute_url(self):
		return "/notification/{}".format(self.pk)
