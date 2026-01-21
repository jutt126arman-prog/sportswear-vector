import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Auto Vector")
st.title("👕 Sportswear Texture Extractor")

file = st.file_uploader("Upload Camouflage Image", type=["jpg", "png", "jpeg"])

if file:
    img_data = file.getvalue()
    result = remove(img_data)
    st.image(result, caption="Final Texture")
    st.download_button("Download PNG", result, "texture.png")
