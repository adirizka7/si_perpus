from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect

from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings

import os

from .models import Mahasiswa

class home(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/home.html'

class login(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/login.html'

class cek_status(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/cek_status.html'

class tambah_syarat(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/tambah_syarat.html'

class rekap_data(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/rekap_data.html'

class import_csv(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/import_csv.html'


class Searched(generic.ListView):
	template_name = 'polls/temuan.html'
	context_object_name = 'searcheded'
	def get_queryset(self):
		nim_argument = self.kwargs['nim']
		nim_argument = nim_argument.upper()
		return Mahasiswa.objects.filter(NIM__icontains=nim_argument)


def cari(request):
	alfa = request.POST['search']
	return HttpResponseRedirect(reverse('polls:searched', args=[alfa]))
