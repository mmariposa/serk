import os
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image
import tkinter as tk
from tkinter import ttk

# ICONO
ruta_icono = "icon_16x16.ico"

def convertir_imagenes_a_pdf():
    try:
        # Obtener la ruta del directorio actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        
        # Carpeta para guardar los PDF
        carpeta_pdf = os.path.join(directorio_actual, "PDFs")
        if not os.path.exists(carpeta_pdf):
            os.makedirs(carpeta_pdf)

        # Obtener todas las carpetas que contienen imágenes en el directorio actual
        carpetas = [nombre for nombre in os.listdir(directorio_actual) if os.path.isdir(os.path.join(directorio_actual, nombre)) and
                    any(archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) 
                        for archivo in os.listdir(os.path.join(directorio_actual, nombre)))]

        # Crear ventana de progreso
        root = tk.Tk()
        root.title("PDF serker ♥")
        if os.path.exists(ruta_icono):
            root.iconbitmap(ruta_icono)
        
        frame_general = ttk.Frame(root, padding="10")
        frame_general.grid(row=0, column=0, sticky="ew")
        label_general = ttk.Label(frame_general, text="Progreso general:")
        label_general.grid(row=0, column=0, sticky="w")
        progress_general = ttk.Progressbar(frame_general, orient="horizontal", length=300, mode="determinate")
        progress_general.grid(row=1, column=0, sticky="ew")

        frame_pdf = ttk.Frame(root, padding="10")
        frame_pdf.grid(row=1, column=0, sticky="ew")
        label_pdf = ttk.Label(frame_pdf, text="")
        label_pdf.grid(row=0, column=0, sticky="w")
        progress_pdf = ttk.Progressbar(frame_pdf, orient="horizontal", length=300, mode="determinate")
        progress_pdf.grid(row=1, column=0, sticky="ew")

        progress_general.configure(maximum=len(carpetas))

        for idx, carpeta in enumerate(carpetas, 1):
            carpeta_completa = os.path.join(directorio_actual, carpeta)
            
            # Obtener el nombre de la carpeta para el PDF
            nombre_pdf = os.path.join(carpeta_pdf, f"{carpeta}.pdf")
            
            # Lista para almacenar nombres de imágenes
            nombres_imagenes = []
            for archivo in os.listdir(carpeta_completa):
                if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    nombres_imagenes.append(os.path.join(carpeta_completa, archivo))

            # Verificar si se encontraron imágenes en la carpeta
            if nombres_imagenes:
                progress_pdf.configure(maximum=len(nombres_imagenes))
                label_pdf.configure(text=f"Procesando: {os.path.basename(nombre_pdf)}")
                c = canvas.Canvas(nombre_pdf, pagesize=portrait)
                for i, nombre_imagen in enumerate(nombres_imagenes, 1):
                    try:
                        imagen = Image.open(nombre_imagen)
                        ancho_imagen, altura_imagen = imagen.size
                        c.setPageSize((ancho_imagen, altura_imagen))
                        c.drawImage(nombre_imagen, 0, 0, width=ancho_imagen, height=altura_imagen)
                        c.showPage()
                        progress_pdf.step()
                        progress_pdf.update()
                    except IOError:
                        print(f"No se pudo abrir la imagen: {nombre_imagen}")

                c.save()
                print(f"PDF generado: {nombre_pdf}")
            else:
                print(f"No se encontraron imágenes en la carpeta '{carpeta}'")
            progress_general.step()
            progress_general.update()
            label_general.configure(text=f"Progreso general: ({idx}/{len(carpetas)})")
        root.destroy()
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar la función principal
convertir_imagenes_a_pdf()
