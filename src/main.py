import numpy as np
import argparse
import math
import cv2
import csv

from PIL import Image
from collections import Counter
from colorthief import ColorThief
import matplotlib.pyplot as plt
import colorsys

pix_value = []
selected_corners = []
selected_points = []
selected_contour = []
selected_surfaces = []
selected_width = []
selected_height = []
selected_length = []
selected_angle_pts = []
cropping = False
drawing = False

def select_points(event, x, y, flags, param):
    global selected_contour, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        selected_contour.append([x,y])
        drawing = True
        print("Drawing Started.")
        #print([x,y])
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            selected_contour.append([x,y])
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        print("Drawing Ended.")
        print(f"{len(selected_contour)} pts are selected.")

def select_surface_points(event, x, y, flags, param):
    global selected_surfaces

    if event == 2:
        selected_surfaces.append([x,y])
        print([x,y])

def select_corners(event, x, y, flags, param):
    global selected_corners

    if event == 2:
        selected_corners.append([x,y])
        print([x,y])

def select_four_points(event, x, y, flags, param):
    global selected_points

    if event == 2:
        selected_points.append([x,y])
        print([x,y])

def select_vector_points(event, x, y, flags, param):
    global selected_angle_pts

    if event == 2:
        selected_angle_pts.append([x,y])
        print([x,y])

def select_length_points(event, x, y, flags, param):
    global selected_length

    if event == 2:
        selected_length.append([x,y])
        print([x,y])

def selected_height_points(event, x, y, flags, param):
    global selected_height

    if event == 2:
        selected_height.append([x,y])
        print([x,y])

def selected_width_points(event, x, y, flags, param):
    global selected_width

    if event == 2:
        selected_width.append([x,y])
        print([x,y])

def crop_image(image_folder, image_name, image_category):

    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")
    print("Click the points Top-left, Top-right, Bottom-left, Bottom-right")
    clone = image.copy()

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', select_corners)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    if len(selected_corners) == 4:
        pts = np.array(selected_corners)

        x, y, w, h = cv2.boundingRect(pts)

        cropped_image = clone[y:y+h, x:x+w]


        #leaf_length = math.sqrt((pts[0][0] - pts[2][0])**2 + (pts[0][1] - pts[2][1])**2)
        #leaf_width = math.sqrt((pts[0][0] - pts[1][0])**2 + (pts[0][1] - pts[1][1])**2)

        #leaf_length *= ratio
        #leaf_width *= ratio

        #print(f"Leaf Length is: {leaf_length} m")
        #print(f"Leaf Width is: {leaf_width} m")

        cv2.imshow('cropped image', cropped_image)
        cv2.imwrite(f"../image/{image_folder}/cropped/{image_category}/{image_name}_{image_category}.jpg", cropped_image)
        print("Press Enter key. \n")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return pts, cropped_image
    else:
        print("Please select four points on the image.")

        return np.array(selected_contour), image

def calculate_dimension(pts, ratio):

    area = 0
    pts *= ratio
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        area += pts[i][0] * pts[j][1]
        area -= pts[j][0] * pts[i][1]
    area = abs(area) / 2.0

    return area


def draw_contour(image_folder, image_name, image):

    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', select_points)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    if len(selected_contour):
        pts = np.array(selected_contour, dtype=np.float64)

        cv2.destroyAllWindows()

        return pts
    else:
        print("Draw Contour around the leaf.")

        return np.array(selected_contour)

    cv2.destroyAllWindows()

def trunk_surface(image_folder, image_name, ratio):
    global selected_surfaces

    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")

    surface_area = 0

    for i in range(2):

        print(f"Click two points for diameter and several points for the length of trunk {i+1} \n")
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('image', select_surface_points)

        cv2.imshow('image', image)
        cv2.waitKey(0)

        pts = np.array(selected_surfaces, dtype=np.float64)
        diameter = two_points_distance(pts[0], pts[1])
        diameter *= ratio
        print(f"Diameter: {diameter}")

        total_length = 0
        for i in range(2, len(pts) - 1):
            total_length += two_points_distance(pts[i], pts[i+1])

        total_length *= ratio
        print(f"Length: {total_length}")

        current_surface_area = math.pi * diameter * total_length
        print(math.pi, current_surface_area)
        surface_area += current_surface_area
        selected_surfaces = []

    cv2.destroyAllWindows()

    return surface_area

