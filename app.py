import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Texture Fix", layout="wide")
st.title("👕 Flat Design Extractor")

file = st.file_uploader("Upload Mockup", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    w, h = img.size
    
    # Simple Crop and Stretch (Design nikalne ke liye)
    # Is se shirt ki shape khatam ho jati hai
    left, top, right, bottom = w*0.2, h*0.15, w*0.8, h*0.85
    flat_design = img.crop((left, top, right, bottom))
    flat_design = flat_design.resize((1200, 1200), Image.LANCZOS)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Original")
    with col2:
        st.image(flat_design, caption="Extracted Flat Design")

    # --- DOWNLOAD BUTTON ---
    buf = io.BytesIO()
    flat_design.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.divider()
    st.download_button(
        label="📥 DOWNLOAD PNG NOW",
        data=byte_im,
        file_name="flat_design.png",
        mime="image/png"
    )
