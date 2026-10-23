from datetime import datetime
from calendar import monthrange
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from barang.models import Barang, Parameter
from inspection.models import LaporanInspeksi

from .models import UserProfile


# =========================================================
# ROLE
# =========================================================

def get_role(user):
    try:
        role = user.profile.role

        if role == "SERVER":
            return "SERVER"

        if role == "ADMIN":
            return "ADMIN"

        return "PETUGAS"

    except UserProfile.DoesNotExist:

        if user.is_superuser or user.is_staff:
            return "ADMIN"

        return "PETUGAS"


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        role = get_role(request.user)

        if role == "PETUGAS":
            return redirect("dashboard_user")

        if role == "SERVER":
            return redirect("server_dashboard")

        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            role = get_role(user)

            if role == "PETUGAS":
                return redirect("dashboard_user")

            if role == "SERVER":
                return redirect("server_dashboard")

            return redirect("dashboard")

        messages.error(
            request,
            "Username atau password salah."
        )

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


# =========================================================
# DASHBOARD ADMIN
# =========================================================

@login_required
def dashboard(request):
    """
    Dashboard Admin CHECKSHEET.

    Data dashboard mengikuti bulan dan tahun yang dipilih.
    Filter tanggal dilakukan di Python agar aman terhadap
    perbedaan DateField / DateTimeField dan timezone MySQL.
    """

    # =========================================================
    # CEK ROLE
    # =========================================================

    role = get_role(request.user)

    if role == "PETUGAS":
        return redirect("dashboard_user")

    if role == "SERVER":
        return redirect("server_dashboard")

    # =========================================================
    # PERIODE
    # =========================================================

    now = timezone.localdate()

    try:
        selected_month = int(
            request.GET.get(
                "month",
                now.month
            )
        )
    except (TypeError, ValueError):
        selected_month = now.month

    try:
        selected_year = int(
            request.GET.get(
                "year",
                now.year
            )
        )
    except (TypeError, ValueError):
        selected_year = now.year

    if selected_month < 1 or selected_month > 12:
        selected_month = now.month

    # =========================================================
    # NAMA BULAN
    # =========================================================

    month_names = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember",
    }

    selected_month_name = month_names[selected_month]

    # =========================================================
    # DATA EQUIPMENT
    # =========================================================

    total_equipment = (
        Barang.objects
        .filter(status=True)
        .count()
    )

    # =========================================================
    # AMBIL SEMUA LAPORAN
    #
    # Jangan langsung filter __year/__month.
    # Kita filter tanggal di Python supaya lebih aman.
    # =========================================================

    all_reports = list(
        LaporanInspeksi.objects
        .select_related(
            "barang",
            "user",
            "approved_by",
        )
        .order_by("-tanggal_inspeksi")
    )

    # =========================================================
    # FILTER BULAN DAN TAHUN
    # =========================================================

    month_reports = []

    for report in all_reports:

        tanggal = report.tanggal_inspeksi

        if not tanggal:
            continue

        # Mendukung DateField maupun DateTimeField
        if hasattr(tanggal, "date"):
            tanggal_date = tanggal.date()
        else:
            tanggal_date = tanggal

        if (
            tanggal_date.year == selected_year
            and tanggal_date.month == selected_month
        ):
            month_reports.append(report)

    # =========================================================
    # HELPER STATUS
    #
    # Dibuat case-insensitive dan aman jika ada spasi.
    # =========================================================

    def clean_status(value):
        if value is None:
            return ""

        return str(value).strip().upper()

    # =========================================================
    # KPI UTAMA
    # =========================================================

    total_inspection = len(month_reports)

    total_pending = sum(
        1
        for report in month_reports
        if clean_status(report.status_approval) == "PENDING"
    )

    total_approved = sum(
        1
        for report in month_reports
        if clean_status(report.status_approval) == "APPROVED"
    )

    total_rejected = sum(
        1
        for report in month_reports
        if clean_status(report.status_approval) == "REJECTED"
    )

    total_ok = sum(
        1
        for report in month_reports
        if clean_status(report.status_hasil) == "OK"
    )

    total_ng = sum(
        1
        for report in month_reports
        if clean_status(report.status_hasil) == "NG"
    )

    # =========================================================
    # KATEGORI EQUIPMENT
    # =========================================================

    equipment_categories = [

        {
            "code": "TRAFO_GUN",
            "name": "Trafo & Gun",
            "icon": "bi-lightning-charge",
        },

        {
            "code": "ELECTRICAL_AIR_HOIST",
            "name": "Electrical & Air Hoist",
            "icon": "bi-boxes",
        },

        {
            "code": "HANGER",
            "name": "Hanger",
            "icon": "bi-link-45deg",
        },

        {
            "code": "BALANCER",
            "name": "Balancer",
            "icon": "bi-sliders",
        },

        {
            "code": "TROLLEY",
            "name": "Trolley",
            "icon": "bi-cart3",
        },

        {
            "code": "KBK_REL",
            "name": "KBK Rel",
            "icon": "bi-diagram-3",
        },

    ]

    # =========================================================
    # DATA PER EQUIPMENT
    # =========================================================

    equipment_dashboard = []

    for equipment in equipment_categories:

        code = equipment["code"]

        # -----------------------------------------------------
        # TOTAL ITEM
        # -----------------------------------------------------

        total_item = (
            Barang.objects
            .filter(
                status=True,
                jenis_equipment__iexact=code,
            )
            .count()
        )

        # -----------------------------------------------------
        # LAPORAN KATEGORI
        # -----------------------------------------------------

        category_reports = []

        for report in month_reports:

            barang = report.barang

            if not barang:
                continue

            jenis = str(
                barang.jenis_equipment or ""
            ).strip().upper()

            if jenis == code:
                category_reports.append(report)

        # -----------------------------------------------------
        # PENDING
        # -----------------------------------------------------

        pending_count = sum(
            1
            for report in category_reports
            if clean_status(
                report.status_approval
            ) == "PENDING"
        )

        # -----------------------------------------------------
        # APPROVED
        # -----------------------------------------------------

        approved_reports = [
            report
            for report in category_reports
            if clean_status(
                report.status_approval
            ) == "APPROVED"
        ]

        approved_total = len(
            approved_reports
        )

        # -----------------------------------------------------
        # HASIL APPROVED
        #
        # Pie chart hanya menghitung laporan APPROVED.
        # -----------------------------------------------------

        approved_ok_count = sum(
            1
            for report in approved_reports
            if clean_status(
                report.status_hasil
            ) == "OK"
        )

        approved_ng_count = sum(
            1
            for report in approved_reports
            if clean_status(
                report.status_hasil
            ) == "NG"
        )

        # -----------------------------------------------------
        # FINISH CHECK
        #
        # Sesuai kebutuhan dashboard:
        # Finish Check = jumlah laporan APPROVED.
        #
        # September Trafo & Gun:
        # APPROVED = 6
        # -----------------------------------------------------

        finish_check = approved_total

        # -----------------------------------------------------
        # PERSENTASE PIE
        # -----------------------------------------------------

        if approved_total > 0:

            ok_percentage = round(
                (
                    approved_ok_count
                    / approved_total
                ) * 100
            )

            ng_percentage = (
                100 - ok_percentage
            )

        else:

            ok_percentage = 0
            ng_percentage = 0

        # -----------------------------------------------------
        # DATA CARD
        # -----------------------------------------------------

        equipment_dashboard.append({

            "code": code,

            "name": equipment["name"],

            "icon": equipment["icon"],

            "total_item": total_item,

            "finish_check": finish_check,

            "pending_count": pending_count,

            "approved_total": approved_total,

            "approved_ok_count": approved_ok_count,

            "approved_ng_count": approved_ng_count,

            "approved_ok_percentage": ok_percentage,

            "approved_ng_percentage": ng_percentage,

            # -----------------------------------------------
            # ALIAS UNTUK TEMPLATE LAMA
            # -----------------------------------------------

            "result_total": approved_total,

            "ok_count": approved_ok_count,

            "ng_count": approved_ng_count,

            "ok_percentage": ok_percentage,

            "ng_percentage": ng_percentage,

        })

    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        # -----------------------------------------------------
        # ROLE
        # -----------------------------------------------------

        "role": role,

        # -----------------------------------------------------
        # PERIODE
        # -----------------------------------------------------

        "selected_month": selected_month,

        "selected_year": selected_year,

        "selected_month_name":
            selected_month_name,

        "month_names":
            month_names,

        # -----------------------------------------------------
        # KPI
        # -----------------------------------------------------

        "total_equipment":
            total_equipment,

        "total_inspection":
            total_inspection,

        "total_pending":
            total_pending,

        "total_approved":
            total_approved,

        "total_rejected":
            total_rejected,

        "total_ok":
            total_ok,

        "total_ng":
            total_ng,

        # -----------------------------------------------------
        # ALIAS TEMPLATE LAMA
        # -----------------------------------------------------

        "barang_count":
            total_equipment,

        "inspection_count":
            total_inspection,

        "pending_count":
            total_pending,

        "approved_count":
            total_approved,

        "ok_count":
            total_ok,

        "ng_count":
            total_ng,

        # -----------------------------------------------------
        # EQUIPMENT
        # -----------------------------------------------------

        "equipment_dashboard":
            equipment_dashboard,
    }

    # =========================================================
    # RENDER
    # =========================================================

    return render(
        request,
        "admin/dashboard.html",
        context
    )

