import os
import cv2
import numpy as np

aerosol_leaf_only_path = '/Users/hdoh/HJ/Research/prof_byeon/plant_kindey_2/image/top_camera/leaf_only/aerosol/'
no_aerosol_leaf_only_path = '/Users/hdoh/HJ/Research/prof_byeon/plant_kindey_2/image/top_camera/leaf_only/no_aerosol/'
aerosol_edge_path = "/Users/hdoh/HJ/Research/prof_byeon/plant_kindey_2/image/top_camera/edges/aerosol/"
no_aerosol_edge_path = '/Users/hdoh/HJ/Research/prof_byeon/plant_kindey_2/image/top_camera/edges/no_aerosol/'

aerosol_leaf_only_list = os.listdir(aerosol_leaf_only_path)
no_aerosol_leaf_only_list = os.listdir(no_aerosol_leaf_only_path)
aerosol_edge_list = os.listdir(aerosol_edge_path)
no_aerosol_edge_list = os.listdir(no_aerosol_edge_path)

path_list = [aerosol_leaf_only_path, aerosol_edge_path, no_aerosol_leaf_only_path, no_aerosol_edge_path]
entire_list = [aerosol_leaf_only_list, aerosol_edge_list, no_aerosol_leaf_only_list, no_aerosol_edge_list]

for i in entire_list:
    if ".DS_Store" in i:
        i.remove(".DS_Store")

    print(i)

for i in range(0,4,2):

    path_leaf = path_list[i]
    path_edge = path_list[i+1]

    images_leaf = entire_list[i]
    images_edge = entire_list[i+1]

    for image_leaf, image_edge in zip(images_leaf, images_edge):

        il_path = path_leaf + image_leaf
        ie_path = path_edge + image_edge

        il = cv2.imread(il_path, cv2.IMREAD_GRAYSCALE)
        ie = cv2.imread(ie_path, cv2.IMREAD_GRAYSCALE)

        threshold_value = 1

        _, binary_il = cv2.threshold(il, threshold_value, 255, cv2.THRESH_BINARY)
        _, binary_ie = cv2.threshold(ie, threshold_value, 255, cv2.THRESH_BINARY)

        total_pixels_il = binary_il.size
        total_pixels_ie = binary_ie.size
        print(total_pixels_ie)

        black_pixels_il = np.sum(binary_il == 0)
        print(black_pixels_il)

        white_pixels_ie = np.sum(binary_ie == 255)
        black_pixels_ie = np.sum(binary_ie == 0)

        leaf_area_pixel = total_pixels_ie - black_pixels_il

        proportion_white = white_pixels_ie / leaf_area_pixel

        print(f"Proportion of white pixels {ie_path}: {proportion_white:.4f}")
        print(f"White percentage: {proportion_white * 100:.4f}\n")

