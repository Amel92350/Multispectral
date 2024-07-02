# Logiciel de traitement d'images multispectrales

Ce repository contient le code source d'un logiciel de traitement d'images multispectrales. Ce logiciel permet de traiter et d'analyser des images capturées dans différents domaines spectraux, tels que le visible, l'infrarouge, l'ultraviolet, etc.

## Fonctionnalités

- **Traitement d'images multispectrales :** Effectuez des traitements d'images tels que la correction de la distorsion, l'alignement, et le recadrage.

- **Création de panoramas:** Créez des panoramas à partir des images traitées.

- **Application d'indices:** Appliquez différents indices sur les panoramas.
  
## Dépendances

* Python 3.11 et supérieur
* OpenCV
* NumPy
* Pillow
* Matplotlib
* licence Metashape 

## Installation

1. Clonez le repository à l'aide de la commande `git clone https://github.com/Amel92350/Multispectral.git`
2. Installez les dépendances nécessaires à l'aide de la commande `pip install -r requirements.txt`

## Utilisation

Pour exécuter ce logiciel, assurez-vous d'avoir installé les dépendances Python spécifiées. De plus, le logiciel utilise l'API Metashape pour certaines fonctionnalités. Voici comment configurer l'environnement :

1. **Téléchargez Agisoft Metashape Pro :**  Téléchargez Agisoft Metashape Professional depuis [le site officiel de Metashape](https://www.agisoft.com/downloads/installer/).

2. **Télécharger du module Python Metashape :** Téléchargez le module python de Metashape depuis le même site.

3. **Installez le module :** Installez le module python à l'aide de `pip` : 

     ```batch
     pip install Metashape-2.1.2-cp37.cp38.cp39.cp310.cp311-none-win_amd64.whl
     ```
     par exemple en remplaçant le nom du module avec celui que vous avez installé
   
4. **Lancement du logiciel :** Une fois l'environnement configuré, exécutez le logiciel à l'aide de la commande :

   ```bash
   python main.py

  Assurez-vous d'utiliser Python 3.11 ou une version supérieure pour exécuter le logiciel.


## Auteurs

* Amel92350