# =========================================================
# DETAIL DASHBOARD EQUIPMENT
# =========================================================

@login_required
def equipment_dashboard(request, equipment_code):

    role = get_role(request.user)

    if role != "ADMIN":
        return render(
            request,
            "errors/403.html",
            status=403
        )


    # -----------------------------------------------------
    # KATEGORI VALID
    # -----------------------------------------------------

    categories = {

        "TRAFO_GUN": "Trafo & Gun",

        "ELECTRICAL_AIR_HOIST":
            "Electrical & Air Hoist",

        "HANGER": "Hanger",

        "BALANCER": "Balancer",

        "TROLLEY": "Trolley",

        "KBK_REL": "KBK Rel",

    }


    if equipment_code not in categories:

        return render(
            request,
            "errors/404.html",
            status=404
        )


    equipment_name = categories[
        equipment_code
    ]


    # -----------------------------------------------------
    # BULAN
    # -----------------------------------------------------

    today = timezone.localdate()


    try:

        selected_month = int(
            request.GET.get(
                "month",
                today.month
            )
        )

    except (TypeError, ValueError):

        selected_month = today.month


    if selected_month < 1 or selected_month > 12:

        selected_month = today.month


    selected_year = today.year


    month_names = [
        "",
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]


    selected_month_name = month_names[
        selected_month
    ]


    # -----------------------------------------------------
    # EQUIPMENT
    # -----------------------------------------------------

    barang_list = (
        Barang.objects
        .filter(
            jenis_equipment=equipment_code,
            status=True
        )
        .order_by("kode_barang")
    )


    # -----------------------------------------------------
    # LAPORAN
    # -----------------------------------------------------

    reports = (
        LaporanInspeksi.objects
        .select_related(
            "barang",
            "user",
            "approved_by"
        )
        .filter(
            barang__jenis_equipment=equipment_code,
            tanggal_inspeksi__year=selected_year,
            tanggal_inspeksi__month=selected_month
        )
        .order_by("-tanggal_inspeksi")
    )


    # -----------------------------------------------------
    # STATISTIK
    # -----------------------------------------------------

    total_item = barang_list.count()


    finish_check = (
        reports
        .values("barang_id")
        .distinct()
        .count()
    )


    pending_count = reports.filter(
        status_approval="PENDING"
    ).count()


    approved_count = reports.filter(
        status_approval="APPROVED"
    ).count()


    ok_count = reports.filter(
        status_hasil="OK"
    ).count()


    ng_count = reports.filter(
        status_hasil="NG"
    ).count()


    result_total = ok_count + ng_count


    if result_total:

        ok_percentage = round(
            (ok_count / result_total) * 100
        )

    else:

        ok_percentage = 0


    context = {

        "equipment_code": equipment_code,

        "equipment_name": equipment_name,

        "barang_list": barang_list,

        "reports": reports,

        "total_item": total_item,

        "finish_check": finish_check,

        "pending_count": pending_count,

        "approved_count": approved_count,

        "ok_count": ok_count,

        "ng_count": ng_count,

        "result_total": result_total,

        "ok_percentage": ok_percentage,

        "selected_month": selected_month,

        "selected_year": selected_year,

        "selected_month_name": selected_month_name,

        "month_names": month_names,

    }


    return render(
        request,
        "admin/equipment_dashboard.html",
        context
    )


