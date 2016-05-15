from django.http import HttpResponse
from django.shortcuts import render_to_response


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def index(request, *args, **kwargs):
    return render_to_response('index.html')
