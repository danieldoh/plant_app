import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_gsheets import GSheetsConnection

import io
import numpy as np
from PIL import Image
from datetime import datetime

from src.utils import two_points_calculation, three_points_angle_calculation, points_distance_calculation, points_surface_area_calculation

### Page Configurations ###
st.set_page_config(
    page_title="Trunk Analysis",
    page_icon="🌱",
    layout='wide',
)

st.title("🌳 Trunk Analysis")



### session state ###
if 'aerosol_selection' not in st.session_state:
    st.session_state['aerosol_selection'] = ""

if "calculated_values" not in st.session_state:
    st.session_state["calculated_values"] = {
        "diameter": 0.0,
        "cumulative_height": 0.0,
        "height": 0.0,
        "surface_area": 0.0,
        "tilt_angle": 0.0,
        "leaf_angle": 0.0
    }

if 'diameter' not in st.session_state:
    st.session_state['diameter'] = [[0,0]]

if 'height' not in st.session_state:
    st.session_state['height'] = [[0,0]]

if 'cumulative_height' not in st.session_state:
    st.session_state['cumulative_height'] = [[0,0]]

if 'tilt_angle' not in st.session_state:
    st.session_state['tilt_angle'] = [[0,0]]

if 'leaf_angle' not in st.session_state:
    st.session_state['leaf_angle'] = [[0,0]]

if 'surface_area' not in st.session_state:
    st.session_state['surface_area'] = [[0,0]]

if 'attempt' not in st.session_state:
    st.session_state['attempt'] = 1

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

    value = streamlit_image_coordinates(
        img_pil,
        use_column_width="always",
        key="pil",
    )

    ### Value Calculated ###
    st.write("📏 Calculated Values 📏")
    st.write(f"Diamter: {st.session_state['calculated_values']['diameter']} m")
    st.write(f"Cumulative Height: {st.session_state['calculated_values']['cumulative_height']} m")
    st.write(f"Height: {st.session_state['calculated_values']['height']} m")
    st.write(f"Surface Area: {st.session_state['calculated_values']['surface_area']} m^2")
    st.write(f"Tilt Angle: {st.session_state['calculated_values']['tilt_angle']} degrees")
    st.write(f"Leaf Tilt Angle: {st.session_state['calculated_values']['leaf_angle']} degrees")

    ### Mode Selection ###
    mode_selected = st.selectbox("Select the category", ["Diameter", "Cumulative Height", "Height", "Surface Area", "Tilt Angle", "Leaf Tilt Angle"], index = None, placeholder="Select an option")

    ### Calculation ###
    if mode_selected == "Diameter":
        st.session_state['height'] = []
        st.session_state['cumulative_height'] = []
        st.session_state['surface_area'] = []
        st.session_state['tilt_angle'] = []
        st.session_state['leaf_angle'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select the two points for the trunk.")

        # value = streamlit_image_coordinates
        # mode = 'width'
        # mode_selected = 'Width'
        two_points_calculation(value, ratio, 'diameter', mode_selected, 'calculated_values')

    elif mode_selected == "Cumulative Height":
        st.session_state['diameter'] = []
        st.session_state['height'] = []
        st.session_state['surface_area'] = []
        st.session_state['tilt_angle'] = []
        st.session_state['leaf_angle'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select the side of the trunk for the cumulative height.")
        st.write("🖐️ Press START button and click the points. When you finish, press END button")

        # value = streamlit_image_coordinates
        # mode = 'cum_height'
        # mode_selected = 'Cumulative Height'
        points_distance_calculation(value, ratio, 'cumulative_height', mode_selected, 'calculated_values')
        

    elif mode_selected == "Height":
        st.session_state['diameter'] = []
        st.session_state['cumulative_height'] = []
        st.session_state['leaf_angle'] = []
        st.session_state['surface_area'] = []
        st.session_state['tilt_angle'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select one bottom point and one top point for the height.")

        # value = streamlit_image_coordinates
        # mode = 'height'
        # mode_selected = 'Height'
        two_points_calculation(value, ratio, 'height', 'Height', 'calculated_values') 
    
    elif mode_selected == "Surface Area":
        st.session_state['diameter'] = []
        st.session_state['cum_height'] = []
        st.session_state['height'] = []
        st.session_state['tilt_angle'] = []
        st.session_state['leaf_angle'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select the side of the trunk for the surface area.")

        # value = streamlit_image_coordinates
        # mode = 'surface_area'
        # mode_selected = 'Surface Area'
        points_surface_area_calculation(value, ratio, 'surface_area', 'Surface Area', 'calculated_values', 'attempt')

    elif mode_selected == "Tilt Angle":
        st.session_state['diameter'] = []
        st.session_state['cumulative_height'] = []
        st.session_state['height'] = []
        st.session_state['surface_area'] = []
        st.session_state['leaf_angle'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select three points for the angle.")
        st.write("🖐️ Click Order: BOTTOM - STRAIGHT TOP - TILTED TOP")

        # value = streamlit_image_coordinates
        # mode = 'angle'
        # mode_selected = 'Tilt Angle'
        three_points_angle_calculation(value, 'tilt_angle', 'Tilt Angle', 'calculated_values')
    
    elif mode_selected == "Leaf Tilt Angle":
        st.session_state['diameter'] = []
        st.session_state['cumulative_height'] = []
        st.session_state['height'] = []
        st.session_state['surface_area'] = []
        st.session_state['tilt_angle'] = []
        ratio = st.session_state['ratio']

        st.write("🖐️ Click on the image to select three points for the leaf angle.")
        st.write("🖐️ Click Order: LEAF BOTTOM - LEAF TOP - TRUNK")

        # value = streamlit_image_coordinates
        # mode = 'leaf_angle'
        # mode_selected = 'Leaf Tilt Angle'
        three_points_angle_calculation(value, 'leaf_angle', 'Leaf Tilt Angle', 'calculated_values')
    
st.write("Click button when you finish all the calculations.")
if st.button("Update Data"):
    conn = st.connection("gsheets", type=GSheetsConnection)
    trunk_df = conn.read(
        worksheet="trunk",
        ttl="0m",
    )
    new_row = {
        "date": datetime.now().strftime("%Y/%m/%d_%H:%M:%S"),
        "aerosol_condition": st.session_state['aerosol_selection'],
    }

    new_row.update(st.session_state["calculated_values"])

    trunk_df = trunk_df.append(new_row, ignore_index=True)

    conn.update(
        worksheet="trunk",
        data=trunk_df
    )

    st.write("Data is updated successfully.")
    st.write(trunk_df)