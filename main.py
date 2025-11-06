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


# Chain Code Implementation for Strawberry Boundary
def compute_chain_code(contour):
    """
    Compute 8-directional chain code from a contour.
    Direction encoding:
    3  2  1
    4  *  0
    5  6  7
    """
    # Direction vectors for 8-connectivity
    directions = {
        (1, 0): 0,    # Right
        (1, -1): 1,   # Up-Right
        (0, -1): 2,   # Up
        (-1, -1): 3,  # Up-Left
        (-1, 0): 4,   # Left
        (-1, 1): 5,   # Down-Left
        (0, 1): 6,    # Down
        (1, 1): 7     # Down-Right
    }
    
    chain_code = []
    contour = contour.squeeze()
    
    for i in range(len(contour) - 1):
        x1, y1 = contour[i]
        x2, y2 = contour[i + 1]
        
        dx = np.sign(x2 - x1)
        dy = np.sign(y2 - y1)
        
        direction = directions.get((dx, dy), -1)
        if direction != -1:
            chain_code.append(direction)
    
    return chain_code


def process_strawberry_chain_code():
    """Process strawberry image and extract boundary using chain code."""
    print("\n" + "="*60)
    print("CHAIN CODE - Strawberry Boundary Representation")
    print("Using segmented Otsu image: results/natural_otsu.png")
    print("="*60 + "\n")
    
    # Load the already-segmented Otsu strawberry image
    otsu_binary = cv2.imread("results/natural_otsu.png", cv2.IMREAD_GRAYSCALE)
    if otsu_binary is None:
        print("Erro ao carregar imagem Otsu da morango.")
        return
    
    # Load original strawberry for visualization
    img_strawberry = cv2.imread(path_natural)
    if img_strawberry is None:
        print("Erro ao carregar imagem original da morango.")
        return
    
    # Resize original to match Otsu dimensions
    h, w = img_strawberry.shape[:2]
    new_h = int(h * TARGET_WIDTH / w)
    img_resized = cv2.resize(img_strawberry, (TARGET_WIDTH, new_h))
    
    # Find contours from the segmented Otsu image
    contours, _ = cv2.findContours(otsu_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # type: ignore
    
    if len(contours) == 0:
        print("Nenhum contorno encontrado.")
        return
    
    # Get the largest contour (presumably the strawberry)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Compute chain code
    chain_code = compute_chain_code(largest_contour)
    
    # Create visualization
    img_boundary = img_resized.copy()
    cv2.drawContours(img_boundary, [largest_contour], -1, (0, 255, 0), 2)
    
    # Create binary visualization with boundary using the loaded Otsu image
    binary_rgb = cv2.cvtColor(otsu_binary, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(binary_rgb, [largest_contour], -1, (0, 255, 0), 2)
    
    # Combine original with boundary and binary with boundary
    combined = np.hstack((img_boundary, binary_rgb))
    
    # Save results
    cv2.imwrite("results/strawberry_chain_code_boundary.png", combined)
    
    # Save chain code to file
    with open("results/strawberry_chain_code.txt", "w") as f:
        f.write("Chain Code (8-directional):\n")
        f.write("Direction encoding: 0=R, 1=UR, 2=U, 3=UL, 4=L, 5=DL, 6=D, 7=DR\n\n")
        f.write("Chain Code Sequence:\n")
        f.write("".join(map(str, chain_code[:100])) + "...\n\n")
        f.write(f"Total boundary points: {len(chain_code)}\n")
        f.write(f"Contour area: {cv2.contourArea(largest_contour):.2f} pixels\n")
        f.write(f"Contour perimeter: {cv2.arcLength(largest_contour, True):.2f} pixels\n\n")
        f.write("Full chain code:\n")
        for i in range(0, len(chain_code), 50):
            f.write("".join(map(str, chain_code[i:i+50])) + "\n")
    
    # Print summary
    print(f"Contorno encontrado com {len(largest_contour)} pontos")
    print(f"Chain code length: {len(chain_code)}")
    print(f"Área do contorno: {cv2.contourArea(largest_contour):.2f} pixels")
    print(f"Perímetro: {cv2.arcLength(largest_contour, True):.2f} pixels")
    print(f"\nPrimeiros 100 códigos: {''.join(map(str, chain_code[:100]))}")
    print(f"\nResultados salvos:")
    print(f"  - results/strawberry_chain_code_boundary.png")
    print(f"  - results/strawberry_chain_code.txt")
    print("\n" + "="*60 + "\n")


# Execute chain code processing
process_strawberry_chain_code()
