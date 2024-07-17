# Logiciel de traitement d'images multispectrales

Ce repository contient le code source d'un logiciel de traitement d'images multispectrales. Ce logiciel permet de traiter et d'analyser des images capturées dans différents domaines spectraux, tels que le visible, l'infrarouge, l'ultraviolet, etc.

## Fonctionnalités

- **Traitement d'images multispectrales :** Effectuez des traitements d'images tels que la correction de la distorsion, l'alignement, et le recadrage.

- **Création d'orthomosaïque:** Créez des orthomosaïques à partir des images traitées.

- **Application d'indices:** Appliquez différents indices sur les orthomosaïques.

- **Visualisation d'images:** Visualisez les images du dossier selectionné ou les orthomosaïques créées.
  
## Dépendances

* Python 3.11 et supérieur
* OpenCV
* NumPy
* Pillow
* Matplotlib
* licence Agisoft Metashape Professional

## Installation

1. Clonez le repository à l'aide de la commande `git clone https://github.com/Amel92350/Multispectral.git`
   Pour se déplacer dans le dossier contenant le fichier 'main.py':
   ```batch
   cd Multispectral/Amelie_Humeau/main
   ```
2. Installez les dépendances nécessaires à l'aide de la commande `pip install -r requirements.txt`
3. **Téléchargez Agisoft Metashape Pro :**  Téléchargez Agisoft Metashape Professional depuis [le site officiel de Metashape](https://www.agisoft.com/downloads/installer/).
4. **Télécharger du module Python Metashape :** Téléchargez le module python de Metashape depuis le même site.
5. **Installez le module :** Installez le module python à l'aide de `pip` : 
     ```batch
     pip install Metashape-2.1.2-cp37.cp38.cp39.cp310.cp311-none-win_amd64.whl
     ```
     par exemple en remplaçant le nom du module avec celui que vous avez téléchargé
6. **Pour installer l'exécutable**, modifiez la ligne : binaries=[('C:\\Users\\AHUMEAU\\AppData\\Local\\Programs\\Python\\Python311\\DLLs', '.')] du fichier main.spec en remplaçant le chemin par votre chemin vers python\\DLLs.
   Ensuite exécutez la commande :
   ```batch
   pyinstaller main.spec
   ```
  
## Utilisation
  
**Lancement du logiciel :** Une fois l'environnement configuré, exécutez le logiciel à l'aide de la commande :

   ```bash
   python main.py
   ```
Assurez-vous d'utiliser Python 3.11 ou une version supérieure pour exécuter le logiciel.

**Ou** lancez l'exécutable créé dans dist/main


## Auteurs

* Amel92350
