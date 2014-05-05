from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^accounts/xmlapi/(?P<cookie_value>.*)/$', views.UserKeyView.as_view(content_type='text/xml'), name="users_xmlapi"),
)
