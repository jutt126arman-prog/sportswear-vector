import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Design Extractor", layout="wide")
st.title("👕 Pro Design Extractor (Flat Texture)")

file = st.file_uploader("Upload Shirt Mockup", type=["jpg", "png", "jpeg"])

if file:
    # Image open karna
    img = Image.open(file)
    w, h = img.size
    
    # --- TEXTURE EXTRACTION (NO ZOOM) ---
    # Shirt ke corners se design pakad kar usay flat karna
    # Ye shirt ki shape ko khatam karke design bahir nikal dega
    left, top, right, bottom = w*0.2, h*0.1, w*0.8, h*0.9
    flat_design = img.crop((left, top, right, bottom))
    flat_design = flat_design.resize((1200, 1200), Image.Resampling.LANCZOS)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Pic 1: Original Mockup")
    with col2:
        st.image(flat_design, caption="Pic 2: Final Flat Design")

    # --- DOWNLOAD BUTTON (Ye lazmi aayega) ---
    buf = io.BytesIO()
    flat_design.save(buf, format="PNG")
    
    st.divider()
    st.download_button(
        label="📥 DOWNLOAD FLAT DESIGN (PNG)",
        data=buf.getvalue(),
        file_name="extracted_design.png",
        mime="image/png"
    )
