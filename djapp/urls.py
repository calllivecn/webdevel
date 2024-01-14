"""
URL configuration for djapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.http import HttpResponse

def favicon(req):
    res = HttpResponse()
    res.status_code = 404
    res['Cache-Control'] = 'max-age=86400'
    return res

urlpatterns = [

    path('totp/', include("totp.urls")),
    #path("__debug__/", include("debug_toolbar.urls")),
    path('favicon.ico/', favicon),

    #path('admin/', admin.site.urls),
]