def plant_angle(image_folder, image_name):

    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', select_vector_points)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    if len(selected_angle_pts) == 3:
        pts = np.array(selected_angle_pts)

        vec1 = pts[1] - pts[0]
        vec2 = pts[2] - pts[0]

        dot_product = np.dot(vec1, vec2)
        magnitude_1 = np.linalg.norm(vec1)
        magnitude_2 = np.linalg.norm(vec2)

        cos_theta = dot_product / (magnitude_1 * magnitude_2)

        angle_rad = np.arccos(cos_theta)
        angle_deg = np.degrees(angle_rad)

        print(f"Angle tilted: {angle_deg} degree \n")
        return angle_deg

def two_points_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    distance = math.sqrt((x2 - x1)**2 + (y2-y1)**2)

    return distance

def plant_length(image_folder, image_name, ratio):

    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', select_length_points)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    total_length = 0
    if len(selected_length):
        pts = np.array(selected_length)

        for i in range(len(pts) - 1):
            total_length += two_points_distance(pts[i], pts[i+1])

        total_length *= ratio
        print(f"Trunk Cumulative Height: {total_length} m \n")
        return total_length

def plant_height(image_folder, image_name, ratio):

    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', selected_height_points)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    if len(selected_height) == 2:
        pts = np.array(selected_height)

        height = two_points_distance(pts[1], pts[0])
        height *= ratio

        print(f"Height: {height} m \n")
        return height

def plant_width(image_folder, image_name, ratio):

    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', selected_width_points)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    if len(selected_width) == 2:
        pts = np.array(selected_width)

        width = two_points_distance(pts[1], pts[0])
        width *= ratio

        print(f"Diameter: {width} m \n")
        return width

def mouse_callback(event, x, y, flags, params):
    if event == 2:
        global pix_value
        pix_value.append([x,y])
        print([x,y])

def calculate_pixel(img, real_length): #, ax):

    global pix_value
    img = cv2.imread(img)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    '''if ax == "y":
        pix_length = pix_value[1][1] - pix_value[0][1]
    elif ax == "x":
        pix_length = pix_value[1][0] - pix_value[0][0]'''
    pix_length = two_points_distance(pix_value[1], pix_value[0])
    print(pix_length)

    ratio = real_length / pix_length
    pix_value = []

    return ratio

