from PIL import Image
import os

def resize_images(input_folder, output_folder, size=(500, 500)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    resample_filter = getattr(Image, 'Resampling', Image).LANCZOS if hasattr(Image, 'Resampling') else getattr(Image, 'ANTIALIAS', Image.BICUBIC)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            try:
                img_path = os.path.join(input_folder, filename)
                with Image.open(img_path) as img:
                    img = img.convert('RGB')
                    img = img.resize(size, resample_filter)
                    img.save(os.path.join(output_folder, filename), quality=90)
            except Exception as e:
                print(f"Erreur pour {filename}: {e}")

if __name__ == '__main__':
    input_folder = os.path.join('media', 'produits')
    output_folder = os.path.join('media', 'produit')
    size = (500, 500)
    if os.path.exists(input_folder):
        resize_images(input_folder, output_folder, size)

