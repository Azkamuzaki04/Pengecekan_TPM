from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .models import Barang, Parameter, TemplateParameter
from .barcode_utils import generate_barcode


# =========================================================
# STAFF REQUIRED DECORATOR
# =========================================================

def staff_required(view):

    return user_passes_test(
        lambda u: u.is_authenticated and u.is_staff
    )(view)


# =========================================================
# CARI BARANG
# =========================================================

@login_required
def cari_barang(request):

    barcode = request.GET.get("barcode", "").strip()

    barang = None
    not_found = False

    if barcode:

        try:

            barang = (
                Barang.objects
                .prefetch_related("parameters")
                .get(
                    barcode=barcode,
                    status=True
                )
            )

        except Barang.DoesNotExist:

            not_found = True

    return render(
        request,
        "barang/cari.html",
        {
            "barang": barang,
            "barcode": barcode,
            "not_found": not_found,
        }
    )


# =========================================================
# MASTER EQUIPMENT
# =========================================================

@staff_required
def master_barang(request):

    q = request.GET.get("q", "").strip()

    jenis = request.GET.get(
        "jenis",
        ""
    ).strip()

    # -----------------------------------------------------
    # QUERY DASAR
    # -----------------------------------------------------

    qs = (
        Barang.objects
        .prefetch_related("parameters")
        .order_by("kode_barang")
    )

    # -----------------------------------------------------
    # FILTER JENIS EQUIPMENT
    # -----------------------------------------------------

    if jenis:

        qs = qs.filter(
            jenis_equipment=jenis
        )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if q:

        qs = qs.filter(
            Q(nama_barang__icontains=q)
            |
            Q(kode_barang__icontains=q)
            |
            Q(barcode__icontains=q)
        )

    # -----------------------------------------------------
    # NAMA EQUIPMENT YANG SEDANG DIPILIH
    # -----------------------------------------------------

    jenis_label = ""

    for value, label in Barang.JENIS_EQUIPMENT:

        if value == jenis:

            jenis_label = label

            break

    # -----------------------------------------------------
    # JUMLAH SETIAP EQUIPMENT
    # -----------------------------------------------------

    equipment_summary = []

    for value, label in Barang.JENIS_EQUIPMENT:

        total = Barang.objects.filter(
            jenis_equipment=value,
            status=True
        ).count()

        equipment_summary.append({
            "value": value,
            "label": label,
            "total": total,
        })

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        "admin/master_barang.html",
        {
            "barang_list": qs.distinct(),

            "q": q,

            "jenis": jenis,

            "jenis_label": jenis_label,

            "equipment_summary": equipment_summary,
        }
    )


# =========================================================
# FORM BARANG
# =========================================================

@staff_required
def barang_form(request, barang_id=None):

    barang = (
        get_object_or_404(Barang, pk=barang_id)
        if barang_id
        else None
    )

    if request.method == "POST":

        kode = request.POST.get(
            "kode_barang",
            ""
        ).strip()

        nama = request.POST.get(
            "nama_barang",
            ""
        ).strip()

        barcode = request.POST.get(
            "barcode",
            ""
        ).strip()


        # =================================================
        # VALIDASI DATA WAJIB
        # =================================================

        if not kode or not nama or not barcode:

            messages.error(
                request,
                "Kode, nama barang, dan barcode wajib diisi."
            )

        else:

            qs = (
                Barang.objects.exclude(pk=barang.pk)
                if barang
                else Barang.objects.all()
            )


            # =================================================
            # VALIDASI DUPLIKAT
            # =================================================

            if (
                qs.filter(barcode=barcode).exists()
            ):

                messages.error(
                    request,
                    "Barcode sudah digunakan. Gunakan barcode yang berbeda"
                )

            else:

                if barang is None:
                    barang = Barang()


                # =============================================
                # SIMPAN DATA BARANG
                # =============================================

                barang.kode_barang = kode
                barang.nama_barang = nama
                barang.barcode = barcode

                barang.model = request.POST.get(
                    "model",
                    ""
                ).strip()

                barang.jenis_equipment = request.POST.get(
                    "jenis_equipment",
                    ""
                ).strip()

                barang.sub_jenis_equipment = request.POST.get(
                    "sub_jenis_equipment",
                    ""
                ).strip()

                # Equipment yang tidak mempunyai subtype
                if barang.jenis_equipment not in [
                    "TRAFO_GUN",
                    "ELECTRICAL_AIR_HOIST",
                ]:
                    barang.sub_jenis_equipment = ""

                # Validasi subtype untuk Trafo & Gun
                if barang.jenis_equipment == "TRAFO_GUN":
                    if barang.sub_jenis_equipment not in [
                        "TRAFO",
                        "GUN",
                ]:
                        barang.sub_jenis_equipment = ""

                # Validasi subtype untuk Electrical & Air Hoist
                if barang.jenis_equipment == "ELECTRICAL_AIR_HOIST":
                    if barang.sub_jenis_equipment not in [
                        "ELECTRICAL_HOIST",
                        "AIR_HOIST",
                ]:
                        barang.sub_jenis_equipment = ""

                barang.deskripsi = request.POST.get(
                    "deskripsi",
                    ""
                ).strip()

                barang.status = (
                    request.POST.get("status") == "on"
                )


                # =============================================
                # UPLOAD GAMBAR
                # =============================================

                if request.FILES.get("gambar"):

                    barang.gambar = request.FILES["gambar"]


                # =============================================
                # SAVE
                # =============================================

                barang.save()

                generate_barcode(barang.barcode)

                messages.success(
                    request,
                    "Data barang berhasil disimpan dan barcode berhasil dibuat"
                )

                return redirect(
                    "master_barang_detail",
                    barang_id=barang.id
                )

    return render(
        request,
        "admin/master_barang_form.html",
        {
            "barang": barang
        }
    )


