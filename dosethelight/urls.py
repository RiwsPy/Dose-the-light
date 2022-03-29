"""dosethelight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django import VERSION
from django.contrib import admin
from .views import home
from django.urls import include

if VERSION[0] >= 3:
    from django.urls import path, re_path
    method = path
    method_re = re_path
else:
    from django.conf.urls import url
    method = url
    method_re = url

urlpatterns = [
    method_re(r'^admin/', admin.site.urls),
    method('', home, name='home'),
    method('maps/', include("maps.urls")),
]
