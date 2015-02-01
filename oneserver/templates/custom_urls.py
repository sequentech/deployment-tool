from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^authapi/api/', include('api.urls')),
    url(r'^authapi/admin/', include(admin.site.urls)),
)
