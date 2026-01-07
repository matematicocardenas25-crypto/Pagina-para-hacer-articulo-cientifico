import streamlit as st
import datetime

# --- LÓGICA DEL GENERADOR APA ---
def formatear_apa_manual(autor, anio, titulo, editorial, url=""):
    """Genera una cita básica en formato APA 7ma Edición"""
    cita = f"{autor} ({anio}). *{titulo}*."
    if editorial:
        cita += f" {editorial}."
    if url:
        cita += f" {url}"
    return cita

# --- NUEVA SECCIÓN EN LA INTERFAZ ---
st.header("📚 Gestor de Bibliografía Automático")
st.info("Organiza tus fuentes siguiendo el rigor académico de la normativa APA.")

with st.expander("Añadir nueva referencia bibliográfica"):
    tipo_fuente = st.selectbox("Tipo de fuente", ["Libro", "Artículo de Revista", "Sitio Web", "Informe Oficial"])
    
    c1, c2 = st.columns(2)
    autor = c1.text_input("Autor(es) (Ej: Saldaña, M. Y.)")
    anio = c2.text_input("Año de publicación", datetime.datetime.now().year)
    titulo_obra = st.text_input("Título de la obra o artículo")
    
    if tipo_fuente == "Libro":
        editorial = st.text_input("Editorial (Ej: Editorial Mc Graw Hill)")
        enlace = ""
    else:
        editorial = st.text_input("Nombre de la Revista o Institución")
        enlace = st.text_input("URL / Enlace (si aplica)")

    if st.button("Añadir a mi bibliografía"):
        nueva_cita = formatear_apa_manual(autor, anio, titulo_obra, editorial, enlace)
        if 'bibliografia_lista' not in st.session_state:
            st.session_state.bibliografia_lista = []
        st.session_state.bibliografia_lista.append(nueva_cita)
        st.success("Referencia añadida.")

# --- VISUALIZACIÓN DE LA BIBLIOGRAFÍA ---
if 'bibliografia_lista' in st.session_state and st.session_state.bibliografia_lista:
    st.subheader("X. BIBLIOGRAFÍA GENERADA")
    # Ordenar alfabéticamente como pide la norma
    lista_ordenada = sorted(st.session_state.bibliografia_lista)
    for cita in lista_ordenada:
        st.markdown(f"- {cita}")
    
    # Opción para copiar todo el bloque
    texto_bibliografia = "\n".join(lista_ordenada)
    st.copy_button("Copiar Bibliografía completa", texto_bibliografia)
