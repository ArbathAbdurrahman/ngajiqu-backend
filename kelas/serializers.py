from rest_framework import serializers
from .models import Kelas, Santri, Ngaji, Kegiatan

class KelasSerializer(serializers.ModelSerializer):
    santri_count = serializers.SerializerMethodField()

    class Meta:
        model = Kelas
        fields = ['id', 'nama', 'deskripsi', 'author', 'slug', 'santri_count']
        extra_kwargs = {'author': {'required': False}}

    def get_santri_count(self, obj):
        return obj.santri_set.count()

class SantriSerializer(serializers.ModelSerializer):
    kelas_nama = serializers.CharField(source='kelas.nama', read_only=True)
    
    class Meta:
        model = Santri
        fields = ['id', 'nama', 'kelas', 'kelas_nama']

class NgajiSerializer(serializers.ModelSerializer):
    santri_nama = serializers.CharField(source='nama.nama', read_only=True)
    kelas_nama = serializers.CharField(source='nama.kelas.nama', read_only=True)
    
    class Meta:
        model = Ngaji
        fields = ['id', 'nama', 'santri_nama', 'kelas_nama', 'tanggal', 'surat', 'ayat', 'pengampu', 'catatan']

class KegiatanSerializer(serializers.ModelSerializer):
    kelas_nama = serializers.CharField(source='kelas.nama', read_only=True)
    
    class Meta:
        model = Kegiatan
        fields = ['id', 'kelas', 'kelas_nama', 'nama', 'deskripsi', 'tanggal']
