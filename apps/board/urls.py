from django.urls import path,include
from django.views.generic import RedirectView
from . import views

app_name = "board"

urlpatterns = [
    path("<str:username>/", include([
        path('', RedirectView.as_view(url='projects/')),
        path("addproject/", views.board_addproject, name="addproject"),
        path("contact/", views.board_contact, name="contact"),
        path("docs/", views.board_docs, name="docs"),
        path("mainboard/<str:project_name>/", views.board_mainboard, name="mainboard"),
        path("projects/", views.board_projects, name="projects"),
        path("chart1/<str:project_name>/", views.board_chart1, name="chart1"),
        path("chart2/<str:project_name>/", views.board_chart2, name="chart2"),
        path("chart3/<str:project_name>/", views.board_chart3, name="chart3"),
        path("delete/<str:project_name>/", views.board_delete, name="delete"),
        path("table1/<str:project_name>/", views.board_table1, name="table1"),
        path("table2/<str:project_name>/", views.board_table2, name="table2"),
        path("settings/", views.board_settings, name="settings"),
        path("calendar/", views.board_calendar, name="calendar"),
    ]))
]