from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Kelas, Santri, Ngaji, Kegiatan
from .serializers import KelasSerializer, SantriSerializer, NgajiSerializer, KegiatanSerializer
from .permissions import IsOwnerOrReadOnly

class KelasViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.all()
    serializer_class = KelasSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        queryset = Kelas.objects.all()
        if self.request.user.is_authenticated:
            # Authenticated user bisa lihat semua kelas
            return queryset
        else:
            # Anonymous user bisa lihat semua kelas (read-only)
            return queryset
    
    @action(detail=True, methods=['get'])
    def santri(self, request, slug=None):
        """Get all santri in this kelas"""
        kelas = self.get_object()
        santri = kelas.santri_set.all()
        serializer = SantriSerializer(santri, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def kegiatan(self, request, slug=None):
        """Get all kegiatan in this kelas"""
        kelas = self.get_object()
        kegiatan = kelas.kegiatan_set.all()
        serializer = KegiatanSerializer(kegiatan, many=True)
        return Response(serializer.data)

class SantriViewSet(viewsets.ModelViewSet):
    queryset = Santri.objects.all()
    serializer_class = SantriSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = Santri.objects.select_related('kelas')
        kelas_slug = self.request.query_params.get('kelas', None)
        if kelas_slug:
            queryset = queryset.filter(kelas__slug=kelas_slug)
        return queryset
    
    @action(detail=True, methods=['get'])
    def ngaji_records(self, request, pk=None):
        """Get all ngaji records for this santri"""
        santri = self.get_object()
        ngaji_records = santri.santri_ngaji.all().order_by('-tanggal')
        serializer = NgajiSerializer(ngaji_records, many=True)
        return Response(serializer.data)

class NgajiViewSet(viewsets.ModelViewSet):
    queryset = Ngaji.objects.all()
    serializer_class = NgajiSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = Ngaji.objects.select_related('nama', 'nama__kelas').order_by('-tanggal')
        santri_id = self.request.query_params.get('santri', None)
        kelas_slug = self.request.query_params.get('kelas', None)
        
        if santri_id:
            queryset = queryset.filter(nama_id=santri_id)
        if kelas_slug:
            queryset = queryset.filter(nama__kelas__slug=kelas_slug)
        
        return queryset

class KegiatanViewSet(viewsets.ModelViewSet):
    queryset = Kegiatan.objects.all()
    serializer_class = KegiatanSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = Kegiatan.objects.select_related('kelas').order_by('-tanggal')
        kelas_slug = self.request.query_params.get('kelas', None)
        if kelas_slug:
            queryset = queryset.filter(kelas__slug=kelas_slug)
        return queryset