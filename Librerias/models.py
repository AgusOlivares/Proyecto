from typing import Any, Dict, Tuple
from django.db import models
from django.urls import reverse

# Create your models here.

class Libro(models.Model):
    # Verbose name le muestra al usuario el nombre del campo
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='Titulo')
    imagen = models.ImageField(upload_to='Imagenes/', verbose_name='Imagen', null=True)
    descripcion = models.TextField(verbose_name='Descripcion', null=True)

    def __str__(self):
        fila = "Titulo: " + self.titulo + " - " + "Descripcion: " + self.descripcion
        return fila
    
    def delete(self, using = None, keep_parents = False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

    def get_absolute_url(self):
        return reverse('creacion_qr', args=[str(self.id)])