import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Hello")

def convert_opencv_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

img = cv2.imread('./image/camera_1/20240531_102924.jpg')

st.image(convert_opencv_to_pil(img), caption='Clikc on the image to get pixel value')

