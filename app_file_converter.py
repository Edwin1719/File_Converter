# Librerias y Recursos
from pypandoc.pandoc_download import download_pandoc
from pdf2docx import Converter
from docx2pdf import convert
import pypandoc
import os
import sys
import logging
import streamlit as st
from st_social_media_links import SocialMediaIcons

# Descargar e instalar Pandoc
download_pandoc()

# Configurar el nivel de registro para suprimir mensajes de información y advertencia
logging.getLogger().setLevel(logging.ERROR)

# Configurar el estilo de la aplicación
st.set_page_config(page_title="CONVERTIDOR DE ARCHIVOS", layout="centered")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2E2E2E;
        color: white;
    }
    .stApp header, .stApp footer, .stApp .stFileUploader label, .stApp .stButton button, .stApp .stTextInput div, .stApp .stTextInput input {
        color: white;
    }
    .stApp h1 {
        color: #1E90FF; /* Azul claro */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Título de la aplicación
st.title("CONVERTIDOR DE ARCHIVOS")

# Subir archivo
uploaded_file = st.file_uploader("Sube un archivo Word o PDF", type=["docx", "pdf"])

if uploaded_file is not None:
    file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)

    # Guardar el archivo subido
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Convertir el archivo según su tipo
    if uploaded_file.type == "application/pdf":
        # Convertir PDF a Word
        docx_file = uploaded_file.name.replace(".pdf", ".docx")
        cv = Converter(uploaded_file.name)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        st.success(f"Conversión completada. El archivo Word se ha guardado como: {docx_file}")
        st.download_button(label="Descargar archivo Word", data=open(docx_file, "rb"), file_name=docx_file)

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Convertir Word a PDF
        pdf_file = uploaded_file.name.replace(".docx", ".pdf")
        pypandoc.convert_file(uploaded_file.name, 'pdf', outputfile=pdf_file, extra_args=['--pdf-engine=xelatex'])
        st.success(f"Conversión completada. El archivo PDF se ha guardado como: {pdf_file}")
        st.download_button(label="Descargar archivo PDF", data=open(pdf_file, "rb"), file_name=pdf_file)
 
# Pie de página con información del desarrollador y logos de redes sociales
st.markdown("""
---
**Desarrollador:** Edwin Quintero Alzate<br>
**Email:** egqa1975@gmail.com<br>
""")

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()