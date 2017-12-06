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

class IndexHome(generic.ListView):
	template_name = 'polls/cek_status.html'
	context_object_name = 'hal_cari'
	def output(request, nim):
		g = Mahasiswa.objects.filter(NIM__icontains=nim)
	def get_queryset(self):
		return g.objects.order_by('NIM')

class Searched(generic.ListView):
	template_name = 'polls/temuan.html'
	context_object_name = 'searcheded'
	def get_queryset(self):
		return Mahasiswa.objects.filter(NIM__icontains='uhuy')


def cari(request):
	alfa = request.POST['search']
	return HttpResponseRedirect(reverse('polls:searched', args=[alfa]))
