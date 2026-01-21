import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("👕 Texture Extractor")

file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    # AI se texture nikalna
    output = remove(img)
    st.image(output, caption="Extracted Texture")
    
    # Download Button
    buf = io.BytesIO()
    output.save(buf, format="PNG")
    st.download_button("Download PNG", buf.getvalue(), "texture.png")
