from django.core.exceptions import ObjectDoesNotExist
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import AuthenticationMiddleware
# from django.contrib.messages .middleware import MessageMiddleware

from .models import Person, Role


def get_person(request):
    if 'person_id' in request.session:
        person_id = request.session['person_id']
        try:
            return Person.objects.get(pk=person_id)
        except ObjectDoesNotExist:
            pass
    return None


class PersonMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if hasattr(request, 'person'):
            print("request.person in clients.middleware.PersonMiddleware before = ",
                  request.person)
        else:
            print("request.person isn't in clients.middleware.PersonMiddleware before")
        value = SimpleLazyObject(lambda: get_person(request))
        if value:
            request.person = value
            print("request.person in clients.middleware.PersonMiddleware after = ",
                  request.person)
        elif hasattr(request, 'person'):
            del request.person
            if 'person_id' in request.session:
                del request.session['person_id']

# class PersonMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         request.person = SimpleLazyObject(lambda: get_person(request))
#         response = self.get_response(request)
#         print("request.person in clients.middleware.PersonMiddleware = ", request.person)
#         return response