# =========================================================
# DETAIL MASTER BARANG
# =========================================================

@staff_required
def master_barang_detail(request, barang_id):

    barang = get_object_or_404(
        Barang.objects.prefetch_related("parameters"),
        pk=barang_id
    )

    return render(
        request,
        "admin/master_barang_detail.html",
        {
            "barang": barang
        }
    )

# =========================================================
# TEMPLATE ITEM PEMERIKSAAN PER JENIS EQUIPMENT
# =========================================================

@staff_required
def template_parameter_list(request, jenis):
    """
    Menampilkan template item pemeriksaan berdasarkan
    jenis equipment.

    Contoh:
        /barang/template/BALANCER/
        /barang/template/TROLLEY/
    """

    # Pastikan jenis equipment valid
    jenis_choices = dict(Barang.JENIS_EQUIPMENT)

    if jenis not in jenis_choices:
        messages.error(
            request,
            "Jenis equipment tidak ditemukan."
        )
        return redirect("master_barang")

    jenis_label = jenis_choices[jenis]

    template_list = (
        TemplateParameter.objects
        .filter(
            jenis_equipment=jenis,
            aktif=True
        )
        .order_by("urutan", "id")
    )

    # Jumlah equipment pada kategori tersebut
    total_equipment = Barang.objects.filter(
        jenis_equipment=jenis,
        status=True
    ).count()

    return render(
        request,
        "admin/template_parameter_list.html",
        {
            "jenis": jenis,
            "jenis_label": jenis_label,
            "template_list": template_list,
            "total_equipment": total_equipment,
        }
    )


@staff_required
def template_parameter_form(
    request,
    jenis,
    template_id=None
):
    """
    Tambah / edit template item pemeriksaan
    berdasarkan jenis equipment.
    """

    jenis_choices = dict(Barang.JENIS_EQUIPMENT)

    if jenis not in jenis_choices:
        messages.error(
            request,
            "Jenis equipment tidak ditemukan."
        )
        return redirect("master_barang")

    jenis_label = jenis_choices[jenis]

    template_parameter = (
        get_object_or_404(
            TemplateParameter,
            pk=template_id,
            jenis_equipment=jenis
        )
        if template_id
        else None
    )

    if request.method == "POST":

        # -------------------------------------------------
        # URUTAN
        # -------------------------------------------------

        try:
            urutan = int(
                request.POST.get(
                    "urutan",
                    "1"
                )
            )
        except (TypeError, ValueError):
            urutan = 1

        # -------------------------------------------------
        # INIT OBJECT
        # -------------------------------------------------

        if template_parameter is None:
            template_parameter = TemplateParameter(
                jenis_equipment=jenis
            )

        template_parameter.urutan = max(
            1,
            urutan
        )

        template_parameter.nama_parameter = (
            request.POST.get(
                "nama_parameter",
                ""
            ).strip()
        )

        template_parameter.instruksi = (
            request.POST.get(
                "instruksi",
                ""
            ).strip()
        )

        template_parameter.standar = (
            request.POST.get(
                "standar",
                ""
            ).strip()
        )

        template_parameter.satuan = (
            request.POST.get(
                "satuan",
                ""
            ).strip()
        )

        template_parameter.tipe_input = (
            request.POST.get(
                "tipe_input",
                "okng"
            )
        )

        template_parameter.opsi_pilihan = (
            request.POST.get(
                "opsi_pilihan",
                ""
            ).strip()
        )

        template_parameter.nilai_min = (
            request.POST.get(
                "nilai_min"
            )
            or None
        )

        template_parameter.nilai_max = (
            request.POST.get(
                "nilai_max"
            )
            or None
        )

        template_parameter.wajib = (
            request.POST.get(
                "wajib"
            ) == "on"
        )

        template_parameter.aktif = (
            request.POST.get(
                "aktif"
            ) == "on"
        )

        # -------------------------------------------------
        # FOTO REFERENSI
        # -------------------------------------------------

        if request.FILES.get(
            "foto_referensi"
        ):
            template_parameter.foto_referensi = (
                request.FILES[
                    "foto_referensi"
                ]
            )

        # -------------------------------------------------
        # VALIDASI
        # -------------------------------------------------

        if not template_parameter.nama_parameter:

            messages.error(
                request,
                "Nama pemeriksaan wajib diisi."
            )

        else:

            template_parameter.save()

            messages.success(
                request,
                "Template item pemeriksaan berhasil disimpan."
            )

            return redirect(
                "template_parameter_list",
                jenis=jenis
            )

    return render(
        request,
        "admin/template_parameter_form.html",
        {
            "jenis": jenis,
            "jenis_label": jenis_label,
            "template_parameter": template_parameter,
        }
    )


