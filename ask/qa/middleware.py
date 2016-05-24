from datetime import datetime
from django.http.response import HttpResponseRedirect
from qa.models import Session


class CheckSessionMiddleware(object):
    def process_request(self, request):
        try:
            sessionid = request.COOKIES.get('sessionid')
            session = Session.objects.get(key=sessionid, expires__gt=datetime.now(), )
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None


def auth_check(view):
    def view2(request, *args, **kwargs):
        if None is request.session:
            return HttpResponseRedirect('/login')
        else:
            return view(request, *args, **kwargs)

    return view2
