import glob, os
import Metashape 

def get_folder_band(path:str)->str:
    bande = ""

    if "415nm"  in path:
        bande = "415nm"
    elif "450nm"  in path:
        bande = "450nm"
    elif "570nm" in path:
        bande = "570nm"
    elif "675nm" in path:
        bande = "675nm"
    elif "730nm" in path:
        bande = "730nm"
    else:
        bande = "850nm"
    return bande

def traitement(doc:Metashape.Document,folders_path:str): 

    folder_paths = glob.glob(os.path.join(folders_path,"*"))
    for path in folder_paths:
        bande = get_folder_band(path)
        # Ajouter un chunk
        chunk = doc.addChunk()

        # Charger des photos
        photo_list = glob.glob(os.path.join(path,"*.tif"))
        chunk.addPhotos(photo_list)

        # Aligner les photos
        chunk.matchPhotos(downscale=1,generic_preselection=True,reference_preselection=True)
        chunk.alignCameras()

        # Calibrer les couleurs
        chunk.calibrateColors(white_balance=True,source_data=Metashape.DataSource.TiePointsData)


        # Construire un nuage de points dense
        chunk.buildDepthMaps(downscale=4,filter_mode = Metashape.AggressiveFiltering)


        # Construire un maillage
        chunk.buildModel(source_data=Metashape.DepthMapsData,surface_type = Metashape.Arbitrary,interpolation=Metashape.EnabledInterpolation)

        
        # Créer l'orthomosaïque 
        chunk.buildOrthomosaic(surface_data=Metashape.DataSource.ModelData)


        #Exporter l'orthomosaïque
        if not os.path.exists(os.path.join(folders_path,"orthos")):
            os.makedirs(os.path.join(folders_path,"orthos"))
        output_path=os.path.join(folders_path,"orthos",bande+".tif")
        chunk.exportRaster(output_path,source_data = Metashape.OrthomosaicData)


def main(input_folder):
    # Créer un nouveau projet
    doc = Metashape.Document()
    doc.save('project.psx')
    traitement(doc,input_folder)

if __name__ == "__main__":
    
    main("C:/Users/AHUMEAU/Desktop/transfert/donnees_triees_test")