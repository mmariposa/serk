import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image

ruta_icono = "icon_16x16.ico"

def obtener_ruta_carpeta():
    return filedialog.askdirectory(title="Selecciona la carpeta de imágenes")

def obtener_ruta_pdf():
    return filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Guardar PDF como...")

def abrir_pdf(nombre_pdf):
    os.startfile(nombre_pdf)

# convertir
def convertir_imagenes_a_pdf(carpeta_imagenes, nombre_pdf, progress_bar):
    try:
        total_imagenes = len([archivo for archivo in os.listdir(carpeta_imagenes) if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
        c = canvas.Canvas(nombre_pdf, pagesize=portrait)
        progress_bar["maximum"] = total_imagenes
        progress = 0
        for archivo in os.listdir(carpeta_imagenes):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                nombre_imagen = os.path.join(carpeta_imagenes, archivo)
                try:
                    imagen = Image.open(nombre_imagen)
                    ancho_imagen, altura_imagen = imagen.size
                    c.setPageSize((ancho_imagen, altura_imagen))
                    c.drawImage(nombre_imagen, 0, 0, width=ancho_imagen, height=altura_imagen)
                    c.showPage()
                    progress += 1
                    progress_bar["value"] = progress
                    progress_bar.update()
                except IOError:
                    messagebox.showerror("PDF serker ♥ - Error", f"No se pudo abrir la imagen: {nombre_imagen}")
        c.save()
        messagebox.showinfo("PDF serker ♥ - Info", f"PDF guardado en: {nombre_pdf}")
        if messagebox.askyesno("PDF serker ♥ - Abrir PDF", "¿Quieres abrir tu nuevo PDF?"):
            abrir_pdf(nombre_pdf)
    except FileNotFoundError:
        messagebox.showerror("PDF serker ♥ - Error", f"No se encontró la carpeta: {carpeta_imagenes}")

# ventana progreso
def convertir():
    carpeta_imagenes = obtener_ruta_carpeta()
    if carpeta_imagenes:
        ruta_pdf = obtener_ruta_pdf()
        if ruta_pdf:
            progress_window = tk.Toplevel(root)
            progress_window.title("PDF serker ♥ - Creando PDF")
            if os.path.exists(ruta_icono):
                progress_window.iconbitmap(ruta_icono)
            progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
            progress_bar.pack(padx=20, pady=20)
            progress_window.geometry("400x100")
            progress_window.transient(root)
            progress_window.grab_set()
            convertir_imagenes_a_pdf(carpeta_imagenes, ruta_pdf, progress_bar)
            progress_window.destroy()

# gui ventana principal
root = tk.Tk()
root.title("PDF serker ♥")
root.geometry("300x85")

# busca si hay icono
if os.path.exists(ruta_icono):
    root.iconbitmap(ruta_icono)

# boton seleccion carpeta
btn_convertir = tk.Button(root, text="Seleccionar carpeta de imágenes", command=convertir)
btn_convertir.pack(pady=20)

root.mainloop()
