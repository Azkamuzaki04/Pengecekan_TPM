from django.contrib import admin
from .models import Barang, Parameter

@admin.register(Barang)
class BarangAdmin(admin.ModelAdmin):
    list_display = ('kode_barang','nama_barang','barcode','model','status','created_at')
    search_fields = ('kode_barang','nama_barang','barcode')
    list_filter = ('status',)

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('urutan','nama_parameter','barang','tipe_input','wajib')
    list_filter = ('tipe_input','wajib')
    search_fields = ('nama_parameter','barang__nama_barang')
