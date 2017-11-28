from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recommender.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('application.urls', namespace="application")),
    url(r'^admin/', include(admin.site.urls)), #Admin
)
