from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

from root.email import send_notification_email
from post.models import Question
from threads.models import Answer


class student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=256, blank=True, default="")
	notification_emails = models.BooleanField(default=True)


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
		notif_template = "@{0} replied to \"{1}\""
		notification = self.create(
			user=user,
			content=notif_template.format(answer.answer_author, answer.question.title[:40]),
			notification_type="answered",
			object_id=answer.pk
		)
		if user.student.notification_emails:
			send_notification_email(notification)

	def create_reply_notification(self, user, reply):
		notif_template = "@{0} replied \"{1}\"."
		notification = self.create(
			user=user,
			content=notif_template.format(reply.answer_author, reply.description),
			notification_type="replied",
			object_id=reply.pk
		)
		if user.student.notification_emails:
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


# As notification is not being directly attached to any model
# We need to manually delete it when an answer delete signal 
# is received

@receiver(pre_delete, sender=Answer, dispatch_uid="delete_notification_with_question")
def delete_notification(sender, instance, using, **kwargs):
	# Instance => Answer going to be deleted
	# Look up Notification object having the same ID as instance
	# And delete it
	target_notif = Notification.objects.filter(object_id=instance.id)
	target_notif.delete()
