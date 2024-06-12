import json
import glob
from qgis.core import (
    QgsFields, QgsField, QgsGeometry, QgsPointXY,
    QgsFeature, QgsVectorFileWriter, QgsWkbTypes, QgsCoordinateReferenceSystem,
    QgsProject, QgsVectorLayer
)
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QApplication
import sys

class GeoLocalizationTool:
    def __init__(self):
        pass

    def load_data(self, path_pattern, images_path):
        files = glob.glob(path_pattern)
        images = glob.glob(images_path)
        data = []
        print(files)
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data.append(json.load(f))
                print(f"Success loading file: {file}")
            except Exception as e:
                print(f"Error reading data from {file}: {str(e)}")

        return data, images

    def process_data(self, data_list, images):
        coordinates = []

        for data in data_list:
            gps_data = data.get('gps')
            if gps_data:
                latitude_str = gps_data.get('latitude')
                longitude_str = gps_data.get('longitude')

                if latitude_str and longitude_str:
                    latitude = self.dms_to_decimal(latitude_str)
                    longitude = self.dms_to_decimal(longitude_str)
                    coordinates.append({'latitude': latitude, 'longitude': longitude})

        self.create_shapefile(coordinates, images)

    def dms_to_decimal(self, dms):
        parts = dms.split('°')
        degrees = float(parts[0])
        parts = parts[1].split("'")
        minutes = float(parts[0])
        parts = parts[1].split(' ')
        seconds = float(parts[0])
        hemisphere = parts[1].strip()  # N, S, E, W

        decimal = degrees + minutes / 60 + seconds / 3600

        if hemisphere in ['S', 'W']:
            decimal = -decimal  # Inverser la coordonnée pour le sud ou l'ouest

        return decimal

    def create_shapefile(self, coordinates, images):
        if not coordinates:
            print("Error: No coordinates found.")
            return

        fields = QgsFields()
        fields.append(QgsField("image", QVariant.String))
        fields.append(QgsField("num", QVariant.String))

        crs = QgsCoordinateReferenceSystem(4326)  # WGS84
        writer = QgsVectorFileWriter(
            'C:/Users/AHUMEAU/Desktop/donnees_triees/geo_images.shp',
            'UTF-8',
            fields,
            QgsWkbTypes.Point,
            crs,
            'ESRI Shapefile'
        )

        if writer.hasError() != QgsVectorFileWriter.NoError:
            print(f"Error creating shapefile: {writer.errorMessage()}")
            return

        i = 0
        for coordinate,image in zip(coordinates,images):
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(coordinate['longitude'], coordinate['latitude'])))
            feature.setAttributes([image,f'{i}'])
            writer.addFeature(feature)
            i+=1

        del writer
        print("Shapefile created successfully.")

        # Load the shapefile into QGIS project
        layer = QgsVectorLayer('C:/Users/AHUMEAU/Desktop/shapefile/geo_images2.shp', "GeoImages", "ogr")
        if not layer.isValid():
            print("Error: Layer failed to load!")
        QgsProject.instance().addMapLayer(layer)

def main():
    print("Script started.")
    app = QApplication(sys.argv)

    geo_tool = GeoLocalizationTool()
    images_path = "C:/Users/AHUMEAU/Desktop/donnees_triees/570nm/*.tif"
    path_pattern = "C:/Users/AHUMEAU/Desktop/Stage/20220519_Prasville/20220518/*/*.json"
    data_list, images = geo_tool.load_data(path_pattern, images_path)
    if data_list:
        print("Data loaded successfully.")
        geo_tool.process_data(data_list, images)
        print("Data processed successfully.")
    else:
        print("Error loading data.")
        print(data_list)

    print("Script finished.")

if __name__ == "__main__":
    main()