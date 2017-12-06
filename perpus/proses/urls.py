from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePage),
    url(r'^atur', views.atur),
]