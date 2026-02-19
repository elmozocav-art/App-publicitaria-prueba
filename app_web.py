import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="AI Ad Generator", page_icon="🎨")
st.title("🚀 Generador de Publicidad Para Nacho")

# Tu API Key (Asegúrate de tener saldo)
api_key = "TU_API_KEY_AQUI"
client = OpenAI(api_key="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")

# Interfaz lateral
st.sidebar.header("Configuración")
estilo = st.sidebar.selectbox("Estilo visual", 
    ["Lujo y Elegante", "Minimalista", "Futurista", "Vintage", "Pop Art"])

# Cuerpo principal
producto = st.text_input("¿Qué producto quieres promocionar?", placeholder="Ej: Reloj de pulsera negro")

if st.button("Generar Imagen Publicitaria"):
    if not producto:
        st.error("Por favor, escribe un producto.")
    else:
        try:
            with st.spinner('Diseñando tu publicidad...'):
                # Construimos el prompt según el estilo elegido
                prompt_final = f"Professional advertising photography of {producto}, {estilo} style, cinematic lighting, 8k resolution, high-end product design."
                
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt_final,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                # Obtener la imagen desde la URL que da OpenAI
                url_imagen = response.data[0].url
                img_res = requests.get(url_imagen)
                img = Image.open(BytesIO(img_res.content))

                # Mostrar la imagen
                st.image(img, caption=f"Publicidad para: {producto}", use_container_width=True)
                
                # Botón para descargar
                buf = BytesIO()
                img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(label="Descargar Imagen", data=byte_im, file_name="publicidad.png", mime="image/png")

        except Exception as e:
            st.error(f"Error: {e}")