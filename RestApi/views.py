from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnswerSerializer, TagSerializer, QuestionSerializer
from rest_framework.decorators import api_view
from threads.models import answer
from ask.models import tag, question
# Create your views here.


def TestView(request):
	return render(request, "test.html")


class TestPost(APIView):
	def post(self):
		pass


class SuggestTag(APIView):
	def post(self, request):
		text = request.data["text"]
		words = text.split()
		tag_names = [x.name for x in tag.objects.all()]
		sugg_tag_names = [x for x in tag_names for y in words if x.lower() == y.lower()]
		sugg_tags = [tag.objects.get(name=x) for x in sugg_tag_names]
		serializer = TagSerializer(sugg_tags, many=True)
		print(serializer.data)
		return Response(serializer.data)


class CreateTag(APIView):
	def get(self, request):
		tags = tag.objects.all()
		serializer = TagSerializer(tags, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = TagSerializer(data=request.data)
		print("data received")
		if serializer.is_valid():
			print("tag is valid")
			serializer.save()
			print("tag creaed")
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VotesView(APIView):

	def get(self, request):
		answers = answer.objects.all()
		serializer = AnswerSerializer(answers, many=True)
		return Response(serializer.data)

		def post(self):
			pass


class AnswerVote(APIView):

	def GetAnswer(self, pk):
		try:
			return answer.objects.get(pk=int(pk))
		except answer.DoesNotExist:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def Vote(self, request, pk, ud):
		ans = self.GetAnswer(pk)
		if ud == 'u':
			print("up")
			vote_on = ans.ups
			vote_on_other = ans.downs
		elif ud == 'd':
			print("down")
			vote_on = ans.downs
			vote_on_other = ans.ups
		if request.user not in vote_on.all():
			print("adding ")
			vote_on.add(request.user)
			vote_on_other.remove(request.user)
		else:
			vote_on.remove(request.user)
		print("saved")
		ans.save()
		return ans

	def get(self, request, pk, ud):
		ans = self.Vote(request, pk, ud)
		serializer = AnswerSerializer(ans)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def post(self, request, pk, ud):
		pass


class QuestionVote(APIView):

	def GetQuestion(self, pk):
		try:
			return question.objects.get(pk=int(pk))
		except question.DoesNotExist:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def Vote(self, request, pk, ud):
		ques = self.GetQuestion(pk)
		if ud == 'u':
			print("up")
			vote_on = ques.ups
			vote_on_other = ques.downs
		elif ud == 'd':
			print("down")
			vote_on = ques.downs
			vote_on_other = ques.ups
		if request.user not in vote_on.all():
			print("adding ")
			vote_on.add(request.user)
			vote_on_other.remove(request.user)
		else:
			vote_on.remove(request.user)
		print("saved")
		ques.points = ques.ups.count() - ques.downs.count()
		ques.save()
		return ques

	def get(self, request, pk, ud):
		ques = self.Vote(request, pk, ud)
		serializer = QuestionSerializer(ques)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def post(self, request, pk, ud):
		pass


