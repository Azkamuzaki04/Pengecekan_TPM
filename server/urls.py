from django.urls import path

from .views import (
    dashboard,
    health,
    server_status,
    database,
    api_monitor,
    storage,
    users,
    activity_log,
    inspection_monitor,
    reports,
)


urlpatterns = [

    # Dashboard
    path(
        "dashboard/",
        dashboard,
        name="server_dashboard"
    ),

    # System
    path(
        "status/",
        server_status,
        name="server_status"
    ),

    path(
        "database/",
        database,
        name="server_database"
    ),

    path(
        "api-monitor/",
        api_monitor,
        name="server_api_monitor"
    ),

    path(
        "storage/",
        storage,
        name="server_storage"
    ),

    # User
    path(
        "users/",
        users,
        name="server_users"
    ),

    path(
        "activity-log/",
        activity_log,
        name="server_activity"
    ),

    # Inspection
    path(
        "inspection-monitor/",
        inspection_monitor,
        name="server_inspection_monitor"
    ),

    # Reports
    path(
        "reports/",
        reports,
        name="server_reports"
    ),

    # Health API
    path(
        "health/",
        health,
        name="server_health"
    ),
]