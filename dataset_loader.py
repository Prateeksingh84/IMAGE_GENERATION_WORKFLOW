import os
import kagglehub

def download_images_dataset():
    dataset_path = kagglehub.dataset_download("pavansanagapati/images-dataset")
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"❌ Dataset not found after download: {dataset_path}")

    # Collect all image file paths
    image_files = []
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_files.append(os.path.join(root, file))

    if not image_files:
        raise FileNotFoundError(f"❌ No image files found in {dataset_path}")

    return image_files
