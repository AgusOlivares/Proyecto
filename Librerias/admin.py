from django.contrib import admin
from .models import Libro

# Register your models here.

admin.site.register(Libro) ## Luego de esto corri un comando que crea un superusuario con python manage.py createsuperuser