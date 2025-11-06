import cv2
import numpy as np

# Path to the Otsu-segmented strawberry image
path_otsu_strawberry = "../results/natural_otsu.png"
path_original_strawberry = "../images/strawberry.jpg"

# Target width for consistent sizing
TARGET_WIDTH = 400


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
    print("Using segmented Otsu image: " + path_otsu_strawberry)
    print("="*60 + "\n")
    
    # Load the already-segmented Otsu strawberry image
    otsu_binary = cv2.imread(path_otsu_strawberry, cv2.IMREAD_GRAYSCALE)
    if otsu_binary is None:
        print(f"Erro ao carregar imagem Otsu: {path_otsu_strawberry}")
        print("Certifique-se de executar o script principal primeiro para gerar a imagem Otsu.")
        return
    
    # Load original strawberry for visualization
    img_strawberry = cv2.imread(path_original_strawberry)
    if img_strawberry is None:
        print(f"Erro ao carregar imagem original: {path_original_strawberry}")
        return
    
    # Resize original to match Otsu dimensions
    h, w = img_strawberry.shape[:2]
    new_h = int(h * TARGET_WIDTH / w)
    img_resized = cv2.resize(img_strawberry, (TARGET_WIDTH, new_h))
    
    # Find contours from the segmented Otsu image
    contours, _ = cv2.findContours(otsu_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
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
    cv2.imwrite("strawberry_chain_code_boundary.png", combined)
    
    # Save chain code to file
    with open("strawberry_chain_code.txt", "w") as f:
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
    print(f"\nResultados salvos em questao2/:")
    print(f"  - strawberry_chain_code_boundary.png")
    print(f"  - strawberry_chain_code.txt")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    process_strawberry_chain_code()
