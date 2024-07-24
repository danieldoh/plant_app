import streamlit as st
import numpy as np
import math
import time
import csv
import cv2
import matplotlib.pyplot as plt
import colorsys

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from skimage import filters
from skimage.draw import polygon
from collections import Counter
from streamlit_image_coordinates import streamlit_image_coordinates

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

def points_distance_calculation(value, ratio, mode, mode_selected, calculated_values):
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

def points_area_calculation(value, ratio, mode, mode_selected, calculated_values):
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
            pts = np.array(st.session_state[mode][1:], dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            st.session_state[calculated_values][mode] = cv2.contourArea(pts) * (ratio**2)
            st.write(f"{mode_selected}: ", f"{st.session_state[calculated_values][mode]} m^2")
            st.write(f"{mode_selected} calcuation is finished. Please press the RESET button to select new points.")

        if len(st.session_state[mode]) > 1:
            st.write("Number of Pixel Clicked: ", len(st.session_state[mode])-1)
            st.write("Points Selected: ", st.session_state[mode][1:])

def points_surface_area_calculation(value, ratio, mode, mode_selected, calculated_values, attempt):
    reset = st.button("RESET")
    start = st.button("START")
    end = st.button("END")

    message_reset = st.empty()

    if start:
        end == False
        st.write("👉 Started.")
        st.session_state[mode] = []

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
            pix_1 = st.session_state[mode][1]
            pix_2 = st.session_state[mode][2]
            diameter = two_points_distance(pix_1, pix_2) * ratio
            
            temp_height = 0.0
            for i in range(3, len(st.session_state[mode])-1):
                pix_1 = st.session_state[mode][i]
                pix_2 = st.session_state[mode][i+1]
                temp_height += (two_points_distance(pix_1, pix_2) * ratio)
            st.session_state[calculated_values][mode] += math.pi * diameter * temp_height
            st.write(f"{mode_selected}: ", f"{st.session_state[calculated_values][mode]} m^2")
            if st.session_state[attempt] == 1:
                st.write(f"Attempt {st.session_state[attempt]} is finished. Press START button again to continue.")
                st.session_state[attempt] += 1
                st.session_state[mode] = []
            else:
                st.write(f"{mode_selected} calcuation is finished.  press the RESET button to select new points.")

        if len(st.session_state[mode]) > 1:
            st.write("Number of Pixel Clicked: ", len(st.session_state[mode])-1)
            st.write("Points Selected: ", st.session_state[mode][1:])

def points_venation_analysis(value, mode, mode_selected, calculated_values, image):
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
            st.session_state[mode].append((value['x'], value['y']))

        if end:
            st.write("🔚 Ended.")
            mask = np.zeros_like(image)
            pts = np.array(st.session_state[mode][1:], dtype=np.int32)
            pts = pts - 100
            cv2.fillPoly(mask, [pts], (255, 255, 255))
            result = cv2.bitwise_and(image, mask)
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 10, 10)
            #pts = tuple(st.session_state[mode][1:])
            #clone = np.array(image)
            #height, width, _ = clone.shape
            #mask = Image.new('L', (width, height), 0)
            #draw = ImageDraw.Draw(mask)
            #draw.ellipse((140, 50, 260, 170), fill=1)
            #draw.polygon(pts, outline=1, fill=255)

            #masked_img = Image.composite(image, Image.new('RGB', image.size, (0,0,0)), mask)
            #edges = masked_img.convert('L').filter(ImageFilter.FIND_EDGES)
            #enhancer = ImageEnhance.Contrast(edges)
            #img_edges_contrast = enhancer.enhance(2.0)
            #st.image(edges, use_column_width=True)
            venation = streamlit_image_coordinates(
                edges,
                use_column_width="always",
                key="edges",
            )
            st.write(f"{mode_selected} analysis is completed. Please press the RESET button to select new points.")

        if len(st.session_state[mode]) > 1:
            st.write("Number of Pixel Clicked: ", len(st.session_state[mode])-1)
            st.write("Points Selected: ", st.session_state[mode][1:])

def two_points_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distance

def angle_calculation(p1, p2, p3):
    p1_np = np.array(p1)
    p2_np = np.array(p2)
    p3_np = np.array(p3)

    vec1 = p2_np - p1_np
    vec2 = p3_np - p1_np

    dot_product = np.dot(vec1, vec2)
    magnitude_1 = np.linalg.norm(vec1)
    magnitude_2 = np.linalg.norm(vec2)

    cos_theta = dot_product / (magnitude_1 * magnitude_2)

    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)

    return angle_deg

def pixel_ratio_calculation(value, real_length, mode, mode_selected, calculated_values):
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
            pix_distance = two_points_distance(pix_1, pix_2)
            st.session_state[calculated_values][mode] = st.session_state[real_length] / pix_distance
            st.write(f"Aerosol Top Ratio: {st.session_state[calculated_values][mode]}")
            st.write(f"{mode_selected} calculation is finished. Please press the RESET button to select new points.")

        if len(st.session_state[mode]) > 1:
            st.write("Number of Pixel Clicked: ", len(st.session_state[mode])-1)
            st.write("Points Selected: ", st.session_state[mode][1:])
