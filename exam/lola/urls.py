from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

_patterns = (
    url(r'^$', 'learning', name='learning'),
)

urlpatterns = patterns('lola.views', *_patterns)
