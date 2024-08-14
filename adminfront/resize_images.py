from PIL import Image
import os

def resize_images(input_folder, output_folder, size=(500, 500)):
    # Crée le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Parcourt toutes les images du dossier source
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # Ouvre l'image
            img = Image.open(os.path.join(input_folder, filename))
            # Redimensionne l'image à la taille spécifiée
            img = img.resize(size, Image.ANTIALIAS)
            # Enregistre l'image redimensionnée dans le dossier de sortie
            img.save(os.path.join(output_folder, filename))

# Utilisation du script
input_folder = 'media\produits'  # Remplace par le chemin de ton dossier d'images
output_folder = 'media\produit'  # Remplace par le chemin de ton dossier de sortie
size = (500, 500)  # Spécifie la taille souhaitée

resize_images(input_folder, output_folder, size)
