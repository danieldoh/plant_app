import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import io
import time
import numpy as np
from PIL import Image
from src.utils import two_points_distance, angle_calculation
from datetime import datetime

st.set_page_config(
    page_title="Trunk Analysis",
    page_icon="🌱",
    layout='wide',
)

st.title("Trunk Analysis")

aerosol_selection = st.selectbox("Select aerosol condition", ["Aerosol", "No Aerosol"], index = None, placeholder="Select an option")

if aerosol_selection == "Aerosol":
    st.write("Aerosol is selected.")
elif aerosol_selection == "No Aerosol":
    st.write("No Aerosol is selected.")

# session state
if 'aerosol_selection' not in st.session_state:
    st.session_state['aerosol_selection'] = aerosol_selection

if "calculated_values" not in st.session_state:
    st.session_state["calculated_values"] = {
        "width": 0.0,
        "cum_height": 0.0,
        "height": 0.0,
        "angle": 0.0,
        "leaf_angle": 0.0
    }

if 'width' not in st.session_state:
    st.session_state['width'] = [[0,0]]

if 'height' not in st.session_state:
    st.session_state['height'] = [[0,0]]

if 'cum_height' not in st.session_state:
    st.session_state['cum_height'] = [[0,0]]

if 'angle' not in st.session_state:
    st.session_state['angle'] = [[0,0]]

if 'leaf_angle' not in st.session_state:
    st.session_state['leaf_angle'] = [[0,0]]


def two_points_calculation(value, ratio, mode, mode_selected, calculated_values):
    reset = st.button("RESET")
    message_reset = st.empty()

    if reset:
        st.session_state[mode] = []
        st.session_state[calculated_values][mode] = 0.0
        message_reset.write("Resetting")

        time.sleep(2)

        message_reset.empty()
        reset = False

    if value and not reset:
        if len(st.session_state[mode]) < 3:
            st.session_state[mode].append([value['x'], value['y']])

        if len(st.session_state[mode]) == 3:
            pix_1 = st.session_state[mode][-2]
            pix_2 = st.session_state[mode][-1]
            st.session_state[calculated_values][mode] = two_points_distance(pix_1, pix_2) * ratio
            st.write(f"{mode_selected}: ", f"{st.session_state[calculated_values][mode]} m")
            st.write(f"{mode_selected} calculation is finished. Please press the RESET button to select new points.")

        if len(st.session_state[mode]) > 1:
            st.write("Number of Pixel Clicked: ", len(st.session_state[mode])-1)
            st.write("Points Selected: ", st.session_state[mode][1:])

def three_points_angle_calculation(value, mode, mode_selected, calculated_values):
    reset = st.button("RESET")
    message_reset = st.empty()

    if reset:
        st.session_state[mode] = []
        st.session_state[calculated_values][mode] = 0.0
        message_reset.write("Resetting")

        time.sleep(2)

        message_reset.empty()
        reset = False

    if value and not reset:
        if len(st.session_state[mode]) < 4:
            st.session_state[mode].append([value['x'], value['y']])

        if len(st.session_state[mode]) == 4:
            pix_1 = st.session_state[mode][-3]
            pix_2 = st.session_state[mode][-2]
            pix_3 = st.session_state[mode][-1]
            st.session_state[calculated_values][mode] = angle_calculation(pix_1, pix_2, pix_3) 
            st.write(f"{mode_selected}: ", f"{st.session_state[calculated_values][mode]} degrees")
            st.write(f"{mode_selected} calculation is finished. Please press the RESET button to select new points.")

        if len(st.session_state[mode]) > 1:
            st.write("Number of Pixel Clicked: ", len(st.session_state[mode])-1)
            st.write("Points Selected: ", st.session_state[mode][1:])

