from django.urls import path
from .views import *

app_name = 'kelas'

urlpatterns = [
    # Kelas URLs
    path('kelas/', KelasViewSet.as_view({'get': 'list', 'post': 'create'}), name='kelas-list'),
    path('kelas/<slug:slug>/', KelasViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='kelas-detail'),
    path('kelas/<slug:slug>/santri/', KelasViewSet.as_view({'get': 'santri'}), name='kelas-santri'),
    path('kelas/<slug:slug>/kegiatan/', KelasViewSet.as_view({'get': 'kegiatan'}), name='kelas-kegiatan'),
    
    # Santri URLs
    path('santri/', SantriViewSet.as_view({'get': 'list', 'post': 'create'}), name='santri-list'),
    path('santri/<int:pk>/', SantriViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='santri-detail'),
    path('santri/<int:pk>/ngaji-records/', SantriViewSet.as_view({'get': 'ngaji_records'}), name='santri-ngaji-records'),
    
    # Ngaji URLs
    path('ngaji/', NgajiViewSet.as_view({'get': 'list', 'post': 'create'}), name='ngaji-list'),
    path('ngaji/<int:pk>/', NgajiViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='ngaji-detail'),
    
    # Kegiatan URLs
    path('kegiatan/', KegiatanViewSet.as_view({'get': 'list', 'post': 'create'}), name='kegiatan-list'),
    path('kegiatan/<int:pk>/', KegiatanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='kegiatan-detail'),
]