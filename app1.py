import streamlit as st
import numpy as np
import pandas as pd
from docx import Document
from docx.shared import Pt
from PIL import Image
import io
import easyocr
import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Redactor Científico Prof. Cárdenas", layout="wide")

# --- FUNCIONES DE APOYO ---
def generar_word_articulo(datos, bibliografia):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(12)
    
    doc.add_heading(datos['titulo'], 0)
    
    secciones = [
        ("RESUMEN", datos['resumen']),
        ("INTRODUCCIÓN", "La presente investigación se fundamenta en la necesidad de generar conocimiento académico..."),
        ("METODOLOGÍA", datos['metodologia']),
        ("RESULTADOS Y DISCUSIÓN", datos['cuerpo']),
        ("CONCLUSIONES", "Se concluye que los objetivos planteados fueron alcanzados mediante el análisis estadístico...")
    ]
    
    for titulo, contenido in secciones:
        doc.add_heading(titulo, level=1)
        doc.add_paragraph(contenido)
    
    if bibliografia:
        doc.add_heading("REFERENCIAS BIBLIOGRÁFICAS (APA)", level=1)
        for cita in sorted(bibliografia):
            doc.add_paragraph(cita, style='List Bullet')
            
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def generar_latex_articulo(datos, bibliografia):
    bib_items = "\n".join([f"\\item {c}" for c in sorted(bibliografia)])
    latex = f"""\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\title{{{datos['titulo']}}}
\\author{{Prof. Ismael Cárdenas}}
\\begin{{document}}
\\maketitle
\\begin{{abstract}}
{datos['resumen']}
\\end{{abstract}}
\\section{{Introducción}}
Texto introductorio generado automáticamente...
\\section{{Metodología}}
{datos['metodologia']}
\\section{{Resultados y Discusión}}
{datos['cuerpo']}
\\section{{Referencias Bibliográficas}}
\\begin{{itemize}}
{bib_items}
\\end{{itemize}}
\\end{{document}}"""
    return latex

# --- INTERFAZ ---
st.title("📝 Redactor de Artículos Científicos con OCR")
st.markdown("---")

# 1. ESCÁNER DE IMAGEN (OCR)
st.subheader("📷 Extracción de Información desde Imagen")
archivo_img = st.file_uploader("Sube una foto del artículo o apuntes", type=['jpg','png','jpeg'])
texto_extraido = ""

if archivo_img:
    with st.spinner("Leyendo imagen..."):
        reader = easyocr.Reader(['es'])
        img = Image.open(archivo_img)
        texto_extraido = "\n".join(reader.readtext(np.array(img), detail=0))
    st.success("Texto extraído con éxito. Puedes copiarlo o usarlo abajo.")
    st.text_area("Texto detectado:", value=texto_extraido, height=150)

# 2. FORMULARIO DEL ARTÍCULO
st.markdown("---")
with st.form("art_form"):
    c1, c2 = st.columns(2)
    titulo = c1.text_input("Título del Artículo", "Estudio sobre Estadística Aplicada")
    metodo = c2.selectbox("Metodología", ["Cuantitativa", "Cualitativa", "Mixta"])
    
    resumen = st.text_area("Resumen (Abstract)", height=100)
    cuerpo = st.text_area("Cuerpo del Artículo / Resultados", 
                          value=texto_extraido, 
                          help="Aquí puedes pegar el texto extraído de la imagen", 
                          height=250)
    
    submit = st.form_submit_button("💾 Guardar Borrador")

# 3. GESTOR APA
st.markdown("---")
st.subheader("📚 Bibliografía APA")
if 'bib_list' not in st.session_state: st.session_state.bib_list = []

with st.expander("Agregar Referencia"):
    ac1, ac2 = st.columns(2)
    autor = ac1.text_input("Autor")
    anio = ac2.text_input("Año")
    tit_obra = st.text_input("Título del Libro/Artículo")
    if st.button("Añadir Cita"):
        st.session_state.bib_list.append(f"{autor} ({anio}). {tit_obra}.")
        st.rerun()

for c in st.session_state.bib_list:
    st.write(f"• {c}")

# 4. DESCARGAS
if submit:
    datos_finales = {
        "titulo": titulo, "resumen": resumen, 
        "metodologia": metodo, "cuerpo": cuerpo
    }
    
    st.markdown("### 📥 Descargar Documentos Finales")
    col_w, col_l = st.columns(2)
    
    file_word = generar_word_articulo(datos_finales, st.session_state.bib_list)
    col_w.download_button("Descargar Word (.docx)", file_word, f"{titulo}.docx")
    
    file_latex = generar_latex_articulo(datos_finales, st.session_state.bib_list)
    col_l.download_button("Descargar LaTeX (.tex)", file_latex.encode(), f"{titulo}.tex")
