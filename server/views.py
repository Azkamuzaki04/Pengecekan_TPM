from functools import wraps
from datetime import datetime, timedelta
import os
import shutil

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.views import get_role
from barang.models import Barang
from inspection.models import LaporanInspeksi


User = get_user_model()


# =========================================================
# SERVER ROLE
# =========================================================

def server_required(view):

    @wraps(view)
    @login_required
    def wrapped(request, *args, **kwargs):

        if get_role(request.user) != "SERVER":
            return render(
                request,
                "errors/403.html",
                status=403
            )

        return view(request, *args, **kwargs)

    return wrapped


# =========================================================
# DATABASE CHECK
# =========================================================

def check_database():

    try:

        with connection.cursor() as cursor:

            cursor.execute("SELECT 1")
            cursor.fetchone()

        return True

    except Exception:

        return False


# =========================================================
# SERVER DASHBOARD
# =========================================================

@server_required
def dashboard(request):

    db_status = check_database()

    media_ok = os.path.exists(settings.MEDIA_ROOT)

    inspection_qs = LaporanInspeksi.objects.all()

    pending_count = inspection_qs.filter(
        status_approval="PENDING"
    ).count()

    approved_count = inspection_qs.filter(
        status_approval="APPROVED"
    ).count()

    rejected_count = inspection_qs.filter(
        status_approval="REJECTED"
    ).count()

    latest = (
        inspection_qs
        .select_related("barang", "user")
        .order_by("-tanggal_inspeksi")[:8]
    )

    context = {

        "db_status": "ONLINE" if db_status else "OFFLINE",

        "media_ok": media_ok,

        "barang_count": Barang.objects.count(),

        "inspection_count": inspection_qs.count(),

        "pending_count": pending_count,

        "approved_count": approved_count,

        "rejected_count": rejected_count,

        "admin_count": User.objects.filter(
            profile__role="ADMIN"
        ).count(),

        "petugas_count": User.objects.filter(
            profile__role="PETUGAS"
        ).count(),

        "latest": latest,
    }

    return render(
        request,
        "server/dashboard.html",
        context
    )


# =========================================================
# SERVER STATUS
# =========================================================

@server_required
def server_status(request):

    db_online = check_database()

    context = {

        "db_online": db_online,

        "django_version": __import__(
            "django"
        ).get_version(),

        "python_version": (
            f"{__import__('sys').version_info.major}."
            f"{__import__('sys').version_info.minor}."
            f"{__import__('sys').version_info.micro}"
        ),

        "server_time": timezone.localtime(),

        "media_root": str(settings.MEDIA_ROOT),

    }

    return render(
        request,
        "server/server_status.html",
        context
    )


# =========================================================
# DATABASE MONITOR
# =========================================================

@server_required
def database(request):

    db_online = check_database()

    context = {

        "db_online": db_online,

        "engine": settings.DATABASES["default"]["ENGINE"],

        "name": settings.DATABASES["default"]["NAME"],

        "host": settings.DATABASES["default"]["HOST"],

        "port": settings.DATABASES["default"]["PORT"],

        "barang_count": Barang.objects.count()
        if db_online else 0,

        "inspection_count": (
            LaporanInspeksi.objects.count()
            if db_online else 0
        ),

        "user_count": (
            User.objects.count()
            if db_online else 0
        ),

    }

    return render(
        request,
        "server/database.html",
        context
    )


# =========================================================
# API MONITOR
# =========================================================

@server_required
def api_monitor(request):

    endpoints = [

        {
            "method": "POST",
            "path": "/api/auth/token/",
            "description": "Login API",
        },

        {
            "method": "GET",
            "path": "/api/barang/{barcode}/",
            "description": "Data barang berdasarkan barcode",
        },

        {
            "method": "POST",
            "path": "/api/inspections/",
            "description": "Submit hasil inspeksi",
        },

        {
            "method": "GET",
            "path": "/api/inspections/history/",
            "description": "History inspeksi",
        },

    ]

    return render(
        request,
        "server/api_monitor.html",
        {
            "endpoints": endpoints,
        }
    )


# =========================================================
# STORAGE
# =========================================================

@server_required
def storage(request):

    media_path = settings.MEDIA_ROOT

    if os.path.exists(media_path):

        total, used, free = shutil.disk_usage(
            media_path
        )

        total_gb = round(
            total / (1024 ** 3),
            2
        )

        used_gb = round(
            used / (1024 ** 3),
            2
        )

        free_gb = round(
            free / (1024 ** 3),
            2
        )

        usage_percent = round(
            (used / total) * 100,
            1
        )

    else:

        total_gb = 0
        used_gb = 0
        free_gb = 0
        usage_percent = 0

    return render(
        request,
        "server/storage.html",
        {
            "media_path": media_path,
            "total_gb": total_gb,
            "used_gb": used_gb,
            "free_gb": free_gb,
            "usage_percent": usage_percent,
        }
    )


# =========================================================
# USERS
# =========================================================

@server_required
def users(request):

    users = (
        User.objects
        .select_related("profile")
        .order_by("username")
    )

    return render(
        request,
        "server/users.html",
        {
            "users": users,
        }
    )


# =========================================================
# ACTIVITY LOG
# =========================================================

@server_required
def activity_log(request):

    logs = (
        LogEntry.objects
        .select_related("user", "content_type")
        .order_by("-action_time")[:50]
    )

    return render(
        request,
        "server/activity_log.html",
        {
            "logs": logs,
        }
    )


# =========================================================
# INSPECTION MONITOR
# =========================================================

