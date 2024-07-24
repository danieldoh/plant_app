import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_gsheets import GSheetsConnection

import io
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

### Session State ###
if 'aerosol_selection' not in st.session_state:
    st.session_state['aerosol_selection'] = ""

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

if 'ratio' not in st.session_state:
    st.session_state['ratio'] = 0.0

### Aerosol Selection ###
aerosol_selection = st.selectbox("Select aerosol condition", ["Aerosol", "No Aerosol"], index = None, placeholder="Select an option")

if aerosol_selection == "Aerosol":
    st.session_state['aerosol_selection'] = aerosol_selection
    st.write("Aerosol is selected.")
else:
    st.session_state['aerosol_selection'] = aerosol_selection
    st.write("No Aerosol is selected.")
### ratio ### 
conn = st.connection("gsheets", type=GSheetsConnection)

ratio_df = conn.read(
    worksheet="ratio",
    ttl="10m",
)

st.write(ratio_df)
st.write("Write the pix-to-m ratio of the image. (Check ratio table)")
st.session_state["ratio"] = st.number_input("Insert the ratio", value=None, placeholder="Type a number...")
st.write(st.session_state["ratio"])

### File Upload ###
uploaded_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])

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
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select the two points for the width.")
        two_points_calculation(value, ratio, 'width', mode_selected, "calculated_values")
    
    elif mode_selected == "Length":
        st.session_state['width'] = []
        st.session_state['area'] = []
        st.session_state['venation'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select the two points for the length.")
        two_points_calculation(value, ratio, 'length', mode_selected, "calculated_values")

    elif mode_selected == "Area":
        st.session_state['width'] = []
        st.session_state['length'] = []
        st.session_state['venation'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select the points for the area.")
        # cv2.contoureArea uses shoe-lace formula to calculate the area
        points_area_calculation(value, ratio, 'area', mode_selected, "calculated_values")
    
    elif mode_selected == "Venation":
        st.session_state['width'] = []
        st.session_state['length'] = []
        st.session_state['area'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select the points for the venation.")
        points_venation_analysis(value, 'venation', mode_selected, "calculated_values", image)

st.write("Click button when you finish all the calculations.")
if st.button("Update Data"):
    conn = st.connection("gsheets", type=GSheetsConnection)

    leaf_df = conn.read(
        worksheet="leaf",
        ttl="0m",
    )

    new_row = {
        "date": datetime.now().strftime("%Y/%m/%d_%H:%M:%S"),
        "aerosol_condition": st.session_state['aerosol_selection'],
    }

    new_row.update(st.session_state["calculated_values"])

    leaf_df = leaf_df.append(new_row, ignore_index=True)

    conn.update(
        worksheet="leaf",
        data=leaf_df
    )

    st.write("Data is updated successfully.")
    st.write(leaf_df)
