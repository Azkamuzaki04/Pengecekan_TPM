from decimal import Decimal, InvalidOperation
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from accounts.views import get_role
from barang.models import Barang
from .models import FotoInspeksi, HasilInspeksi, LaporanInspeksi


def _parameter_result(parameter, raw_value):
    value = str(raw_value or "").strip()
    if parameter.tipe_input == "okng":
        return "PASS" if value.upper() == "OK" else "FAIL" if value.upper() == "NG" else "SKIP"
    if not value:
        return "SKIP"
    if parameter.tipe_input == "number":
        try:
            numeric = Decimal(value.replace(",", "."))
        except (InvalidOperation, ValueError):
            return "FAIL"
        if parameter.nilai_min is not None and numeric < parameter.nilai_min:
            return "FAIL"
        if parameter.nilai_max is not None and numeric > parameter.nilai_max:
            return "FAIL"
    return "PASS"


def _next_report_number():
    return f"INS-{timezone.now():%Y%m%d}-{uuid4().hex[:6].upper()}"


@login_required
def mulai_inspeksi(request, barang_id):
    # =====================================================
    # AMBIL BARANG
    # =====================================================

    barang = get_object_or_404(
        Barang,
        pk=barang_id,
        status=True,
    )

    # =====================================================
    # AMBIL TEMPLATE BERDASARKAN JENIS EQUIPMENT
    # =====================================================

    from barang.models import TemplateParameter

    template_parameters = list(
        TemplateParameter.objects.filter(
            jenis_equipment=barang.jenis_equipment,
            sub_jenis_equipment=barang.sub_jenis_equipment,
            aktif=True,
        ).order_by(
            "urutan",
            "id",
        )
    )

    # =====================================================
    # JIKA BELUM ADA TEMPLATE
    # =====================================================

    if not template_parameters:
        messages.warning(
            request,
            f"Belum ada template pemeriksaan untuk "
            f"{barang.get_jenis_equipment_display()}."
        )

        return redirect("cari_barang")

    # =====================================================
    # POST = SIMPAN HASIL INSPEKSI
    # =====================================================

    if request.method == "POST":

        with transaction.atomic():

            laporan = LaporanInspeksi.objects.create(
                nomor_laporan=_next_report_number(),
                barang=barang,
                user=request.user,
                status_hasil="OK",
                status_approval="PENDING",
                catatan=request.POST.get(
                    "catatan",
                    ""
                ).strip(),
            )

            all_pass = True

            # =============================================
            # LOOP TEMPLATE PEMERIKSAAN
            # =============================================

            for template_parameter in template_parameters:

                value = request.POST.get(
                    f"parameter_{template_parameter.id}",
                    ""
                ).strip()

                hasil = _parameter_result(
                    template_parameter,
                    value,
                )

                # =========================================
                # ITEM WAJIB
                # =========================================

                if template_parameter.wajib and hasil != "PASS":
                    all_pass = False

                # =========================================
                # SIMPAN HASIL
                # =========================================

                h = HasilInspeksi.objects.create(
                    laporan=laporan,
                    parameter=None,
                    template_parameter=template_parameter,
                    nilai_hasil=value,
                    hasil=hasil,
                    catatan=request.POST.get(
                        f"catatan_{template_parameter.id}",
                        ""
                    ).strip(),
                )

                # =========================================
                # FOTO WAJIB JIKA NG
                # =========================================

                if hasil == "FAIL":

                    photo = request.FILES.get(
                        f"foto_ng_{template_parameter.id}"
                    )

                    if not photo:

                        transaction.set_rollback(True)

                        messages.error(
                            request,
                            "Foto wajib untuk item NG: "
                            f"{template_parameter.nama_parameter}."
                        )

                        return render(
                            request,
                            "inspection/form.html",
                            {
                                "barang": barang,
                                "parameters": template_parameters,
                            },
                        )

                    FotoInspeksi.objects.create(
                        laporan=laporan,
                        hasil_inspeksi=h,
                        jenis_foto="NG",
                        file=photo,
                    )

            # =============================================
            # STATUS LAPORAN
            # =============================================

            laporan.status_hasil = (
                "OK"
                if all_pass
                else "NG"
            )

            laporan.save(
                update_fields=[
                    "status_hasil",
                    "updated_at",
                ]
            )

        messages.success(
            request,
            f"Laporan {laporan.nomor_laporan} "
            "berhasil dikirim untuk approval."
        )

        return redirect(
            "inspection_detail",
            laporan_id=laporan.id,
        )

    # =====================================================
    # GET = TAMPILKAN FORM
    # =====================================================

    return render(
        request,
        "inspection/form.html",
        {
            "barang": barang,
            "parameters": template_parameters,
        },
    )

