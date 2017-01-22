from django.utils import timezone
from math import log


def _popularity(ques):
	scores = [x.score for x in ques.answer_set.all()]
	scores_sum = sum(scores)
	time_diff = timezone.now() - timezone.localtime(ques.created_time)
	time_diff_seconds = time_diff.days * 24 * 60 * 60 + time_diff.seconds
	P = float(scores_sum + ques.points) / float(log(time_diff_seconds, 10))
	return P
