from django.shortcuts import render

# Create your views here.

from django.http import (
    HttpResponse,
    Http404,
    HttpResponseServerError,
    JsonResponse,
)



def index(req):
    return HttpResponse("<h1>Hello 你好!</h1>")

async def aindex(req):
    return HttpResponse("<h1>Hello 你好!</h1>")

def json(req):
    return JsonResponse(req.headers)

def err500(req):
    return HttpResponseServerError("内部错误")


def err404(req):
    raise Http404("not found")

