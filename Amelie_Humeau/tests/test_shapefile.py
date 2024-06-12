import fiona # type: ignore
from math import sin, cos, sqrt, atan2, pi, radians
import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import io

def read_shapefile(shapefile_path):
    with fiona.open(shapefile_path, 'r') as shapefile:
        features = []
        for feature in shapefile:
            geometry = dict(feature['geometry'])
            properties = dict(feature['properties'])
            features.append({'geometry': geometry, 'properties': properties})
        return features

def deg2rad(dd):
    return dd * pi / 180

def rad2deg(radians):
    return radians * 180 / pi

def distance(latA, lonA, latB, lonB):
    R = 6373000.0  # rayon de la Terre en mètres

    dlon = lonB - lonA
    dlat = latB - latA

    a = sin(dlat / 2)**2 + cos(latA) * cos(latB) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

def voisins(coordinates_image, coordinates_with_image):
    dict_voisins = {}
    image_base, coordinates_base = coordinates_image
    lat_base = radians(coordinates_base[0])
    lon_base = radians(coordinates_base[1])
    for image, coordinate in coordinates_with_image.items():
        if image_base != image:
            latB = radians(coordinate[0])
            lonB = radians(coordinate[1])        
            
            distance_metres = distance(lat_base, lon_base, latB, lonB)
            if distance_metres < 2:
                dict_voisins[image] = coordinate
    
    return dict_voisins

def create_mosaic(base_img, img, kp_base, des_base, kp, des):
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE)
    matches = matcher.match(des_base, des)

    matches = sorted(matches, key=lambda x: x.distance)
    good_matches = matches[:int(len(matches) * 0.1)]

    src_pts = np.float32([kp_base[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    H, _ = cv2.findHomography(src_pts, dst_pts)

    result = cv2.warpPerspective(base_img, H, (base_img.shape[1] + img.shape[1], base_img.shape[0]+img.shape[0]))

    # Redimensionner l'image à coller en fonction de la hauteur de la mosaïque résultante
    img_resized = cv2.resize(img, (result.shape[1] - base_img.shape[1], int(img.shape[0] * (result.shape[1] - base_img.shape[1]) / img.shape[1])))

    # Vérifier si la hauteur de l'image redimensionnée correspond exactement à la hauteur de la zone de destination
    if img_resized.shape[0] != result.shape[0]:
        img_resized = cv2.resize(img, (result.shape[1] - base_img.shape[1], result.shape[0]))

    result[:, base_img.shape[1]:] = img_resized

    return result, len(matches)


def main():
    shapefile_path = "C:/Users/AHUMEAU/Desktop/transfert/shapefile/geo_images.shp"
    features = read_shapefile(shapefile_path)

    coordinates_with_image = {}
    for feature in features:
        coordinates = feature["geometry"]["coordinates"]
        image = feature["properties"]["image"]
        coordinates_with_image[image] = coordinates

    coordinates_list = list(coordinates_with_image.items())
    coordinates_image_base = list(coordinates_list[0])
    n = 0

    orb = cv2.ORB_create()
    
    while n <= 5:
        dict_voisins = voisins(coordinates_image_base, coordinates_with_image)
        max_matches = (0, "", [], [], [])
        base_img = cv2.imread(coordinates_image_base[0])
        kp_base, des_base = orb.detectAndCompute(base_img, None)
        
        for voisin, coord in dict_voisins.items():
            img = cv2.imread(voisin)
            kp, des = orb.detectAndCompute(img, None)
            mosaic, num_matches = create_mosaic(base_img, img, kp_base, des_base, kp, des)
            
            if num_matches > max_matches[0]:
                max_matches = (num_matches, img, kp, des, voisin)
        print(max_matches[0])
        if max_matches[0] > 100:
            _, img, kp, des, voisin = max_matches
            base_img = mosaic
            coordinates_image_base[1] = coordinates_with_image[voisin]
            del coordinates_with_image[voisin]
            io.imsave(coordinates_image_base[0], base_img)
        
        n += 1

if __name__ == "__main__":
    main()
