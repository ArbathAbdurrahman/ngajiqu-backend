from django.db import models
from django.contrib.auth.models import User

class Kelas(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kelas_dibimbing")
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.nama


class Santri(models.Model):
    nama = models.CharField(max_length=100)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name="santri_set")

    def __str__(self):
        return self.nama
    
class Ngaji(models.Model):
    nama = models.ForeignKey(Santri, on_delete=models.CASCADE, related_name="santri_ngaji")
    tanggal = models.DateField(auto_now=True)
    surat = models.CharField(max_length=255)
    ayat = models.PositiveIntegerField(default=0)
    pengampu = models.CharField(max_length=255)
    catatan = models.CharField(max_length=255)

    def __str__(self):
        return self.nama


class Kegiatan(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name="kegiatan_set")
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    tanggal = models.DateField()

    def __str__(self):
        return f"{self.nama} ({self.kelas.nama})"
