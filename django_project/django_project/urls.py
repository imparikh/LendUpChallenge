from django.conf.urls import patterns, include, url

from django.contrib import admin
from content import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^replayer/', views.replayer),
    url(r'^processFB/', views.processFB),
    url(r'^callOther/', views.callOther),
    url(r'^phaseTwo/', views.phaseTwo),
    url(r'^content/', views.index),
    url(r'^admin/', include(admin.site.urls)),
)
