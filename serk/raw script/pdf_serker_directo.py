import os
import sys
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image

def convertir_imagenes_a_pdf():
    try:
        # Obtener la ruta de la carpeta donde se encuentra el script
        carpeta_script = os.path.dirname(os.path.abspath(__file__))

        # Buscar la primera imagen en la carpeta del script
        nombre_primer_imagen = None
        for archivo in os.listdir(carpeta_script):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                nombre_primer_imagen = archivo
                break

        # Si se encontró una imagen, proceder a crear el PDF
        if nombre_primer_imagen:
            nombre_pdf = os.path.join(carpeta_script, f"{os.path.splitext(nombre_primer_imagen)[0]}.pdf")
            c = canvas.Canvas(nombre_pdf, pagesize=portrait)
            for archivo in os.listdir(carpeta_script):
                if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    nombre_imagen = os.path.join(carpeta_script, archivo)
                    try:
                        imagen = Image.open(nombre_imagen)
                        ancho_imagen, altura_imagen = imagen.size
                        c.setPageSize((ancho_imagen, altura_imagen))
                        c.drawImage(nombre_imagen, 0, 0, width=ancho_imagen, height=altura_imagen)
                        c.showPage()
                    except IOError:
                        print(f"No se pudo abrir la imagen: {nombre_imagen}")

            c.save()
            print(f"PDF generado: {nombre_pdf}")
        else:
            print("No se encontraron imágenes en la carpeta del script.")
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar la función principal
convertir_imagenes_a_pdf()
