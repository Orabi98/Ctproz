from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services_view, name="services"),
    path("projects/", views.projects_view, name="projects"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("about/", views.about, name="about"),

    # Contact removed: redirect old /contact/ traffic to home (prevents form spam)
    path("contact/", RedirectView.as_view(url="/", permanent=False)),
]
