from django.urls import path

from .views import (
    cari_barang,
    item_delete,
    item_form,
    master_barang,
    master_barang_detail,
    barang_form,
    barang_delete,

    # Template Item Pemeriksaan
    template_parameter_list,
    template_parameter_form,
    template_parameter_delete,
)


urlpatterns = [

    # =========================
    # CARI BARANG
    # =========================
    path(
        "cari/",
        cari_barang,
        name="cari_barang",
    ),


    # =========================
    # MASTER EQUIPMENT
    # =========================
    path(
        "master/",
        master_barang,
        name="master_barang",
    ),

    path(
        "master/tambah/",
        barang_form,
        name="master_barang_tambah",
    ),

    path(
        "master/<int:barang_id>/",
        master_barang_detail,
        name="master_barang_detail",
    ),

    path(
        "master/<int:barang_id>/edit/",
        barang_form,
        name="master_barang_edit",
    ),


    # =========================
    # HAPUS EQUIPMENT
    # =========================
    path(
        "master/<int:barang_id>/hapus/",
        barang_delete,
        name="barang_delete",
    ),


    # =========================
    # TEMPLATE ITEM PEMERIKSAAN
    # =========================
    path(
        "template/<str:jenis>/",
        template_parameter_list,
        name="template_parameter_list",
    ),

    path(
        "template/<str:jenis>/tambah/",
        template_parameter_form,
        name="template_parameter_tambah",
    ),

    path(
        "template/<str:jenis>/<int:template_id>/edit/",
        template_parameter_form,
        name="template_parameter_edit",
    ),

    path(
        "template/<str:jenis>/<int:template_id>/hapus/",
        template_parameter_delete,
        name="template_parameter_delete",
    ),


    # =========================
    # ITEM PEMERIKSAAN LAMA
    # =========================
    path(
        "master/<int:barang_id>/item/tambah/",
        item_form,
        name="item_tambah",
    ),

    path(
        "master/<int:barang_id>/item/<int:parameter_id>/edit/",
        item_form,
        name="item_edit",
    ),

    path(
        "master/item/<int:parameter_id>/hapus/",
        item_delete,
        name="item_delete",
    ),
]