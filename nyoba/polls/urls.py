from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required



from . import views

## login - tinggal panggil login_required() di page yang diinginkan

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.home.as_view(), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'polls/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'polls/login.html'}, name='logout'),
    url(r'^tambah_data/$', views.tambah_data.as_view(), name='tambah_data'),
    url(r'^tambah_data/skripsi/$', views.savedata_skripsi, name='skripsi'),
    url(r'^tambah_data/tesis/$', views.savedata_tesis, name='tesis'),
    url(r'^Peminjaman/$', views.pinjam.as_view(), name='pinjam'),
    url(r'^Peminjaman/savedata_pinjam/$', views.savedata_pinjam, name='savedata_pinjam'),
    url(r'^rekap_data/$', views.rekap_data.as_view(), name='rekap_data'),
    url(r'^rekap_data/(?P<id>[a-zA-Z0-9_]+)/$', views.rekapsm, name='rekap_data_simpan'),
    url(r'^rekap_data_skripsi/$', views.rekap_data_skripsi.as_view(), name='rekap_data_skripsi'),
    url(r'^rekap_data_tesis/$', views.rekap_data_tesis.as_view(), name='rekap_data_tesis'),
    url(r'^import_csv/$', views.import_csv.as_view(), name='import_csv'),
    url(r'^import_csv/proc$', views.import_csv_process, name='import_csv_process'),
    url(r'^import_csv/get$', views.import_csv_get, name='import_csv_get'),
    url(r'^cek_status/$', views.cek_status.as_view(), name='cek_status'),
    url(r'^cek_status/cari/$', views.cari, name='cari'),
    url(r'^cek_status/kembali/(?P<nim>[a-zA-Z0-9_]+)/(?P<id>[a-zA-Z0-9_]+)/$', views.sudah_mengembalikan, name='sudah_mengembalikan'),
    url(r'^cek_status/(?P<nim>[a-zA-Z0-9_]+)/$', views.Searched.as_view(), name='searched'),
    url(r'^cek_status/(?P<nim>[a-zA-Z0-9_]+)/buku_sumbangan/$', views.savedata_sumbangan, name='buku_sumbangan'),
    url(r'^cek_status/(?P<nim>[a-zA-Z0-9_]+)/cd/$', views.savedata_cd, name='cdyn'),
    url(r'^cek_status/(?P<nim>[a-zA-Z0-9_]+)/abstrak/$', views.savedata_abstrak, name='abstrakyn'),
    #url(r'^updatedata/$', views.crud.updatedata, name='updatedata'),
    #url(r'^([0-9]+)/editdata/$', views.crud.editdata, name='editdata'),
    #url(r'^([0-9]+)/deletedata/$', views.crud.deletedata, name='deletedata'),
]
