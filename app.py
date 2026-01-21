import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="AI Texture Tool")
st.title("👕 AI Texture Extractor")

file = st.file_uploader("Upload Shirt Image", type=["jpg", "png", "jpeg"])

if file:
    with st.spinner('Extracting...'):
        img = Image.open(file)
        # AI Background Removal
        output = remove(img)
        
        st.image(output, caption="Extracted Design")
        
        # Download
        buf = io.BytesIO()
        output.save(buf, format="PNG")
        st.download_button("📥 Download PNG", buf.getvalue(), "design.png", "image/png")
