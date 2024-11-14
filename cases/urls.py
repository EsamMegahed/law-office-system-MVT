from django.urls import path, include
from . import views

app_name = "cases"

urlpatterns = [
    # Home page
    path("", views.home_page, name="home_page"),
    # Client Create And Edit and Details,clients view
    path("cases/clients", views.clients_view, name="clients_view"),
    path("cases/client/create/", views.client_create, name="client_create"),
    path("cases/client/edit/<int:id>", views.client_edit, name="client_edit"),
    path("cases/client/details/<int:id>", views.client_details, name="client_details"),
    # Case Create And Edit and Details
    path("cases/create/<int:id>", views.case_create, name="case_create"),
    path("cases/edit/<int:id>", views.case_edit, name="case_edit"),
    path("cases/text_feilds/<int:id>", views.case_text_field_edit, name="case_text_feilds"),
    path("cases/details/<int:id>", views.case_details, name="case_details"),
    # Case Files Create and Edit
    path("cases/file/create/<int:id>", views.case_file_create, name="case_file_create"),
    path("cases/file/edit/<int:id>", views.case_file_edit, name="case_file_edit"),
    # Case Sessions Create and Edit and Details
    path(
        "cases/sessions/create/<int:id>",
        views.case_sessions_create,
        name="case_sessions_create",
    ),
    path("cases/sessions/edit/<int:id>", views.case_sessions_edit, name="case_sessions_edit"),
    path(
        "cases/sessions/details/<int:id>",
        views.case_sessions_details,
        name="case_sessions_details",
    ),
    path("cases/sessions/list", views.case_sessions_list, name="case_sessions_list"),
    # Case,client Payment Create ,delete
    path("cases/payment/<int:id>", views.case_payment_create, name="case_payment_create"),
    path("client/payment/<int:id>", views.client_paymen_total, name="client_paymen_total"),
    path(
        "cases/payment/delete/<int:id>", views.case_payment_delete, name="case_payment_delete"
    ),

    # Cases Events 
    path("cases/events/create/<int:id>", views.case_event_create, name="case_event_create"),
    path("cases/events/delete/<int:id>", views.case_event_delete, name="case_event_delete"),
    path("cases/events/view", views.case_event_view, name="case_event_view"),


    # Genrate Pdf
    path("cases/events/pdf/", views.events_pdf_view, name="event_pdf"),
    # path("cases/events/pdf2/", views.pdf_generation, name="pdf_generation"),
]


