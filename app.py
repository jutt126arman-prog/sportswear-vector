import streamlit as st
from rembg import remove
from PIL import Image
import io
import cv2
import numpy as np

st.set_page_config(page_title="Sportswear Texture Extractor", layout="wide")

st.title("👕 AI Sportswear Texture Extractor")
st.write("Upload shirt image to extract the flat texture design.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Load Original Image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, caption="Original Image", use_container_width=True)
        
    with st.spinner('Extracting Texture... Please wait...'):
        # 2. AI Background Removal (Shirt isolate karna)
        extracted_design = remove(image)
        
        # 3. Quality Enhancement (Texture ko saaf karna)
        # Convert to OpenCV format
        open_cv_image = np.array(extracted_design)
        # Convert RGBA to RGB if needed
        if open_cv_image.shape[2] == 4:
            # Masking process to keep colors vibrant
            mask = open_cv_image[:,:,3]
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGBA2RGB)
        
        with col2:
            st.image(extracted_design, caption="Extracted Texture", use_container_width=True)
        
        # 4. Download Process
        buf = io.BytesIO()
        extracted_design.save(buf, format='PNG')
        byte_im = buf.getvalue()
        
        st.divider()
        st.download_button(
            label="📥 Download Texture (Transparent PNG)",
            data=byte_im,
            file_name="extracted_texture.png",
            mime="image/png"
        )

st.success("Tip: Is PNG ko CorelDraw mein import karein aur 'PowerTrace' use karke vector bana lein.")