def points_calculation(value, ratio, mode, mode_selected, calculated_values):
    reset = st.button("RESET")
    start = st.button("START")
    end = st.button("END")

    message_reset = st.empty()

    if start:
        st.session_state[mode] = []
        st.session_state[calculated_values][mode] = 0.0
        st.write("👉 Started.")

    if reset:
        st.session_state[mode] = []
        st.session_state[calculated_values][mode] = 0.0
        message_reset.write("Resetting")

        time.sleep(2)

        message_reset.empty()
        reset = False
        start = False
        end = False

    if value and not reset:
        if not end:
            st.session_state[mode].append([value['x'], value['y']])

        if end:
            st.write("🔚 Ended.")
            for i in range(1, len(st.session_state[mode])-1):
                pix_1 = st.session_state[mode][i]
                pix_2 = st.session_state[mode][i+1]
                st.session_state[calculated_values][mode] += two_points_distance(pix_1, pix_2)
            st.session_state[calculated_values][mode] *= ratio
            st.write(f"{mode_selected}: ", f"{st.session_state[calculated_values][mode]} m")
            st.write(f"{mode_selected} calcuation is finished. Please press the RESET button to select new points.")

        if len(st.session_state[mode]) > 1:
            st.write("Number of Pixel Clicked: ", len(st.session_state[mode])-1)
            st.write("Points Selected: ", st.session_state[mode][1:])

# Image path
uploadted_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])
ratio = 0.00057

if uploadted_file is not None:
    img_pil = Image.open(io.BytesIO(uploadted_file.read()))

    value = streamlit_image_coordinates(
        img_pil,
        use_column_width="always",
        key="pil",
    )

    st.write(f"Width: {st.session_state['calculated_values']['width']} m")
    st.write(f"Cumulative Height: {st.session_state['calculated_values']['cum_height']} m")
    st.write(f"Height: {st.session_state['calculated_values']['height']} m")
    st.write(f"Tilt Angle: {st.session_state['calculated_values']['angle']} degrees")
    st.write(f"Leaf Tilt Angle: {st.session_state['calculated_values']['leaf_angle']} degrees")

    mode_selected = st.selectbox("Select the category", ["Width", "Cumulative Height", "Height", "Tilt Angle", "Leaf Tilt Angle"], index = None, placeholder="Select an option")


    if mode_selected == "Width":
        st.session_state['angle'] = []
        st.session_state['height'] = []
        st.session_state['cum_height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select the two points for the trunk.")

        # value = streamlit_image_coordinates
        # mode = 'width'
        # mode_selected = 'Width'
        two_points_calculation(value, ratio, 'width', mode_selected, 'calculated_values')

    elif mode_selected == "Cumulative Height":
        st.session_state['angle'] = []
        st.session_state['width'] = []
        st.session_state['height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select the side of the trunk for the cumulative height.")
        st.write("🖐️ Press START button and click the points. When you finish, press END button")

        # value = streamlit_image_coordinates
        # mode = 'cum_height'
        # mode_selected = 'Cumulative Height'

        points_calculation(value, ratio, 'cum_height', mode_selected, 'calculated_values')
        

    elif mode_selected == "Height":
        st.session_state['angle'] = []
        st.session_state['width'] = []
        st.session_state['cum_height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select one bottom point and one top point for the height.")

        # value = streamlit_image_coordinates
        # mode = 'height'
        # mode_selected = 'Height'
        two_points_calculation(value, ratio, 'height', 'Height', 'calculated_values') 


    elif mode_selected == "Tilt Angle":
        st.session_state['width'] = []
        st.session_state['cum_height'] = []
        st.session_state['height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select three points for the angle.")
        st.write("🖐️ Click Order: BOTTOM - STRAIGHT TOP - TILTED TOP")

        # value = streamlit_image_coordinates
        # mode = 'angle'
        # mode_selected = 'Tilt Angle'
        three_points_angle_calculation(value, 'angle', 'Tilt Angle', 'calculated_values')
    
    elif mode_selected == "Leaf Tilt Angle":
        st.session_state['width'] = []
        st.session_state['cum_height'] = []
        st.session_state['height'] = []
        st.session_state['angle'] = []

        st.write("🖐️ Click on the image to select three points for the leaf angle.")
        st.write("🖐️ Click Order: LEAF BOTTOM - LEAF BOTTOM - TRUNK")

        # value = streamlit_image_coordinates
        # mode = 'leaf_angle'
        # mode_selected = 'Leaf Tilt Angle'
        three_points_angle_calculation(value, 'leaf_angle', 'Leaf Tilt Angle', 'calculated_values')