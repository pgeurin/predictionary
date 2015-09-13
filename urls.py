from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, TemplateView
from polls.models import Poll
from probabledata.models import Prediction
from probabledata import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#urlpatterns = patterns('polls.views',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
#    url(r'^polls/$', 'index'),
#    url(r'^polls/(?P<poll_id>\d+)/$', 'detail'),
#    url(r'^polls/(?P<poll_id>\d+)/results/$', 'results'),
#    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'vote'),
#)

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Prediction.objects.all(),
            context_object_name='latest_prediction_list',
            #queryset=Poll.objects.order_by('-pub_date')[:5], #CHANGE DATABSE AND SHOW THIS TO SEE OLD LIST
            #context_object_name='latest_poll_list',
            template_name='prediction/home.html')),

    #url(r'^search/$', #add entry
    #    #'probabledata.views.search'
    #    ListView.as_view(
    #        queryset=Prediction.objects.all(),
    #        context_object_name='latest_prediction_list',
    #        template_name='prediction/search.html')
    #    ),
    url(r'^search/$', views.search),
    url(r'^create/$', TemplateView.as_view(template_name="prediction/create.html")),
    url(r'^createcomplete/$', views.newQuiz),
    url(r'^(?P<pk>\d+)/$',DetailView.as_view(model=Prediction, template_name='prediction/takequiz.html')),
    url(r'^(?P<prediction_id>\d+)/vote/$', views.vote),
    url(r'^(?P<prediction_id>\d+)/votecomplete/$', views.results),
    url(r'^(?P<pk>\d+)/results/$',DetailView.as_view(model=Prediction, template_name='prediction/results.html')),
    )

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


#urlpatterns = patterns('polls.views',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

#    url(r'^polls/$', 'polls.views.index'),
#    url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),
#    url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
#    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),

#    # Uncomment the admin/doc line below to enable admin documentation:
#    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
#)
