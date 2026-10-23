from django.contrib.auth.models import User
from django.db import models

from barang.models import Barang, Parameter, TemplateParameter


# =========================================================
# LAPORAN INSPEKSI
# =========================================================

class LaporanInspeksi(models.Model):

    STATUS_HASIL = [
        ("OK", "OK"),
        ("NG", "NG"),
    ]

    STATUS_APPROVAL = [
        ("DRAFT", "Draft"),
        ("PENDING", "Pending Approval"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    nomor_laporan = models.CharField(
        max_length=50,
        unique=True,
    )

    barang = models.ForeignKey(
        Barang,
        on_delete=models.PROTECT,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    tanggal_inspeksi = models.DateTimeField(
        auto_now_add=True,
    )

    status_hasil = models.CharField(
        max_length=10,
        choices=STATUS_HASIL,
    )

    status_approval = models.CharField(
        max_length=20,
        choices=STATUS_APPROVAL,
        default="PENDING",
    )

    catatan = models.TextField(
        blank=True,
        null=True,
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="approved_reports",
    )

    approved_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.nomor_laporan


# =========================================================
# HASIL INSPEKSI
# =========================================================

class HasilInspeksi(models.Model):

    HASIL = [
        ("PASS", "OK"),
        ("FAIL", "NG"),
        ("SKIP", "Tidak Diisi"),
    ]

    STATUS_REPAIR = [
        ("REPAIRED", "Sudah Repair"),
        ("NOT_REPAIRED", "Belum Repair"),
    ]

    laporan = models.ForeignKey(
        LaporanInspeksi,
        on_delete=models.CASCADE,
        related_name="hasil_parameter",
    )

    # =====================================================
    # PARAMETER LAMA
    # =====================================================
    # Tetap dipertahankan agar hasil inspeksi lama
    # yang sudah tersimpan tidak rusak.
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    # =====================================================
    # TEMPLATE PARAMETER BARU
    # =====================================================
    # Digunakan untuk inspeksi baru berdasarkan
    # jenis equipment.
    template_parameter = models.ForeignKey(
        TemplateParameter,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="hasil_inspeksi",
    )

    nilai_hasil = models.CharField(
        max_length=100,
        blank=True,
    )

    hasil = models.CharField(
        max_length=10,
        choices=HASIL,
    )

    status_repair = models.CharField(
        max_length=20,
        choices=STATUS_REPAIR,
        blank=True,
        null=True,
    )

    catatan = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):

        nama_parameter = "-"

        if self.template_parameter:
            nama_parameter = self.template_parameter.nama_parameter

        elif self.parameter:
            nama_parameter = self.parameter.nama_parameter

        return (
            f"{self.laporan.nomor_laporan} - "
            f"{nama_parameter}"
        )


# =========================================================
# FOTO INSPEKSI
# =========================================================

class FotoInspeksi(models.Model):

    JENIS_FOTO = [
        ("BARCODE", "Barcode"),
        ("BARANG", "Barang"),
        ("NG", "Bukti NG"),
    ]

    laporan = models.ForeignKey(
        LaporanInspeksi,
        on_delete=models.CASCADE,
        related_name="foto",
    )

    hasil_inspeksi = models.ForeignKey(
        HasilInspeksi,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="foto_ng",
    )

    jenis_foto = models.CharField(
        max_length=20,
        choices=JENIS_FOTO,
    )

    file = models.ImageField(
        upload_to="inspection/%Y/%m/%d/",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.laporan.nomor_laporan} - "
            f"{self.jenis_foto}"
        )