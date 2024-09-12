# Librerias y Recursos
from pdf2docx import Converter
import pypandoc
import os
import logging
import streamlit as st
from st_social_media_links import SocialMediaIcons
import tempfile

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

    # Crear un archivo temporal para guardar el archivo subido
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    # Convertir el archivo según su tipo
    if uploaded_file.type == "application/pdf":
        # Convertir PDF a Word
        docx_file = temp_file_path.replace(".pdf", ".docx")
        cv = Converter(temp_file_path)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        st.success(f"Conversión completada. El archivo Word se ha guardado como: {docx_file}")
        st.download_button(label="Descargar archivo Word", data=open(docx_file, "rb"), file_name=docx_file)

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Convertir Word a PDF usando pypandoc
        pdf_file = temp_file_path.replace(".docx", ".pdf")
        try:
            pypandoc.convert_file(temp_file_path, 'pdf', outputfile=pdf_file, extra_args=['--pdf-engine=xelatex'])
            st.success(f"Conversión completada. El archivo PDF se ha guardado como: {pdf_file}")
            st.download_button(label="Descargar archivo PDF", data=open(pdf_file, "rb"), file_name=pdf_file)
        except Exception as e:
            st.error(f"No se pudo completar la conversión a PDF: {e}")

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