from django.contrib import admin
from .models import LaporanInspeksi, HasilInspeksi, FotoInspeksi

class HasilInline(admin.TabularInline):
    model = HasilInspeksi
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(LaporanInspeksi)
class LaporanAdmin(admin.ModelAdmin):
    list_display = ('nomor_laporan','barang','user','status_hasil','status_approval','tanggal_inspeksi','approved_by')
    list_filter = ('status_hasil','status_approval')
    search_fields = ('nomor_laporan','barang__nama_barang','barang__barcode','user__username')
    inlines = [HasilInline]

@admin.register(FotoInspeksi)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('laporan','jenis_foto','hasil_inspeksi','created_at')
    list_filter = ('jenis_foto',)
