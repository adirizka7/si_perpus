import datetime
from django.db import models
from django.utils import timezone

class Skripsi(models.Model):
	judul_IND = models.CharField(max_length=200)
	judul_ENG = models.CharField(max_length=200)
	nama_penulis = models.CharField(max_length=200)
	NIM = models.CharField(max_length=200)
	pembimbing = models.CharField(max_length=200)
	penguji = models.CharField(max_length=200)
	tanggal_lulus = models.DateTimeField(null=True, blank=True)
	tanggal_penyerahan = models.DateTimeField(null=True, blank=True)
	pub_date = models.DateTimeField(default=timezone.now())

	class Meta:
		db_table = u'polls_Skripsi'

	def __str__(self):
		return self.judul_IND

class Tesis(models.Model):
	judul_IND = models.CharField(max_length=200)
	judul_ENG = models.CharField(max_length=200)
	ps = models.CharField(max_length=50)
	nama_penulis = models.CharField(max_length=200)
	NIM = models.CharField(max_length=200)
	pembimbing = models.CharField(max_length=200)
	penguji = models.CharField(max_length=200)
	tanggal_lulus = models.DateTimeField(null=True, blank=True)
	tanggal_penyerahan = models.DateTimeField(null=True, blank=True)
	no_panggil = models.CharField(max_length=200)
	pub_date = models.DateTimeField(default=timezone.now())

	class Meta:
		db_table = u'polls_Tesis'

	def __str__(self):
		return self.judul_IND

class BukuS(models.Model):
	judul = models.CharField(max_length=200)
	nama_penulis = models.CharField(max_length=200)
	penyumbang = models.CharField(max_length=200)
	pub_date = models.IntegerField(default=1945)

	class Meta:
		db_table = u'polls_BukuS'

	def __str__(self):
		return self.judul

class Peminjaman(models.Model):
	nama = models.CharField(max_length=200)
	NIM = models.CharField(max_length=200)
	judul = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	barcode = models.CharField(max_length=200)
	pengarang = models.CharField(max_length=200)
	tanggal_pinjam = models.DateTimeField(null=True, blank=True)
	tanggal_kembali = models.DateTimeField(null=True, blank=True)
	tanggal_kembali_riil = models.DateTimeField(null=True, blank=True)
	pub_date = models.DateTimeField(default=timezone.now())

	class Meta:
		db_table = u'polls_Peminjaman'

	def __str__(self):
		return self.judul

class Mahasiswa(models.Model):
	nama = models.CharField(max_length=200)
	NIM = models.CharField(max_length=200)
	status = models.BooleanField()

	class Meta:
		db_table = u'polls_Mahasiswa'

	def __str__(self):
		return self.nama

class Penyerahan(models.Model):
	mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
	buku = models.ForeignKey(BukuS, on_delete=models.CASCADE)
	s_abstrak = models.BooleanField()
	s_cd = models.BooleanField()

	class Meta:
		db_table = u'polls_Penyerahan'
