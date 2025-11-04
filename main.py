import cv2
import numpy as np
import os
import time

# Define image paths
path_natural = "./images/strawberry.jpg"
path_medical = "./images/xray.jpg"
path_industrial = "./images/board.jpeg"

# Load images
images = {
    "natural": cv2.imread(path_natural),
    "medical": cv2.imread(path_medical),
    "industrial": cv2.imread(path_industrial),
}

# Create results folder
os.makedirs("results", exist_ok=True)

# Target width for resized images (to speed up K-Means)
TARGET_WIDTH = 400


def resize_with_padding(img, target_width):
    h, w = img.shape[:2]
    scale = target_width / w
    new_h = int(h * scale)
    resized = cv2.resize(img, (target_width, new_h))

    # Create canvas with target size (square or fixed height)
    canvas_h = max(new_h, target_width)  # or use fixed: 512
    canvas = np.zeros((canvas_h, target_width, 3), dtype=np.uint8)

    # Center the resized image
    y_offset = (canvas_h - new_h) // 2
    canvas[y_offset : y_offset + new_h, :] = resized

    return canvas, (target_width, new_h)  # return resized and original resized size


# Process each image
for image_type, img in images.items():
    if img is None:
        print(f"Erro ao carregar imagem {image_type}.")
        continue

    # Resize original with padding
    img_resized, orig_size = resize_with_padding(img, TARGET_WIDTH)

    # Convert to grayscale for Otsu
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    otsu_rgb = cv2.cvtColor(otsu, cv2.COLOR_GRAY2BGR)

    # Vary K for K-Means
    for k in [2, 3, 4]:
        start = time.time()

        # Use original resized image (without padding) for K-Means to avoid black pixels
        img_for_kmeans = cv2.resize(img, (TARGET_WIDTH, orig_size[1]))
        pixel_values = img_for_kmeans.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.2)
        best_labels = None
        _, labels, centers = cv2.kmeans(  # type: ignore
            pixel_values, k, best_labels, criteria, 5, cv2.KMEANS_RANDOM_CENTERS
        )

        centers = np.uint8(centers)  # type: ignore
        labels = labels.flatten()
        kmeans_result = centers[labels]  # type: ignore
        kmeans_img = kmeans_result.reshape(img_for_kmeans.shape)

        # Resize K-Means result with padding to match canvas
        kmeans_padded, _ = resize_with_padding(kmeans_img, TARGET_WIDTH)

        # Print info
        print(f"Centróides para {image_type} com K={k}: {centers}")
        unique_colors = np.unique(kmeans_img.reshape(-1, 3), axis=0)
        print(f"Cores únicas (sem padding): {len(unique_colors)}")

        # Combine: Original | Otsu | K-Means (all same height)
        combined = np.hstack((img_resized, otsu_rgb, kmeans_padded))

        # Save as PNG
        save_path = f"results/{image_type}_k{k}.png"
        cv2.imwrite(save_path, combined, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        print(f"Salvo: {save_path}")
        print(f"Tempo K-Means: {time.time() - start:.2f}s\n")