@server_required
def inspection_monitor(request):

    qs = LaporanInspeksi.objects.all()

    context = {

        "total": qs.count(),

        "ok": qs.filter(
            status_hasil="OK"
        ).count(),

        "ng": qs.filter(
            status_hasil="NG"
        ).count(),

        "pending": qs.filter(
            status_approval="PENDING"
        ).count(),

        "latest": (
            qs
            .select_related("barang", "user")
            .order_by("-tanggal_inspeksi")[:20]
        ),

    }

    return render(
        request,
        "server/inspection_monitor.html",
        context
    )


# =========================================================
# APPROVAL MONITOR
# =========================================================

@server_required
def approval_monitor(request):

    qs = LaporanInspeksi.objects.all()

    context = {

        "pending": qs.filter(
            status_approval="PENDING"
        ).count(),

        "approved": qs.filter(
            status_approval="APPROVED"
        ).count(),

        "rejected": qs.filter(
            status_approval="REJECTED"
        ).count(),

        "latest": (
            qs
            .select_related("barang", "user")
            .order_by("-tanggal_inspeksi")[:20]
        ),

    }

    return render(
        request,
        "server/approval_monitor.html",
        context
    )


# =========================================================
# REPORTS
# =========================================================

# =========================================================
# REPORTS
# =========================================================

@server_required
def reports(request):

    # -----------------------------------------------------
    # DEBUG
    # -----------------------------------------------------
    print("\n================ REPORTS DEBUG ================")
    print("REQUEST GET:", request.GET)

    # -----------------------------------------------------
    # SEMUA DATA
    # -----------------------------------------------------
    qs = (
        LaporanInspeksi.objects
        .select_related("barang", "user")
        .order_by("-tanggal_inspeksi")
    )

    print("TOTAL AWAL:", qs.count())

    # -----------------------------------------------------
    # AMBIL FILTER
    # -----------------------------------------------------
    tanggal_mulai = request.GET.get(
        "tanggal_mulai",
        ""
    ).strip()

    tanggal_selesai = request.GET.get(
        "tanggal_selesai",
        ""
    ).strip()

    status_hasil = request.GET.get(
        "status_hasil",
        ""
    ).strip()

    status_approval = request.GET.get(
        "status_approval",
        ""
    ).strip()

    print("tanggal_mulai   :", repr(tanggal_mulai))
    print("tanggal_selesai :", repr(tanggal_selesai))
    print("status_hasil    :", repr(status_hasil))
    print("status_approval  :", repr(status_approval))

    # -----------------------------------------------------
    # FILTER TANGGAL MULAI
    # -----------------------------------------------------
    if tanggal_mulai:

        try:
            start_date = datetime.strptime(
                tanggal_mulai,
                "%Y-%m-%d"
            )

            start_datetime = start_date.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=timezone.utc
            )

            qs = qs.filter(
                tanggal_inspeksi__gte=start_datetime
            )

            print(
                "SETELAH TANGGAL MULAI:",
                qs.count()
            )

        except ValueError:
            print(
                "ERROR FORMAT TANGGAL MULAI:",
                tanggal_mulai
            )

    # -----------------------------------------------------
    # FILTER TANGGAL SELESAI
    # -----------------------------------------------------
    if tanggal_selesai:

        try:
            end_date = datetime.strptime(
                tanggal_selesai,
                "%Y-%m-%d"
            )

            # Tambah 1 hari agar seluruh tanggal selesai
            # ikut masuk.
            end_datetime = (
                end_date + timedelta(days=1)
            ).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=timezone.utc
            )

            qs = qs.filter(
                tanggal_inspeksi__lt=end_datetime
            )

            print(
                "SETELAH TANGGAL SELESAI:",
                qs.count()
            )

        except ValueError:
            print(
                "ERROR FORMAT TANGGAL SELESAI:",
                tanggal_selesai
            )

    # -----------------------------------------------------
    # FILTER STATUS HASIL
    # -----------------------------------------------------
    if status_hasil and status_hasil != "ALL":

        qs = qs.filter(
            status_hasil=status_hasil
        )

        print(
            "SETELAH STATUS HASIL:",
            qs.count()
        )

    # -----------------------------------------------------
    # FILTER STATUS APPROVAL
    # -----------------------------------------------------
    if status_approval and status_approval != "ALL":

        qs = qs.filter(
            status_approval=status_approval
        )

        print(
            "SETELAH STATUS APPROVAL:",
            qs.count()
        )

    # -----------------------------------------------------
    # DATA AKHIR
    # -----------------------------------------------------
    print("TOTAL AKHIR:", qs.count())

    for laporan in qs[:20]:
        print(
            "DATA:",
            laporan.id,
            laporan.tanggal_inspeksi,
            laporan.status_hasil,
            laporan.status_approval
        )

    print("================================================\n")

    # -----------------------------------------------------
    # STATISTIK
    # -----------------------------------------------------
    context = {

        "reports": qs,

        "total": qs.count(),

        "ok": qs.filter(
            status_hasil="OK"
        ).count(),

        "ng": qs.filter(
            status_hasil="NG"
        ).count(),

        "pending": qs.filter(
            status_approval="PENDING"
        ).count(),

        "approved": qs.filter(
            status_approval="APPROVED"
        ).count(),

        "rejected": qs.filter(
            status_approval="REJECTED"
        ).count(),

        "tanggal_mulai": tanggal_mulai,

        "tanggal_selesai": tanggal_selesai,

        "status_hasil": status_hasil,

        "status_approval": status_approval,
    }

    return render(
        request,
        "server/reports.html",
        context
    )

# =========================================================
# HEALTH
# =========================================================

@server_required
def health(request):

    try:

        with connection.cursor() as cursor:

            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JsonResponse({
            "status": "ok",
            "database": "online"
        })

    except Exception as exc:

        return JsonResponse(
            {
                "status": "error",
                "database": "offline",
                "detail": str(exc)
            },
            status=503
        )