@login_required
def history(request):
    qs = LaporanInspeksi.objects.select_related("barang", "user").prefetch_related("hasil_parameter__parameter", "foto").order_by("-tanggal_inspeksi")
    if get_role(request.user) != "ADMIN":
        qs = qs.filter(user=request.user)
    return render(request, "inspection/history.html", {"laporan_list": qs[:200]})


@login_required
def detail(request, laporan_id):
    laporan = get_object_or_404(LaporanInspeksi.objects.select_related("barang", "user", "approved_by").prefetch_related("hasil_parameter__parameter", "hasil_parameter__foto_ng", "foto"), pk=laporan_id)
    if get_role(request.user) == "PETUGAS" and laporan.user_id != request.user.id:
        return HttpResponseForbidden("Anda tidak memiliki akses ke laporan ini.")
    return render(request, "inspection/detail.html", {"laporan": laporan})


@login_required
def approval(request):
    if get_role(request.user) != "ADMIN":
        return HttpResponseForbidden("Halaman approval hanya untuk administrator.")
    status = request.GET.get("status", "PENDING")
    allowed = {"PENDING", "APPROVED", "REJECTED", "ALL"}
    if status not in allowed: status = "PENDING"
    qs = LaporanInspeksi.objects.select_related("barang", "user", "approved_by").order_by("-tanggal_inspeksi")
    if status != "ALL": qs = qs.filter(status_approval=status)
    return render(request, "inspection/approval.html", {"laporan_list": qs, "status_filter": status})


@login_required
def approval_action(request, laporan_id, action):
    if get_role(request.user) != "ADMIN":
        return HttpResponseForbidden("Akses ditolak.")
    if request.method != "POST" or action not in {"approve", "reject"}:
        return redirect("approval")
    laporan = get_object_or_404(LaporanInspeksi, pk=laporan_id)
    laporan.status_approval = "APPROVED" if action == "approve" else "REJECTED"
    note = request.POST.get("catatan", "").strip()
    if action == "reject" and not note:
        messages.error(request, "Alasan reject wajib diisi.")
        return redirect("inspection_detail", laporan_id=laporan.id)
    laporan.catatan = note or laporan.catatan
    laporan.approved_by = request.user
    laporan.approved_at = timezone.now()
    laporan.save(update_fields=["status_approval", "catatan", "approved_by", "approved_at", "updated_at"])
    messages.success(request, f"Laporan {laporan.nomor_laporan} telah {('disetujui' if action == 'approve' else 'ditolak')}.")
    return redirect("approval")


@login_required
def dashboard_user(request):
    mine = LaporanInspeksi.objects.filter(user=request.user)
    return render(request, "user/dashboard.html", {
        "inspection_count": mine.count(),
        "approved_count": mine.filter(status_approval="APPROVED").count(),
        "pending_count": mine.filter(status_approval="PENDING").count(),
        "ng_count": mine.filter(status_hasil="NG").count(),
        "recent_reports": mine.select_related("barang").order_by("-tanggal_inspeksi")[:5],
    })
