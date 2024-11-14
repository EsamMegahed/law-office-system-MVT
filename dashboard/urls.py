from django.urls import path, include
from . import views

app_name = "dashboard"

urlpatterns = [
    # --------- Home page ---------
    path("", views.dashboard_home, name="home_page"),
    # --------- Cases ---------
    # +++ Category Create And Delete +++
    path(
        "cases/category/create",
        views.dashboard_case_category,
        name="dashboard_case_category",
    ),
    path(
        "cases/category/delete/<int:id>",
        views.dashboard_case_category_delete,
        name="dashboard_case_category_delete",
    ),
    # +++ Clients View And Delete +++
    path(
        "cases/clients",
        views.dashboard_clients,
        name="dashboard_clients",
    ),
    path(
        "cases/clients/delete/<int:id>",
        views.dashboard_clients_delete,
        name="dashboard_clients_delete",
    ),
    # +++ Cases Create And Delete +++
    path(
        "cases",
        views.dashboard_cases,
        name="dashboard_cases",
    ),
    path(
        "cases/delete/<int:id>",
        views.dashboard_cases_delete,
        name="dashboard_cases_delete",
    ),

    # +++ Sessions Create And Delete +++
    path(
        "sessions",
        views.dashboard_sessions,
        name="dashboard_sessions",
    ),
    path(
        "sessions/view/<int:id>",
        views.dashboard_sessions_view,
        name="dashboard_sessions_view",
    ),
    path(
        "sessions/delete/<int:id>",
        views.dashboard_sessions_delete,
        name="dashboard_sessions_delete",
    ),

    # +++ Files Create And Delete +++
    path(
        "files",
        views.dashboard_files,
        name="dashboard_files",
    ),
    path(
        "sessions/files/<int:id>",
        views.dashboard_files_view,
        name="dashboard_files_view",
    ),
    path(
        "files/delete/<int:id>",
        views.dashboard_file_delete,
        name="dashboard_file_delete",
    ),

    # +++ Cases Charts +++
    path(
        "cases/charts",
        views.dashboard_cases_charts,
        name="dashboard_cases_charts",
    ),
    # --------- Sales page ---------
    path("sales", views.dashboard_sales, name="dashboard_sales"),
    path(
        "sales/view/<int:id>", views.dashboard_sales_view, name="dashboard_sales_view"
    ),
    path("sales/charts", views.dashboard_sales_charts, name="dashboard_sales_charts"),
    path(
        "sales/delete/<int:id>",
        views.dashboard_payment_delete,
        name="dashboard_payment_delete",
    ),
    # --------- Users pages ---------
    path("user/create", views.dashboard_user_create, name="dashboard_user_create"),
    path("user/list", views.dashboard_user_list, name="dashboard_user_list"),
    path("user/details/<int:id>", views.dashboard_user_details, name="dashboard_user_details"),
    path("user/edit/<int:id>", views.dashboard_user_edit, name="dashboard_user_edit"),
    path("user/delete/<int:id>", views.dashboard_user_delete, name="dashboard_user_delete"),
    path("user/password_change/<int:id>", views.dashboard_user_password_change, name="dashboard_user_password_change"),
    path("user/add_permission/<int:id>", views.dashboard_user_add_permission, name="dashboard_user_add_permission"),
    path("user/remove_permission/<int:id>", views.dashboard_user_remove_permission, name="dashboard_user_remove_permission"),
]
