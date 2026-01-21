import streamlit as st
from rembg import remove
from PIL import Image
import io

# Page setup
st.set_page_config(page_title="Sportswear Tool", layout="centered")
st.title("👕 Sportswear Texture Extractor")

# File uploader
uploaded_file = st.file_uploader("Upload Camouflage Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 1. Show Original
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)
    
    # 2. Process
    with st.spinner('Extracting texture... Please wait.'):
        img_bytes = uploaded_file.getvalue()
        result_bytes = remove(img_bytes)
        result_img = Image.open(io.BytesIO(result_bytes))
        
        # 3. Show Result
        st.image(result_img, caption="Final Texture (No Background)", use_container_width=True)
        
        # 4. Download
        st.download_button("📥 Download Texture PNG", result_bytes, "texture.png", "image/png")
else:
    st.info("Please upload an image to start.")
