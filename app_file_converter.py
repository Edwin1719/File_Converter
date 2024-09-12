# Librerias y Recursos
from pdf2docx import Converter
import cloudconvert
import os
import logging
import streamlit as st
from st_social_media_links import SocialMediaIcons
import tempfile

# Configurar el nivel de registro para suprimir mensajes de información y advertencia
logging.getLogger().setLevel(logging.ERROR)

# Configura tu API Key de CloudConvert
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNGZmNzcyYWYwY2Q2YTFiYzdkNzM2MjdhOTVlOTU2YzhmOWM2YzM2ZGM4Nzc3NzdkZmE1M2ZlM2U3MTg4ZTQ0ZTNkMTMzZWU5ZDRjMzRmNjAiLCJpYXQiOjE3MjYxMDI4NDMuMDY5NTMsIm5iZiI6MTcyNjEwMjg0My4wNjk1MzIsImV4cCI6NDg4MTc3NjQ0My4wNjU4MjMsInN1YiI6IjY5NTYyMTYyIiwic2NvcGVzIjpbInRhc2sucmVhZCIsInRhc2sud3JpdGUiXX0.EtRNdks5U48z4XwvBhYN3SQxgmrxg4hxrufZL2PWArMI-f6fcllBj2wyuDya3Pe6SjOYMi775UAJVMm7PEEbEvJh2YLRMZuv_UlS5f27e1SLbfq4gKPDn3woI0K6YFzIJDFIMMM8xXwsasRme94lRwlELLoha0KgzejUYUdotXDqpJyE2VBw770dnzjsfiIfe62Wo1sgXRt4p87HSqf2ISJj3bQOVs7-UneLg4-8_CQMWGrwTGX3JVmtUnjRCxQszoB-cIKsEnTPEELxyFDdfnqae4jJjn-sD38LQO-GwW3Ue1rXzU0jtZH2vHtjJ4u8SjU9qRXW7TFZyjMFt4qju1YeykBdMDWc3hdHtXdUhEuF0DKPSEfYI8fk0Bs3tGRHRiGGtrgECN0ZYnlZkcP4u-R0w5HkGPbWWwVrmZRULYs63LBWzEuP-11oKFOzm45Z-AakVkZ7zP_CO0kPM1Z54IFeu_Io_its8lDEQNQALYdqeZ7yRtmkUo6xiQB6bd8cJ8WN4llhUtL0K3jP_eiZCIDBvHKPdNcqESD7NXOnbvBoNM9AUgAEVOOSQahyTjxGlktSDQUa4oqaFtxN6Itv4H0du307Su6Aa1uJpV9NIxazDGJBwB61tI_xmh6SDjKXSWFBW0EjdhjLLNeaRgWub1X5wlECXSHwvh-wwPhQAik"  # Reemplaza esto con tu clave

cloudconvert.configure(api_key=API_KEY)

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
        # Convertir Word a PDF usando CloudConvert API
        try:
            # Crear el trabajo de conversión en CloudConvert
            job = cloudconvert.Job.create(payload={
                'tasks': {
                    'import-my-file': {
                        'operation': 'import/upload'
                    },
                    'convert-my-file': {
                        'operation': 'convert',
                        'input': 'import-my-file',
                        'output_format': 'pdf',
                        'input_format': 'docx'
                    },
                    'export-my-file': {
                        'operation': 'export/url',
                        'input': 'convert-my-file'
                    }
                }
            })

            # Subir el archivo DOCX a CloudConvert
            upload_task_id = job['tasks'][0]['id']
            with open(temp_file_path, 'rb') as docx_file:
                cloudconvert.Task.upload(upload_task_id, file=docx_file)

            # Esperar a que el trabajo se complete
            job = cloudconvert.Job.wait(id=job['id'])

            # Descargar el archivo PDF convertido
            export_task = next(task for task in job['tasks'] if task['name'] == 'export-my-file')
            file_url = export_task['result']['files'][0]['url']

            st.success("Conversión completada. Descarga el archivo PDF:")
            st.download_button(label="Descargar archivo PDF", data=file_url, file_name="archivo_convertido.pdf")

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
