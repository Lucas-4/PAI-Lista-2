import cv2
import numpy as np
import os
import time

# Define image paths (now in parent directory)
path_natural = "../images/strawberry.jpg"
path_medical = "../images/xray.jpg"
path_industrial = "../images/board.jpeg"

# Load images
images = {
    "natural": cv2.imread(path_natural),
    "medical": cv2.imread(path_medical),
    "industrial": cv2.imread(path_industrial),
}

# Create results folder
os.makedirs("./results", exist_ok=True)

# Target width for resized images (to speed up K-Means)
TARGET_WIDTH = 400

# Process each image
for image_type, img in images.items():
    if img is None:
        print(f"Erro ao carregar imagem {image_type}.")
        continue

    # Resize for processing
    h, w = img.shape[:2]
    new_h = int(h * TARGET_WIDTH / w)
    img_resized = cv2.resize(img, (TARGET_WIDTH, new_h))

    # Convert to grayscale for Otsu
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save Otsu result
    otsu_path = f"results/{image_type}_otsu.png"
    cv2.imwrite(otsu_path, otsu)
    print(f"Otsu salvo: {otsu_path}")

    # Vary K for K-Means
    for k in [2, 3, 4]:
        start = time.time()

        # Use the already resized image for K-Means
        pixel_values = img_resized.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.2)
        best_labels = None
        _, labels, centers = cv2.kmeans(  # type: ignore
            pixel_values, k, best_labels, criteria, 5, cv2.KMEANS_RANDOM_CENTERS
        )

        centers = np.uint8(centers)  # type: ignore
        labels = labels.flatten()
        kmeans_result = centers[labels]  # type: ignore
        kmeans_img = kmeans_result.reshape(img_resized.shape)

        # Print info
        print(f"Centróides para {image_type} com K={k}: {centers}")
        unique_colors = np.unique(kmeans_img.reshape(-1, 3), axis=0)
        print(f"Cores únicas (sem padding): {len(unique_colors)}")

        # Save only the K-means result image
        save_path = f"results/{image_type}_k{k}.png"
        cv2.imwrite(save_path, kmeans_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        print(f"Salvo: {save_path}")
        print(f"Tempo K-Means: {time.time() - start:.2f}s\n")
