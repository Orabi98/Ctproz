from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=80, blank=True)
    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    quote = models.TextField()
    def __str__(self):
        return self.client_name

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.email}"
