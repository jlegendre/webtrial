"""webtrial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import patterns, include, url
from django.contrib import admin
from polls import views
from django.conf import settings
from django.conf.urls.static import static
from polls.views import *
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', views.welcome),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', views.register),
    url(r'^addFriend/', views.add_friend),
    url(r'^showProfile/$', views.show_profile),
    url(r'^modifyProfile/$', views.modify_profile),
    url(r'^login/',views.login),
    url(r'^welcome/$',views.welcome),
    url(r'^upload/$', views.upload),
    url(r'^ajax/checkEmailField$', views.ajax_check_email_field),
    url(r'^ajax/addFriend$', views.ajax_add_friend),
    url(r'^champs/$', views.champs),
    url(r'^replyTest/$', views.replyTest),
    url(r'^reply/$', views.reply),
    url(r'^google/', views.google),
    url(r'^baseVisite/$', views.baseVisite),
    url(r'^access/(?P<page_id>[0-9]+)/$', views.access),
    url(r'^access/modifyAnswer/(?P<page_id>[0-9]+)/$', views.modify_answer),
    url(r'^modifyChamps/(?P<instance>[0-9]+)/$', views.modify_champs),
    url(r'^modifyChamps/(?P<instance>[0-9]+)/delete/$', views.delete_champs),
    url(r'^galerie/$', views.galerie),
    url(r'^email/send/$', views.sendmail),
    url(r'^email/thankyou/$', TemplateView.as_view(template_name='polls/thankyou.html'), name='thankyou'),
    url(r'^email/$', TemplateView.as_view(template_name='polls/email.html'), name='email'),
    url(r'^addQuestion/$', views.addQuestion),
    url(r'^addPage/$', views.addPage),
    url(r'^get_reply/$', views.get_reply),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

# urlpatterns = [
#     url(r'^$', views.welcome),
#     url(r'^polls/', include('polls.urls')),
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^register/', views.register),
#     url(r'^addFriend/', views.add_friend),
#     url(r'^showProfile$', views.show_profile),
#     url(r'^login/',views.login),
#     url(r'^welcome/$',views.welcome),
    
# ]    

