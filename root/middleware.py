from django.utils.functional import SimpleLazyObject
from root.settings import DEBUG
from django_user_agents.utils import get_user_agent


# Fix for the middleware error of the django-user-agents plugin


class UserAgentMiddleware(object):

    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))


class DebugMiddleware(object):

	def __init__(self, get_response=None):
		if get_response is not None:
			self.get_response = get_response

	def __call__(self, request):
		self.process_request(request)
		return self.get_response(request)

	def process_request(self, request):
		request.debug = DEBUG
