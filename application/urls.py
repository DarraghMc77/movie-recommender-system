from django.conf.urls import patterns, url

from application import views


urlpatterns = patterns('',
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.IndexView, name='index'),
    url(r'results/', views.ResultsView, name='results'),
    url(r'ratings/', views.RatingsView.as_view(), name='ratings'),
    url(r'recommend/', views.recommend, name='recommend'),

)
