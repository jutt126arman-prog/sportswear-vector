import streamlit as st
from rembg import remove
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Flat Texture Extractor", layout="wide")
st.title("🎨 Pro Shirt Texture Extractor (Flat Mode)")

uploaded_file = st.file_uploader("Upload Shirt Mockup (Pic 1)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 1. Image loading
    input_image = Image.open(uploaded_file)
    
    with st.spinner('Extracting Flat Texture...'):
        # 2. Background Remove (Shirt isolate karna)
        no_bg = remove(input_image)
        img_np = np.array(no_bg)

        # 3. Design ko Flat Square banana
        # Hum shirt ke main body area ka coordinates nikal kar usay stretch karenge
        h, w = img_np.shape[:2]
        
        # Points for transformation (Shirt ke center se design pakarna)
        src_pts = np.float32([
            [w*0.2, h*0.2], [w*0.8, h*0.2], 
            [w*0.2, h*0.8], [w*0.8, h*0.8]
        ])
        dst_pts = np.float32([
            [0, 0], [800, 0], 
            [0, 800], [800, 800]
        ])
        
        # Warp Perspective (Design ko flat karna)
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        flat_texture = cv2.warpPerspective(img_np, matrix, (800, 800))

        # 4. Result Display
        col1, col2 = st.columns(2)
        with col1:
            st.image(input_image, caption="Pic 1: Original Mockup", use_container_width=True)
        with col2:
            st.image(flat_texture, caption="Pic 2: Extracted Flat Texture", use_container_width=True)

        # 5. Download Button
        res_img = Image.fromarray(flat_texture)
        buf = io.BytesIO()
        res_img.save(buf, format="PNG")
        
        st.divider()
        st.download_button("📥 Download Flat Texture (High Res)", buf.getvalue(), "flat_design.png", "image/png")

st.info("Tip: Is flat design ko CorelDraw mein 'PowerTrace' karein taake ye vector ban jaye.")
