from django.urls import path

from .views import (
    login_view,
    logout_view,
    dashboard,
    kelola_user,
    user_form,
    toggle_user,
)


urlpatterns = [

    # ==============================
    # AUTH
    # ==============================

    path(
        "login/",
        login_view,
        name="login",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),


    # ==============================
    # DASHBOARD ADMIN
    # ==============================

    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),


    # ==============================
    # USER MANAGEMENT
    # ==============================

    path(
        "users/",
        kelola_user,
        name="kelola_user",
    ),

    path(
        "users/tambah/",
        user_form,
        name="user_tambah",
    ),

    path(
        "users/<int:user_id>/edit/",
        user_form,
        name="user_edit",
    ),

    path(
        "users/<int:user_id>/toggle/",
        toggle_user,
        name="toggle_user",
    ),
]