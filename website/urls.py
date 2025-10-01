# website/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_view, name='services'),
    path('projects/', views.projects_view, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("projects/", views.projects_view, name="projects"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    # optionally: path("services/", views.services_view, name="services"),
]
