from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnswerSerializer
from rest_framework.decorators import api_view
from threads.models import answer
# Create your views here.


class VotesView(APIView):

    def get(self, request):
        answers = answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class GetVote(APIView):

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