@staff_required
def template_parameter_delete(
    request,
    jenis,
    template_id
):
    """
    Menghapus template item pemeriksaan.
    """

    template_parameter = get_object_or_404(
        TemplateParameter,
        pk=template_id,
        jenis_equipment=jenis
    )

    if request.method == "POST":

        nama = template_parameter.nama_parameter

        template_parameter.delete()

        messages.success(
            request,
            f"Template item '{nama}' berhasil dihapus."
        )

    return redirect(
        "template_parameter_list",
        jenis=jenis
    )

@staff_required
def barang_delete(request, barang_id):
    barang = get_object_or_404(Barang, pk=barang_id)

    if request.method == "POST":
        nama_barang = barang.nama_barang
        barang.delete()

        messages.success(
            request,
            f"Equipment '{nama_barang}' berhasil dihapus."
        )

    return redirect("master_barang")

# =========================================================
# FORM ITEM PEMERIKSAAN
# =========================================================

@staff_required
def item_form(request, barang_id, parameter_id=None):

    barang = get_object_or_404(
        Barang,
        pk=barang_id
    )

    parameter = (
        get_object_or_404(
            Parameter,
            pk=parameter_id,
            barang=barang
        )
        if parameter_id
        else None
    )

    if request.method == "POST":

        try:

            urutan = int(
                request.POST.get(
                    "urutan",
                    "1"
                )
            )

        except ValueError:

            urutan = 1


        # =================================================
        # INIT PARAMETER
        # =================================================

        parameter = (
            parameter
            or Parameter(barang=barang)
        )

        parameter.urutan = max(
            1,
            urutan
        )

        parameter.nama_parameter = request.POST.get(
            "nama_parameter",
            ""
        ).strip()

        parameter.instruksi = request.POST.get(
            "instruksi",
            ""
        ).strip()

        parameter.standar = request.POST.get(
            "standar",
            ""
        ).strip()

        parameter.satuan = request.POST.get(
            "satuan",
            ""
        ).strip()

        parameter.tipe_input = request.POST.get(
            "tipe_input",
            "okng"
        )

        parameter.opsi_pilihan = request.POST.get(
            "opsi_pilihan",
            ""
        ).strip()

        parameter.nilai_min = (
            request.POST.get("nilai_min")
            or None
        )

        parameter.nilai_max = (
            request.POST.get("nilai_max")
            or None
        )

        parameter.wajib = (
            request.POST.get("wajib") == "on"
        )


        # =================================================
        # UPLOAD FOTO REFERENSI
        # =================================================

        if request.FILES.get("foto_referensi"):

            parameter.foto_referensi = (
                request.FILES["foto_referensi"]
            )


        # =================================================
        # VALIDASI NAMA PARAMETER
        # =================================================

        if not parameter.nama_parameter:

            messages.error(
                request,
                "Nama pemeriksaan wajib diisi."
            )

        else:

            parameter.save()

            messages.success(
                request,
                "Item pemeriksaan berhasil disimpan."
            )

            return redirect(
                "master_barang_detail",
                barang_id=barang.id
            )

    return render(
        request,
        "admin/item_form.html",
        {
            "barang": barang,
            "parameter": parameter,
        }
    )


# =========================================================
# HAPUS ITEM PEMERIKSAAN
# =========================================================

@staff_required
def item_delete(request, parameter_id):

    parameter = get_object_or_404(
        Parameter,
        pk=parameter_id
    )

    barang_id = parameter.barang_id

    if request.method == "POST":

        parameter.delete()

        messages.success(
            request,
            "Item pemeriksaan dihapus."
        )

    return redirect(
        "master_barang_detail",
        barang_id=barang_id
    )