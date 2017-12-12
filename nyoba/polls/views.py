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

from .models import *

class home(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/home.html'

class login(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/login.html'

class logout(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/login.html'

class cek_status(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/cek_status.html'

class tambah_data(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/tambah_data.html'
	context_object_name = 'dropp'
	def get_queryset(self):
		return Mahasiswa.objects.all()

class rekap_data(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/rekap_data.html'

class import_csv(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/import_csv.html'


def import_csv_process(request):
	if request.POST:
		print(os.getcwd())
		tipe = request.POST['tipe']
		file_doc = request.FILES['file_doc']
		print(tipe)
		print()
		with open('temp/'+'TEMP'+'.xlsx','wb+') as dest:
			for chunk in file_doc.chunks():
				dest.write(chunk)

		import xlrd
		import csv

		csvPath = 'temp/'+'TEMP'+'.csv'
		workBook = xlrd.open_workbook('temp/'+'TEMP'+'.xlsx')
		nama_sheet = workBook.sheet_names()
		list_sheet = []
		length = len(nama_sheet)
		for i in range(0,length):
			sheet =  workBook.sheet_by_name(nama_sheet[i])
			list_sheet.append(sheet)
		outcsvFile = open(csvPath, 'w')
		wr = csv.writer(outcsvFile, quoting=csv.QUOTE_ALL)
		total_row = list_sheet[0].ncols
		for k in range(0,len(list_sheet)):
			for rownum in range(list_sheet[k].nrows):
				wr.writerow(list_sheet[k].row_values(rownum))

		outcsvFile.close()

	return HttpResponseRedirect(reverse('polls:import_csv'))

class Searched(generic.ListView):
	template_name = 'polls/temuan.html'
	context_object_name = 'searcheded'
	def get_context_data(self, **kwargs):
		context = super(Searched, self).get_context_data(**kwargs)
		skripsi = Skripsi.objects.filter(NIM__icontains=self.kwargs['nim'])
		tesis = Tesis.objects.filter(NIM__icontains=self.kwargs['nim'])
		pn = Penyerahan.objects.filter(NIM__icontains=self.kwargs['nim'])
		if skripsi:
			context['skripsi'] = skripsi[0].judul_IND
		elif tesis:
			context['tesis'] = tesis[0].judul_IND
		try:
			mahasiswa = Mahasiswa.objects.get(NIM__icontains=self.kwargs['nim'])
		except Mahasiswa.DoesNotExist:
			mahasiswa = None
		buku = BukuS.objects.filter(penyumbang=mahasiswa)
		if buku:
			context['buku'] = buku[0].judul
		if pn:
			context['pnc'] = pn[0].s_cd
			context['pna'] = pn[0].s_abstrak
		return context
	def get_queryset(self):
		nim_argument = self.kwargs['nim']
		nim_argument = nim_argument.upper()
		return Mahasiswa.objects.filter(NIM__icontains=nim_argument)

def cari(request):
	alfa = request.POST['search']
	return HttpResponseRedirect(reverse('polls:searched', args=[alfa]))

def savedata_sumbangan(request, nim):
	if request.POST:
		judul=request.POST['judul']
		penulis=request.POST['penulis']
		tahun=request.POST['tahun']
		m = Mahasiswa.objects.filter(NIM__icontains=nim)
		name = m[0].nama
		b = BukuS(judul = judul, nama_penulis = penulis, pub_date = tahun, penyumbang = name)
		b.save()
	return HttpResponseRedirect(reverse('polls:searched', args=[nim]))

def savedata_cd(request, nim):
	if request.POST:
		cd=request.POST['cd']
		if cd=='y':
			pn = Penyerahan.objects.filter(NIM__icontains=nim).update(s_cd=1)
	return HttpResponseRedirect(reverse('polls:searched', args=[nim]))

def savedata_abstrak(request, nim):
	if request.POST:
		ab=request.POST['abs']
		if ab=='y':
			pn = Penyerahan.objects.filter(NIM__icontains=nim).update(s_abstrak=1)
	return HttpResponseRedirect(reverse('polls:searched', args=[nim]))

def savedata_skripsi(request):
	if request.POST:
		nama=request.POST['nama']
		nim=request.POST['nim']
		if Mahasiswa.objects.filter(NIM__icontains=nim).exists():
			sv = Skripsi(judul_IND=request.POST['IND'], judul_ENG=request.POST['ENG'], nama_penulis=nama, NIM=nim, pembimbing=request.POST['pembimbing'], penguji=request.POST['penguji'], tanggal_penyerahan=request.POST['tanggal'], tanggal_lulus=request.POST['lulus'],pub_date=timezone.now())
			sv.save()
		else:
			mv = Mahasiswa(nama = nama, NIM = nim, status = 0)
			mv.save()
			pn = Penyerahan(NIM = nim, s_abstrak = 0, s_cd = 0, buku=0)
			pn.save()
			sv = Skripsi(judul_IND=request.POST['IND'], judul_ENG=request.POST['ENG'], nama_penulis=nama, NIM=nim, pembimbing=request.POST['pembimbing'], penguji=request.POST['penguji'], tanggal_penyerahan=request.POST['tanggal'], tanggal_lulus=request.POST['lulus'],pub_date=timezone.now())
			sv.save()
	# return redirect()
	return HttpResponseRedirect(reverse('polls:tambah_data'))

def savedata_tesis(request):
	if request.POST:
		nama=request.POST['nama1']
		nim=request.POST['nim1']
		if Mahasiswa.objects.filter(NIM__icontains=nim).exists():
			sv = Tesis(judul_IND=request.POST['IND1'], judul_ENG=request.POST['ENG1'],  ps=request.POST['ps'], nama_penulis=nama, NIM=nim, pembimbing=request.POST['pembimbing1'], penguji=request.POST['penguji1'], tanggal_penyerahan=request.POST['tanggal1'], tanggal_lulus=request.POST['lulus1'],pub_date=timezone.now())
			sv.save()
		else:
			mv = Mahasiswa(nama = nama, NIM = nim, status = 0)
			mv.save()
			pn = Penyerahan(NIM = nim, s_abstrak = 0, s_cd = 0, buku=0)
			pn.save()
			sv = Tesis(judul_IND=request.POST['IND1'], judul_ENG=request.POST['ENG1'],  ps=request.POST['ps'], nama_penulis=nama, NIM=nim, pembimbing=request.POST['pembimbing1'], penguji=request.POST['penguji1'], tanggal_penyerahan=request.POST['tanggal1'], tanggal_lulus=request.POST['lulus1'],pub_date=timezone.now())
			sv.save()
	return HttpResponseRedirect(reverse('polls:tambah_data'))
