# website/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services_view, name="services"),
    path("projects/", views.projects_view, name="projects"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("about/", views.about, name="about"),

    # Keep the name 'contact' so templates won't crash
    path("contact/", RedirectView.as_view(url="/", permanent=False), name="contact"),
]
