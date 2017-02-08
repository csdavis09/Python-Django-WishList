from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='login'),
    url(r'^process$', views.process, name='process_login'),
    # url(r'^success$', views.show),
    # url(r'^logout$', views.logout),
]
