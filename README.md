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

## Installation

1. Clonez le repository à l'aide de la commande `git clone https://github.com/Amel92350/Multispectral.git`
2. Installez les dépendances nécessaires à l'aide de la commande `pip install -r requirements.txt`

## Utilisation

Pour exécuter ce logiciel, assurez-vous d'avoir installé les dépendances Python spécifiées. De plus, le logiciel utilise l'API Metashape pour certaines fonctionnalités. Voici comment configurer l'environnement :

1. **Installation de Metashape :** Téléchargez et installez Metashape depuis [le site officiel de Metashape](https://www.agisoft.com/downloads/installer/) selon les instructions fournies.

2. **Configuration de l'environnement :** Pour utiliser Metashape avec ce logiciel, assurez-vous que l'exécutable Python de Metashape est ajouté à votre chemin d'accès système. Vous pouvez le faire en créant un fichier batch (.bat) comme suit :

   - Créez un nouveau fichier texte et renommez-le `setup_env.bat`.

   - Ouvrez `setup_env.bat` avec un éditeur de texte et ajoutez les lignes suivantes :

     ```batch
     @echo off
     set METASHAPE_PATH="C:\Chemin\vers\le\dossier\Metashape"
     set PATH=%METASHAPE_PATH%;%PATH%
     ```

     Remplacez `"C:\Chemin\vers\le\dossier\Metashape"` par le chemin réel où Metashape est installé sur votre système.

   - Enregistrez le fichier `setup_env.bat`.

3. **Exécution du batch :** Avant d'exécuter le logiciel, ouvrez une nouvelle fenêtre de terminal et exécutez `setup_env.bat`. Cela ajoutera Metashape à votre chemin d'accès, permettant au logiciel de trouver l'API Metashape correctement.

4. **Lancement du logiciel :** Une fois l'environnement configuré, exécutez le logiciel à l'aide de la commande :

   ```bash
   python main.py
## Auteurs

* Amel92350