# =========================================================
# KELOLA USER
# =========================================================

@login_required
def kelola_user(request):

    if get_role(request.user) != "ADMIN":

        return render(
            request,
            "errors/403.html",
            status=403
        )


    users = (
        User.objects
        .select_related("profile")
        .order_by("username")
    )


    return render(
        request,
        "admin/users.html",
        {
            "users": users
        }
    )


# =========================================================
# USER FORM
# =========================================================

@login_required
def user_form(request, user_id=None):

    if get_role(request.user) != "ADMIN":

        return render(
            request,
            "errors/403.html",
            status=403
        )


    target = (
        get_object_or_404(
            User,
            pk=user_id
        )
        if user_id
        else None
    )


    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        role = request.POST.get(
            "role",
            "PETUGAS"
        )

        nama = request.POST.get(
            "nama",
            ""
        ).strip()

        jabatan = request.POST.get(
            "jabatan",
            ""
        ).strip()


        if role not in {
            "PETUGAS",
            "ADMIN",
            "SERVER"
        } or not username:

            messages.error(
                request,
                "Username dan role wajib diisi."
            )


        elif not target and not password:

            messages.error(
                request,
                "Password wajib untuk user baru."
            )


        elif (
            User.objects
            .exclude(
                pk=target.pk
                if target
                else None
            )
            .filter(
                username=username
            )
            .exists()
        ):

            messages.error(
                request,
                "Username sudah digunakan."
            )


        else:

            with transaction.atomic():

                target = (
                    target
                    or User(
                        username=username
                    )
                )

                target.username = username


                if password:

                    target.password = make_password(
                        password
                    )


                target.is_staff = (
                    role == "ADMIN"
                )


                target.save()


                profile, _ = (
                    UserProfile.objects
                    .get_or_create(
                        user=target
                    )
                )


                profile.role = role

                profile.nama = nama

                profile.jabatan = jabatan

                profile.save()


            messages.success(
                request,
                "Data user berhasil disimpan."
            )


            return redirect(
                "kelola_user"
            )


    return render(
        request,
        "admin/user_form.html",
        {
            "target": target
        }
    )


# =========================================================
# TOGGLE USER
# =========================================================

@login_required
def toggle_user(request, user_id):

    if (
        get_role(request.user) != "ADMIN"
        or request.method != "POST"
    ):

        return render(
            request,
            "errors/403.html",
            status=403
        )


    target = get_object_or_404(
        User,
        pk=user_id
    )


    if target.pk == request.user.pk:

        messages.warning(
            request,
            "User yang sedang login tidak dapat dinonaktifkan sendiri."
        )

    else:

        target.is_active = not target.is_active

        target.save(
            update_fields=[
                "is_active"
            ]
        )

        messages.success(
            request,
            f"Status {target.username} berhasil diubah."
        )


    return redirect(
        "kelola_user"
    )