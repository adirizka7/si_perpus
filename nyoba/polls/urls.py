from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexHome.as_view(), name='home'),
    url(r'^cari/$', views.cari, name='cari'),
    url(r'^(?P<nim>[a-zA-Z0-9_]+)/$', views.Searched.as_view(), name='searched'),
    #url(r'^updatedata/$', views.crud.updatedata, name='updatedata'),
    #url(r'^([0-9]+)/editdata/$', views.crud.editdata, name='editdata'),
    #url(r'^([0-9]+)/deletedata/$', views.crud.deletedata, name='deletedata'),
]
