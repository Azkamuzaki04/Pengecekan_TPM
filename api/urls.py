from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    BarangByBarcodeAPI,
    InspectionCreateAPI,
    InspectionHistoryAPI,
)


urlpatterns = [

    path(
        "auth/token/",
        obtain_auth_token,
        name="api_token",
    ),

    path(
        "barang/<str:barcode>/",
        BarangByBarcodeAPI.as_view(),
        name="api_barang_barcode",
    ),

    path(
        "inspections/",
        InspectionCreateAPI.as_view(),
        name="api_inspection_create",
    ),

    path(
        "inspections/history/",
        InspectionHistoryAPI.as_view(),
        name="api_inspection_history",
    ),
]