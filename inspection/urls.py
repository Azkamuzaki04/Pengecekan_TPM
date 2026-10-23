from django.urls import path

from .views import (
    approval,
    approval_action,
    dashboard_user,
    detail,
    history,
    mulai_inspeksi,
)

urlpatterns = [
    # Dashboard User / Inspector
    path(
        "dashboard/",
        dashboard_user,
        name="dashboard_user",
    ),

    # Proses inspeksi
    path(
        "mulai/<int:barang_id>/",
        mulai_inspeksi,
        name="mulai_inspeksi",
    ),

    # History inspeksi
    path(
        "history/",
        history,
        name="inspection_history",
    ),

    # Detail laporan
    path(
        "<int:laporan_id>/",
        detail,
        name="inspection_detail",
    ),

    # Approval Admin
    path(
        "approval/",
        approval,
        name="approval",
    ),

    path(
        "approval/<int:laporan_id>/<str:action>/",
        approval_action,
        name="approval_action",
    ),
]