from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, Http404



async def index(req):
#def index(req):
    return HttpResponse("Hello 你好!")




def err404(req):
    return Http404("not found")

