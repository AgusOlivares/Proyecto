from django.urls import path
from . import views

from django.conf import settings # se importa el archivo de configuraciones para acceder a la url_rrot
from django.contrib.staticfiles.urls import static # contrib es para acceder a la ruta estatica de mis imagenes


# Este archivo fue creado no por el sistema ni no por mi para poder
# registrar los path de cada direccion que se ingrese en la url de la pagina

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='Nosotros'),
    path('libros', views.libros, name='libros'),
    path('libros/crear', views.crear, name='crear'), # el 'libros/crear es porque esto se modifica en la parte de la url'
    path('libros/editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'), # agrego el /<int:id> ya que va a recibir el valor de eliminar y un entero que va a ser el id
    path('libros/editar/<int:id>', views.editar, name='editar'), # le envio 3 parametros, las direcciones y el id
    path('convertir', views.convertir, name='convertir'), # funcion agregada por mi, conversion de la tabla a archivo excel
    path('ver_pdf/<int:id>/', views.ver_pdf, name="ver_pdf"), ## PUEDE GENERAR EL QR, PERO AL ESTAR EN UN SERVIDOR LOCAL NO SE PUEDE DESCARGAR EL ARCHIVO DESDE LOS CELULARES
    path('generar_qr/<int:id>/', views.generar_qr, name = 'generar_qr') # funcion 2 agregada por mi, generacion de qr para descarga de datos en pdf


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # hago esto para poder concatenar las rutas de acceso a las imagenes junto a las vistas