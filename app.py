import streamlit as st
import cv2
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

st.title("👕 Pro Sportswear Vector Tool")

file = st.file_uploader("Upload Camouflage Design", type=["jpg", "png", "jpeg"])

if file:
    # Image process karna
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Background Removal & Tracing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Vector PDF Banana
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # Design ko "Paths" mein convert karna (Simple Tracing)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        points = cnt.reshape(-1, 2)
        if len(points) > 2:
            path = c.beginPath()
            path.moveTo(points[0][0], letter[1] - points[0][1])
            for x, y in points[1:]:
                path.lineTo(x, letter[1] - y)
            path.close()
            c.drawPath(path, stroke=1, fill=1)
    
    c.save()
    pdf_data = pdf_buffer.getvalue()

    # Display Results
    st.image(thresh, caption="Traced Vector Preview", channels="GRAY")
    
    # Download Buttons
    st.download_button("📥 Download Vector PDF (for Corel/AI)", pdf_data, "design_vector.pdf", "application/pdf")
    st.info("Tip: Is PDF ko CorelDraw ya Illustrator mein khol kar 'Ungroup' karein, ye poora vector ban chuka hoga.")
