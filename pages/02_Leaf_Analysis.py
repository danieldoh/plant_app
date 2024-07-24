import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_gsheets import GSheetsConnection

import io
import cv2
import time
import numpy as np
from PIL import Image
from datetime import datetime

from src.utils import two_points_calculation, points_area_calculation, points_venation_analysis

### Page Configurations ###
st.set_page_config(
    page_title="Leaf Analysis",
    page_icon="🍃",
    layout='wide',
)

st.title("🌿 Leaf Analysis")
conn = st.connection("gsheets", type=GSheetsConnection)

### Aerosol Selection ###
aerosol_selection = st.selectbox("Select aerosol condition", ["Aerosol", "No Aerosol"], index = None, placeholder="Select an option")

if aerosol_selection == "Aerosol":
    st.write("Aerosol is selected.")
elif aerosol_selection == "No Aerosol":
    st.write("No Aerosol is selected.")

### Session State ###
if "calculated_values" not in st.session_state:
    st.session_state["calculated_values"] = {
        "width": 0.0,
        "length": 0.0,
        "area": 0.0,
    }

if 'width' not in st.session_state:
    st.session_state['width'] = [[0,0]]

if 'length' not in st.session_state:
    st.session_state['length'] = [[0,0]]

if 'area' not in st.session_state:
    st.session_state['area'] = [[0,0]]

if 'venation' not in st.session_state:
    st.session_state['venation'] = [[0,0]]

### File Upload ###
uploaded_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])
ratio = 0.00023

if uploaded_file is not None:
    ### Image Display ###
    img_pil = Image.open(io.BytesIO(uploaded_file.read()))
    image = np.array(img_pil)

    value = streamlit_image_coordinates(
        image,
        use_column_width="always",
        key="pil",
    )

    ### Value Calculated ###
    st.write("📏 Calculated Values 📏")
    st.write(f"Width: {st.session_state['calculated_values']['width']} m")
    st.write(f"Length: {st.session_state['calculated_values']['length']} m")
    st.write(f"Area: {st.session_state['calculated_values']['area']} m^2")

    ### Mode Selection ###
    mode_selected = st.selectbox("Select the category", ["Width", "Length", "Area", "Venation"], index = None, placeholder="Select an option")

    ### Calculation ###
    if mode_selected == "Width":
        st.session_state['length'] = []
        st.session_state['area'] = []
        st.session_state['venation'] = []

        st.write("🖐️ Click on the image to select the two points for the width.")
        two_points_calculation(value, ratio, 'width', mode_selected, "calculated_values")
    
    elif mode_selected == "Length":
        st.session_state['width'] = []
        st.session_state['area'] = []
        st.session_state['venation'] = []

        st.write("🖐️ Click on the image to select the two points for the length.")
        two_points_calculation(value, ratio, 'length', mode_selected, "calculated_values")

    elif mode_selected == "Area":
        st.session_state['width'] = []
        st.session_state['length'] = []
        st.session_state['venation'] = []

        st.write("🖐️ Click on the image to select the points for the area.")
        # cv2.contoureArea uses shoe-lace formula to calculate the area
        points_area_calculation(value, ratio, 'area', mode_selected, "calculated_values")
    
    elif mode_selected == "Venation":
        st.session_state['width'] = []
        st.session_state['length'] = []
        st.session_state['area'] = []

        st.write("🖐️ Click on the image to select the points for the venation.")
        points_venation_analysis(value, 'venation', mode_selected, "calculated_values", image)
