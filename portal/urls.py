from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import LoginView, logout_then_login


urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^clear_session_fls$', views.clear_session, name='clear_session'),
    url(r'^survey/details/(?P<slug>[\w-]+)/$', views.SurveyDetailView.as_view(), name='survey_detail'),
    url(r'^survey/start/(?P<slug>[\w-]+)/$', views.survey_start, name='survey_start'),
    url(r'^survey/submitted/', TemplateView.as_view(template_name='portal/survey_submitted.html'),
        name='survey_submitted'),
    url(r'^survey/already_given/(?P<slug>[\w-]+)/$', views.survey_already_done, name='survey_already_done'),

    url(r'^myadmin/login/$', LoginView.as_view(template_name='portal/login.html'), name='admin_login'),
    url(r'^myadmin/logout/$', logout_then_login, {'login_url': '/myadmin/login'}, name='admin_logout'),
    url(r'^myadmin/$', views.admin_home, name='admin_home'),
    url(r'^myadmin/survey/report/(?P<survey_id>[0-9]+)$', views.survey_report, name='survey_report'),

]
