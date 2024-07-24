import io
import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_gsheets import GSheetsConnection

from src.utils import pixel_ratio_calculation

st.set_page_config(
    page_title="Ratio Calculation",
    page_icon="📐",
    layout='wide',
)

st.title("📐 Ratio Calculation")

### session state ###
if "calculated_values" not in st.session_state:
    st.session_state["calculated_values"] = {
        "aerosol_top_ratio": 0.0,
        "no_aerosol_top_ratio": 0.0,
        "aerosol_side_ratio": 0.0,
        "no_aerosol_side_ratio": 0.0,
    }

if 'aerosol_top_ratio' not in st.session_state:
    st.session_state['aerosol_top_ratio'] = [[0,0]]

if 'no_aerosol_top_ratio' not in st.session_state:
    st.session_state['no_aerosol_top_ratio'] = [[0,0]]

if 'aerosol_side_ratio' not in st.session_state:
    st.session_state['aerosol_side_ratio'] = [[0,0]]

if 'no_aerosol_side_ratio' not in st.session_state:
    st.session_state['no_aerosol_side_ratio'] = [[0,0]]

if 'real_length' not in st.session_state:
    st.session_state['real_length'] = 0.0

### File Upload ###
uploaded_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img_pil = Image.open(io.BytesIO(uploaded_file.read()))

    value = streamlit_image_coordinates(
        img_pil,
        use_column_width="always",
        key="pil",
    )

    ### Ratio Calculated ###
    st.write("📏 Calculated Ratio 📏")
    st.write(f"Aerosol Top Ratio: {st.session_state['calculated_values']['aerosol_top_ratio']}")
    st.write(f"No Aerosol Top Ratio: {st.session_state['calculated_values']['no_aerosol_top_ratio']}")
    st.write(f"Aerosol Side Ratio: {st.session_state['calculated_values']['aerosol_side_ratio']}")
    st.write(f"No Aerosol Side Ratio: {st.session_state['calculated_values']['no_aerosol_side_ratio']}")

    ### Mode Selection ###
    mode_selected = st.selectbox("Select the mode", ["Aerosol Top", "No Aerosol Top", "Aerosol Side", "No Aerosol Side"], index = None, placeholder="Select an option") 

    ### Calculation ###
    if mode_selected == "Aerosol Top":
        st.write("Aerosol Top Ratio is selected.")
        st.session_state['real_length'] = st.number_input("Insert measured length (m)", value=None, placeholder="Type a number...")

        st.session_state['no_aerosol_top_ratio'] = []
        st.session_state['aerosol_side_ratio'] = []
        st.session_state['no_aerosol_side_ratio'] = []

        pixel_ratio_calculation(value, 'real_length', "aerosol_top_ratio", mode_selected, "calculated_values")
    
    elif mode_selected == "No Aerosol Top":
        st.write("No Aerosol Top Ratio is selected.")
        st.session_state['real_length'] = st.number_input("Insert measured length (m)", value=None, placeholder="Type a number...")

        st.session_state['aerosol_top_ratio'] = []
        st.session_state['aerosol_side_ratio'] = []
        st.session_state['no_aerosol_side_ratio'] = []

        pixel_ratio_calculation(value, 'real_length', "no_aerosol_top_ratio", mode_selected, "calculated_values")
    
    elif mode_selected == "Aerosol Side":
        st.write("Aerosol Side Ratio is selected.")
        st.session_state['real_length'] = st.number_input("Insert measured length (m)", value=None, placeholder="Type a number...")

        st.session_state['aerosol_top_ratio'] = []
        st.session_state['no_aerosol_top_ratio'] = []
        st.session_state['no_aerosol_side_ratio'] = []

        pixel_ratio_calculation(value, 'real_length', "aerosol_side_ratio", mode_selected, "calculated_values")

    elif mode_selected == "No Aerosol Side":
        st.write("No Aerosol Side Ratio is selected.")
        st.session_state['real_length'] = st.number_input("Insert measured length (m)", value=None, placeholder="Type a number...")

        st.session_state['aerosol_top_ratio'] = []
        st.session_state['no_aerosol_top_ratio'] = []
        st.session_state['aerosol_side_ratio'] = []

        pixel_ratio_calculation(value, 'real_length', "no_aerosol_side_ratio", mode_selected, "calculated_values")

if st.button("Update data"):
    conn = st.connection("gsheets", type=GSheetsConnection)

    ratio_df = conn.read(
        worksheet="ratio",
        ttl="0m",
    )

    new_row = {"date": datetime.now().strftime("%Y/%m/%d_%H:%M:%S")}
    new_row.update(st.session_state["calculated_values"])

    ratio_df = ratio_df.append(new_row, ignore_index=True)

    conn.update(
        worksheet="leaf",
        data=ratio_df
    )

    st.write("Data is updated successfully.")

    st.subheader("Ratio Data")
    st.write(ratio_df)