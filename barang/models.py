from django.db import models


# ============================================================
# BARANG
# ============================================================

class Barang(models.Model):

    # --------------------------------------------------------
    # JENIS EQUIPMENT UTAMA
    # --------------------------------------------------------

    JENIS_EQUIPMENT = [
        ("TRAFO_GUN", "Trafo & Gun"),
        ("ELECTRICAL_AIR_HOIST", "Electrical & Air Hoist"),
        ("HANGER", "Hanger"),
        ("BALANCER", "Balancer"),
        ("TROLLEY", "Trolley"),
        ("KBK_REL", "KBK Rel"),
    ]

    # --------------------------------------------------------
    # SUB JENIS EQUIPMENT
    #
    # Tidak semua jenis equipment membutuhkan sub jenis.
    #
    # Contoh:
    # Trafo & Gun
    #   -> Trafo
    #   -> Gun
    #
    # Electrical & Air Hoist
    #   -> Electrical Hoist
    #   -> Air Hoist
    #
    # Balancer / Hanger / Trolley / KBK Rel
    #   -> Tidak ada
    # --------------------------------------------------------

    SUB_JENIS_EQUIPMENT = [
        ("", "Tidak ada"),

        ("TRAFO", "Trafo"),
        ("GUN", "Gun"),

        ("ELECTRICAL_HOIST", "Electrical Hoist"),
        ("AIR_HOIST", "Air Hoist"),
    ]

    # --------------------------------------------------------
    # DATA BARANG
    # --------------------------------------------------------

    kode_barang = models.CharField(
        max_length=50
    )

    nama_barang = models.CharField(
        max_length=150
    )

    jenis_equipment = models.CharField(
        max_length=30,
        choices=JENIS_EQUIPMENT,
        blank=True,
        null=True
    )

    sub_jenis_equipment = models.CharField(
        max_length=30,
        choices=SUB_JENIS_EQUIPMENT,
        blank=True,
        default=""
    )

    barcode = models.CharField(
        max_length=100,
        unique=True
    )

    model = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    deskripsi = models.TextField(
        blank=True,
        null=True
    )

    gambar = models.ImageField(
        upload_to="barang/",
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["kode_barang"]

    def __str__(self):
        return f"{self.kode_barang} - {self.nama_barang}"


# ============================================================
# PARAMETER LAMA
# ============================================================

class Parameter(models.Model):
    """
    Model Item Pemeriksaan lama.

    Tetap dipertahankan agar:
    - data lama tidak rusak
    - history inspeksi lama tetap aman
    - kompatibilitas dengan sistem sebelumnya tetap terjaga

    Sistem template baru menggunakan TemplateParameter.
    """

    TIPE_INPUT = [
        ("okng", "OK / NG"),
        ("number", "Nilai Angka"),
        ("text", "Teks"),
        ("select", "Pilihan"),
    ]

    barang = models.ForeignKey(
        Barang,
        on_delete=models.CASCADE,
        related_name="parameters"
    )

    urutan = models.PositiveIntegerField(
        default=1
    )

    nama_parameter = models.CharField(
        max_length=150
    )

    instruksi = models.TextField(
        blank=True,
        null=True
    )

    standar = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    satuan = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    nilai_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    nilai_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    tipe_input = models.CharField(
        max_length=20,
        choices=TIPE_INPUT,
        default="okng"
    )

    opsi_pilihan = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Pisahkan pilihan dengan koma."
    )

    wajib = models.BooleanField(
        default=True
    )

    foto_referensi = models.ImageField(
        upload_to="parameter_reference/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "barang",
            "urutan",
            "id"
        ]

    def __str__(self):
        return (
            f"{self.barang.nama_barang} - "
            f"{self.nama_parameter}"
        )


# ============================================================
# TEMPLATE PARAMETER
# ============================================================

class TemplateParameter(models.Model):
    """
    Template Item Pemeriksaan berdasarkan:

        1. JENIS EQUIPMENT
        2. SUB JENIS EQUIPMENT

    Contoh:

        BALANCER
            sub jenis = kosong
                -> Bottom Hook
                -> Latch
                -> Swivel Bottom Hook
                -> dst.

        HANGER
            sub jenis = kosong
                -> Sambungan Las
                -> Body
                -> Rantai
                -> dst.

        TRAFO & GUN
            sub jenis = TRAFO
                -> item pemeriksaan Trafo

        TRAFO & GUN
            sub jenis = GUN
                -> item pemeriksaan Gun

        ELECTRICAL & AIR HOIST
            sub jenis = ELECTRICAL_HOIST
                -> item pemeriksaan Electrical Hoist

        ELECTRICAL & AIR HOIST
            sub jenis = AIR_HOIST
                -> item pemeriksaan Air Hoist

    Semua barang dengan kombinasi jenis + sub jenis
    yang sama akan menggunakan template yang sama.
    """

    # --------------------------------------------------------
    # PILIHAN JENIS EQUIPMENT
    # --------------------------------------------------------

    JENIS_EQUIPMENT = Barang.JENIS_EQUIPMENT

    # --------------------------------------------------------
    # PILIHAN SUB JENIS EQUIPMENT
    # --------------------------------------------------------

    SUB_JENIS_EQUIPMENT = Barang.SUB_JENIS_EQUIPMENT

    # --------------------------------------------------------
    # JENIS INPUT
    # --------------------------------------------------------

    TIPE_INPUT = Parameter.TIPE_INPUT

    # --------------------------------------------------------
    # JENIS EQUIPMENT
    # --------------------------------------------------------

    jenis_equipment = models.CharField(
        max_length=30,
        choices=JENIS_EQUIPMENT
    )

    # --------------------------------------------------------
    # SUB JENIS EQUIPMENT
    # --------------------------------------------------------

    sub_jenis_equipment = models.CharField(
        max_length=30,
        choices=SUB_JENIS_EQUIPMENT,
        blank=True,
        default=""
    )

    # --------------------------------------------------------
    # DATA ITEM PEMERIKSAAN
    # --------------------------------------------------------

    urutan = models.PositiveIntegerField(
        default=1
    )

    nama_parameter = models.CharField(
        max_length=150
    )

    instruksi = models.TextField(
        blank=True,
        null=True
    )

    standar = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    satuan = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    nilai_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    nilai_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    tipe_input = models.CharField(
        max_length=20,
        choices=TIPE_INPUT,
        default="okng"
    )

    opsi_pilihan = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Pisahkan pilihan dengan koma."
    )

    wajib = models.BooleanField(
        default=True
    )

    foto_referensi = models.ImageField(
        upload_to="template_parameter/",
        blank=True,
        null=True
    )

    aktif = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "jenis_equipment",
            "sub_jenis_equipment",
            "urutan",
            "id"
        ]

    def __str__(self):
        jenis = self.get_jenis_equipment_display()

        if self.sub_jenis_equipment:
            sub_jenis = self.get_sub_jenis_equipment_display()
            return (
                f"{jenis} / {sub_jenis} - "
                f"{self.nama_parameter}"
            )

        return (
            f"{jenis} - "
            f"{self.nama_parameter}"
        )