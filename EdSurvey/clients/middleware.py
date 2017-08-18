from django.core.exceptions import ObjectDoesNotExist
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

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

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     if hasattr(request, 'person'):
    #         if len(view_args) >= 3:
    #             view_args[2] = request.person
    #         elif 'person' in view_kwargs:
    #             view_kwargs['person'] = request.person
    #     response = view_func(request, *view_args, **view_kwargs)
    #     return response