def get_leaf(image_folder, image_name, image_category):

    print("Draw the contour around the leaf to get the leaf color.")
    image = cv2.imread(f"../image/{image_folder}/cropped/{image_category}/{image_name}_{image_category}.jpg")
    clone = image.copy()

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', select_points)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    print(len(selected_contour))
    if len(selected_contour):

        mask = np.zeros_like(image)
        cv2.fillPoly(mask, [np.array(selected_contour)], (255, 255, 255))

        #inner_pixels = [image[coord[0], coord[1]] for coord in zip(y,x)]
        result = cv2.bitwise_and(clone, mask)

        nonzero_indices = np.where(mask == 255)

        applied_pixels = [(nonzero_indices[1][i], nonzero_indices[0][i]) for i in range(len(nonzero_indices[0]))]

        gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(blurred, threshold1=10, threshold2=10)
        #for x,y in applied_pixels:
        #    cv2.circle(result, (x, y), radius=5, color=(0, 0, 255), thickness=-1)

        cv2.imshow('Edges', edges)
        cv2.imshow('Leaf Only', result)
        cv2.imwrite(f"../image/{image_folder}/edges/{image_category}/{image_name}_{image_category}.jpg", edges)
        cv2.imwrite(f"../image/{image_folder}/leaf_only/{image_category}/{image_name}_{image_category}.jpg", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return applied_pixels

def check_color(image_folder, image_name, image_category):

    inner_pixels = get_leaf(image_folder, image_name, image_category)
    total_colors = len(inner_pixels)

    ct = Image.open(f"../image/{image_folder}/leaf_only/{image_category}/{image_name}_{image_category}.jpg")
    color_value = [ct.getpixel((x, y)) for x, y in inner_pixels]
    color_average = np.mean(np.array(color_value), axis = 0).astype(int)

    _, counts = np.unique(color_value, axis = 0, return_counts=True)
    _, index = np.unique(color_value, axis = 0, return_index=True)

    frequency_list = list(zip(counts, index))


    frequent_index = [index for _, index in sorted(frequency_list)[::-1]]
    frequent_count = [count for count, _ in sorted(frequency_list)[::-1]]

    frequent_color = [color_value[i] for i in frequent_index[:25]]
    frequent_color = np.array(frequent_color).reshape(5,5,3)

    frequent_pertange = [f"{round((count / total_colors) * 100, 2)} %" for count in frequent_count[:25]]
    frequent_pertange = np.array(frequent_pertange).reshape(5,5)

    date_color = [image_name, color_average]

    for p in frequency_list[:25][::-1]:
        date_color.append(p)

    with open(f"../image/{image_folder}/color/{image_category}/color.csv", 'a', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(date_color)

    print("Average Color: ", color_average)
    plt.figure(figsize=(9,9))
    plt.imshow(frequent_color)

    plt.axis('off')
    plt.grid(True, color='black', linewidth=20)

    for i in range(frequent_pertange.shape[0]):
        for j in range(frequent_pertange.shape[1]):
            color = frequent_color[i, j]
            text = f"{color[0], color[1], color[2]} \n {frequent_pertange[i][j]}"
            plt.text(j, i, text, ha='center', va='center', color='black')

    plt.savefig(f"../image/{image_folder}/color/{image_category}/{image_name}_{image_category}_color.jpg")

    '''ct = ColorThief(f"../image/{image_folder}/leaf_only/{image_category}/{image_name}_{image_category}.jpg")

    quality_num = 7
    palette = ct.get_palette(color_count = quality_num)



    print(date_color)
    plt.imshow([[palette[i] for i in range(quality_num)]])
    plt.show()'''

def get_width_height(image_folder, image_name, ratio):
    print("Click the points for width first, then height.\n")
    image = cv2.imread(f"../image/{image_folder}/{image_name}.jpg")

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', select_four_points)

    cv2.imshow('image', image)
    cv2.waitKey(0)

    if len(selected_points) == 4:
        pts = np.array(selected_points)

        width = two_points_distance(pts[1], pts[0])
        height = two_points_distance(pts[3], pts[2])

        width *= ratio
        height *= ratio

        aspect_ratio = height / width

        print(f"Leaf Width: {width} m \n")
        print(f"Leaf Length: {height} m \n")
        print(f"Leaf Aspect Ratio: {aspect_ratio} \n")

        cv2.destroyAllWindows()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='get input')
    parser.add_argument("--top_image_name", "-ti", help="write top view image name")
    parser.add_argument("--top_image_name_2", "-ti2", help="write top view image name")
    parser.add_argument("--flower_image_name", "-fi", help="write flower image name")
    parser.add_argument("--bean_image_name", "-bi", help="write bean image name")
    parser.add_argument("--camera1_image_name", "-c1", help="write camera1 view image name")
    parser.add_argument("--camera2_image_name", "-c2", help="write camera2 view image name")
    parser.add_argument("--ratio_check", "-r", action="store_true", help="want to check ratio")

    args = parser.parse_args()

    top_ratio_1 = 0.00022721405353294153
    top_ratio_2 = 0.00024388430433987696
    camera1_ratio = 0.0005711954779775399
    camera2_ratio = 0.0005714285714285715

    done1 = "n"
    done2 = "n"
    done3 = "n"
    done4 = "n"

    if args.ratio_check:
        top_image_1 = f"../image/top_camera/{args.top_image_name}"
        top_image_2 = f"../image/top_camera/{args.top_image_name_2}"
        camera1_image = f"../image/camera_1/{args.camera1_image_name}"
        camera2_image = f"../image/camera_2/{args.camera2_image_name}"
        image_list = [top_image_1, top_image_2, camera1_image, camera2_image]
        real_length = [0.02, 0.02, 0.02, 0.02]
        #ax_list = ["y", "x", "y", "y"]

        for image, realLen in zip(image_list, real_length):
            ratio = calculate_pixel(image, realLen)
            print(f"{image} ratio: {ratio} m")

    if args.top_image_name:

        while done1 != "y":

            print("--------------Aerosol (left side) ----------------\n")
            print("Select 4 corners to get width and height. (Right-Click)")
            pts, cropped_image = crop_image("top_camera", args.top_image_name, "aerosol")
            selected_corners = []

            get_width_height("top_camera", args.top_image_name, top_ratio_1)
            selected_points = []

            print("Draw contour to get dimension for leaf.")
            pts = draw_contour("top_camera", args.top_image_name, cropped_image)
            leaf_area = calculate_dimension(pts, top_ratio_1)
            print(f"Leaf Dimension: {leaf_area} m^2 \n")
            selected_contour = []

            check_color("top_camera", args.top_image_name, "aerosol")
            selected_corners = []

            done1 = input("Done? (y/n): ")

    if args.top_image_name_2:

        while done2 != "y":

            print("--------------No Aerosol (right side) ----------------\n")
            print("Select 4 corners to get width and height. (Right-Click)")
            pts, cropped_image = crop_image("top_camera", args.top_image_name_2, "no_aerosol")
            selected_corners = []

            get_width_height("top_camera", args.top_image_name_2, top_ratio_2)
            selected_points = []

            print("Draw contour to get dimension for leaf.")
            pts = draw_contour("top_camera", args.top_image_name_2, cropped_image)
            leaf_area = calculate_dimension(pts, top_ratio_2)
            print(f"Leaf Area: {leaf_area} m^2 \n")
            selected_contour = []

            check_color("top_camera", args.top_image_name_2, "no_aerosol")
            selected_corners = []

            done2 = input("Done? (y/n): ")


    if args.camera1_image_name:

        while done3 != "y":

            print("--------------Camera1 (No Aerosol) ----------------\n")
            print("Click three points for angle of leaf")
            plant_angle("camera_1", args.camera1_image_name)
            selected_angle_pts = []

            print("Click the points around trunk surface for dimension")
            trunk_area = trunk_surface("camera_1", args.camera1_image_name, camera1_ratio)
            #trunk_area = calculate_dimension(pts, camera1_ratio)
            print(f"Trunk Dimension: {trunk_area} m^2")
            selected_contour = []

            print("Click two points for width")
            plant_width("camera_1", args.camera1_image_name, camera1_ratio)
            selected_width = []

            print("Click some points for length")
            plant_length("camera_1", args.camera1_image_name, camera1_ratio)
            selected_length = []

            print("Click bottom and top points for height")
            plant_height("camera_1", args.camera1_image_name, camera1_ratio)
            selected_height = []

            print("Click three points for angle of trunk")
            plant_angle("camera_1", args.camera1_image_name)
            selected_angle_pts = []

            done3 = input("Done? (y/n): ")

    if args.camera2_image_name:

        while done4 != "y":

            print("--------------Camera2 (Aerosol) ----------------\n")
            print("Click three points for angle of leaf")
            plant_angle("camera_2", args.camera2_image_name)
            selected_angle_pts = []

            print("Click the points around trunk surface for dimension")
            trunk_area = trunk_surface("camera_2", args.camera2_image_name, camera1_ratio)
            #trunk_area = calculate_dimension(pts, camera2_ratio)
            print(f"Trunk Dimension: {trunk_area} m^2")
            selected_contour = []

            print("Click two points for width")
            plant_width("camera_2", args.camera2_image_name, camera2_ratio)
            selected_width = []

            print("Click some points for length")
            plant_length("camera_2", args.camera2_image_name, camera2_ratio)
            selected_length = []

            print("Click bottom and top points for height")
            plant_height("camera_2", args.camera2_image_name, camera2_ratio)
            selected_height = []

            print("Click three points for angle of trunk")
            plant_angle("camera_2", args.camera2_image_name)
            selected_angle_pts = []


            done4 = input("Done? (y/n): ")

    '''if args.flower_image_name:
        print("Draw contour to get dimension for flower.")
        pts = draw_contour(args.flower_image_name)
        flower_area = calculate_dimension()
        print(f"Flower Dimension: {flower_area}")
        selected_contour = []

    if args.bean_image_name:
        print("Draw contour to get dimension for flower.")
        pts = draw_contour(args.bean_image_name)
        bean_area = calculate_dimension()
        print(f"bean Dimension: {bean_area}")
        selected_contour = []'''
