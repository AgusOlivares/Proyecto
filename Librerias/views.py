import os
import io
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from django.shortcuts import render, redirect
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.drawing.image import Image 
from django.urls import reverse
from django.conf import settings

from .models import Libro # Importo el modelo libro de models para poder acceder a el
from .forms import LibroForm # Importo el modelo de formulario para cargar libro

# Create your views here.

# Cada acceso a paginas Html debe estar confgurado aca abajo

# Acceso a las vistas de las paginas
def inicio(request):
    return render(request, 'paginas/inicio.html')
def nosotros(request):
    return render(request, 'paginas/Nosotros.html')

# Acceso a las funcionalidades CRUD de libros
def libros(request):
    libros = Libro.objects.all()
    # luego de pasar la variable con el nombre y su valor
    # Voy a modificar el lugar donde se muestra: el "index. html"
    return render(request, 'libros/index.html', {'libros': libros}) 
def crear(request):
    formulario = LibroForm(request.POST or None, request.FILES or None) 
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')

    return render(request, 'libros/crear.html', {'formulario': formulario}) # Luego de hacer esto tuve que pasar a crear el path hacia esta url

def editar(request, id):
    libro = Libro.objects.get(id=id) # consulta de id
    formulario = LibroForm(request.POST or None, request.FILES or None, instance=libro) # paso id al formulario para que me muestre los datos
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/editar.html', {'formulario': formulario}) # Nos muestra los datos del formulario

def eliminar(request, id):
    libro = Libro.objects.get(id=id)
    libro.delete()
    return redirect('libros')

def convertir(request): # funcionalidad de exportar los libros a una tabla de excel # tuve que agregar el path a esto dentro del 'urls' de la app 'librerias'
    # Obtener los datos de la base de datos, aquí un ejemplo hipotético
    data = Libro.objects.all()
    
    # Crear un libro de Excel y una hoja de trabajo
    workbook = Workbook()
    sheet = workbook.active
    
    # Escribir los encabezados de las columnas
    sheet.append(['ID', 'Titulo', 'Imagen', 'Descripcion'])
    
    # Escribir los datos de la base de datos en el archivo Excel
    for item in data:
        # Obtener la ruta de la imagen (asumiendo que la imagen se encuentra en el campo 'imagen')
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(item.imagen))
        
        # Añadir los datos de cada fila en la hoja de trabajo
        sheet.append([item.id, item.titulo, ruta_imagen, item.descripcion])
    
    # Insertar las imágenes en el archivo Excel
    for row_num, row_data in enumerate(sheet.iter_rows(min_row=2), start=2):
        # Obtener la ruta de la imagen desde la columna "Imagen" (asumiendo que es la columna 3)
        ruta_imagen = row_data[2].value
        
        # Insertar la imagen en la celda (columna "Imagen")
        if ruta_imagen:
            img = Image(ruta_imagen)
            img.width = 100  # Ajustar el tamaño de la imagen (puedes ajustarlo según tus necesidades)
            img.height = 100
            sheet.column_dimensions['C'].width = 15  # Ajustar el ancho de la columna "Imagen"
            sheet.row_dimensions[row_num].height = 100  # Ajustar la altura de la fila
            sheet.add_image(img, f"C{row_num}")
    
    # Crear la respuesta HTTP con el archivo Excel adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Libros.xlsx'
    
    # Guardar el libro de Excel en la respuesta HTTP
    workbook.save(response)
    
    return response


def ver_pdf(request, libro_id):
    # Obtener el libro seleccionado por su ID
    try:
        libro = Libro.objects.get(pk=libro_id)
    except Libro.DoesNotExist:
        return HttpResponse("Libro no encontrado", status=404)

    # Generar el contenido del PDF
    buffer = io.BytesIO()

    # Crear el documento PDF usando reportlab
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Agregar el contenido del libro al PDF
    story = []
    story.append(Paragraph(f"<b>ID:</b> {libro.id}", styles['Normal']))
    story.append(Paragraph(f"<b>Titulo:</b> {libro.titulo}", styles['Normal']))
    story.append(Spacer(1, 12))  # Espaciado entre párrafos
    story.append(Paragraph(f"<b>Descripcion:</b> {libro.descripcion}", styles['Normal']))
    
    # Puedes agregar más campos según la estructura de tu modelo y la información que deseas incluir en el PDF.

    doc.build(story)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{libro.titulo}.pdf"'
    buffer.close()

    return response



def generar_qr(request, id):
    # Obtener el libro seleccionado por su ID
    try:
        libro = Libro.objects.get(pk=id)
    except Libro.DoesNotExist:
        return HttpResponse("Libro no encontrado", status=404)

    # Generar la URL de descarga del PDF usando la vista 'ver_pdf' y el ID del libro
    url_descarga_pdf = request.build_absolute_uri(reverse('ver_pdf', args=[libro.id]))

    # Generar el código QR con la URL de descarga del PDF
    qr_code = qrcode.make(url_descarga_pdf)

    # Crear una respuesta HTTP para la imagen del código QR
    buffer_qr = io.BytesIO()
    qr_code.save(buffer_qr, format='PNG')
    response_qr = HttpResponse(buffer_qr.getvalue(), content_type='image/png')

    return response_qr


    





