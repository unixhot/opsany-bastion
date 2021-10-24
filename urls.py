# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('blueapps.account.urls')),
    url(r'^', include('index.urls')),
    url(r'^api/bastion/v0_1/', include('bastion.urls')),
]
