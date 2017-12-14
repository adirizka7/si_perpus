from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.core.validators import RegexValidator
from django.contrib import messages

from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings
from django.utils.encoding import smart_str

from django.views.static import serve

import os

from .models import *

class home(generic.ListView):
	model = Mahasiswa
	template_name = 'polls/home.html'

class pinjam(generic.ListView):
	model = Peminjaman
	template_name = 'polls/Peminjaman.html'

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
	model = Peminjaman
	template_name = 'polls/rekap_data.html'
	context_object_name = 'rekap_pinjaman'
	def get_queryset(self):
		return Peminjaman.objects.all().order_by("id")

class rekap_data_tesis(generic.ListView):
	model = Tesis
	template_name = 'polls/rekap_data_tesis.html'
	context_object_name = 'rekap_tesis'
	def get_queryset(self):
		return Tesis.objects.all().order_by("id")

class rekap_data_skripsi(generic.ListView):
	model = Skripsi
	template_name = 'polls/rekap_data_skripsi.html'
	context_object_name = 'rekap_skripsi'
	def get_queryset(self):
		return Skripsi.objects.all().order_by("id")

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

def import_csv_get(request):
	tipe = str(request.GET['tipe'])
	print(tipe)
	import sqlite3
	# tinggal ambil database sesuai nama tipe
	connection = sqlite3.connect("db.sqlite3")

	# polls_Skripsi
	# polls_Tesis
	# polls_Peminjaman
	# polls_BukuS

	with open("temp/"+tipe[6:]+".csv", "w") as write_file:
	    cursor = connection.cursor()
	    for row in cursor.execute("SELECT * FROM "+tipe):
	        writeRow = ",".join(str(v) for v in row)
	        write_file.write(writeRow)
	        write_file.write("\n")

	file_path = os.getcwd()+'/temp/'+tipe[6:]+'.csv'
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="text/csv")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response



class Searched(generic.ListView):
	template_name = 'polls/temuan.html'
	context_object_name = 'searcheded'
	def get_context_data(self, **kwargs):
		context = super(Searched, self).get_context_data(**kwargs)
		skripsi = Skripsi.objects.filter(NIM__icontains=self.kwargs['nim'])
		tesis = Tesis.objects.filter(NIM__icontains=self.kwargs['nim'])
		pn = Penyerahan.objects.filter(NIM__icontains=self.kwargs['nim'])
		jm = Peminjaman.objects.filter(NIM__icontains=self.kwargs['nim'])
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
		if jm:
			context['jm'] = jm
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
		messages.success(request, 'Form submission successful')
	return HttpResponseRedirect(reverse('polls:searched', args=[nim]))

def sudah_mengembalikan(request, nim, id):
	if request.POST:
		try:
			jm = Peminjaman.objects.get(id=id)
		except Mahasiswa.DoesNotExist:
			jm = None
		if jm:
			jm.status=1
			jm.tanggal_kembali_riil=timezone.now()
			jm.save()
		else:
			jm.status=1
			jm.tanggal_kembali_riil=timezone.now()
			jm.save()
		messages.success(request, 'Data Berhasil di update')
	return HttpResponseRedirect(reverse('polls:searched', args=[nim]))

def savedata_cd(request, nim):
	if request.POST:
		if Penyerahan.objects.filter(NIM__icontains=nim).exists():
			pass
		else:
			pn = Penyerahan(NIM = nim, s_abstrak = 0, s_cd = 0, buku=0)
			pn.save()
		cd=request.POST['cd']
		if cd=='y':
			pn = Penyerahan.objects.filter(NIM__icontains=nim).update(s_cd=1)
		elif cd=='n':
			pn = Penyerahan.objects.filter(NIM__icontains=nim).update(s_cd=0)
	return HttpResponseRedirect(reverse('polls:searched', args=[nim]))

def savedata_abstrak(request, nim):
	if request.POST:
		if Penyerahan.objects.filter(NIM__icontains=nim).exists():
			pass
		else:
			pn = Penyerahan(NIM = nim, s_abstrak = 0, s_cd = 0, buku=0)
			pn.save()
		ab=request.POST['abs']
		if ab=='y':
			pn = Penyerahan.objects.filter(NIM__icontains=nim).update(s_abstrak=1)
		elif ab=='n':
			pn = Penyerahan.objects.filter(NIM__icontains=nim).update(s_abstrak=0)
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
		messages.success(request, 'Form submission successful')
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
		messages.success(request, 'Form submission successful')
	return HttpResponseRedirect(reverse('polls:tambah_data'))

def savedata_pinjam(request):
	if request.POST:
		nama=request.POST['nama']
		nim=request.POST['nim']
		judul=request.POST['judul']
		phone=request.POST['phone']
		barcode=request.POST['barcode']
		pengarang=request.POST['pengarang']
		tg=request.POST['tanggal']
		pm=Peminjaman(nama=nama,NIM=nim,judul=judul,phone=phone,barcode=barcode,pengarang=pengarang,tanggal_pinjam=timezone.now(),tanggal_kembali=tg,pub_date=timezone.now())
		pm.save()
		messages.success(request, 'Form submission successful')
	return HttpResponseRedirect(reverse('polls:pinjam'))

def rekapsm(request, id):
	if request.POST:
		try:
			jm = Peminjaman.objects.get(id=id)
		except Peminjaman.DoesNotExist:
			jm = None
		if jm:
			if jm.status == 1:
				jm.status=0
			else:
				jm.status=1
			jm.tanggal_kembali_riil=timezone.now()
			jm.save()
			messages.success(request, 'Data Berhasil di update')
			return HttpResponseRedirect(reverse('polls:rekap_data'))
