import cv2
import numpy as np
import os

# ---------------------------------------------------------------------------------
# STEP 0: SETUP THE RESULTS DIRECTORY
# ---------------------------------------------------------------------------------
results_folder = "results"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f"Directory '{results_folder}' was created.")


# ---------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------------
def add_text_to_image(image, text):
    """Adds white text with a black background to a BGR image."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    color = (255, 255, 255)  # White color
    thickness = 2

    (text_width, text_height), baseline = cv2.getTextSize(
        text, font, font_scale, thickness
    )
    org = (10, image.shape[0] - 10)

    cv2.rectangle(
        image,
        (org[0] - 5, org[1] + 5),
        (org[0] + text_width + 5, org[1] - text_height - 5),
        (0, 0, 0),
        -1,
    )
    cv2.putText(image, text, org, font, font_scale, color, thickness, cv2.LINE_AA)

    return image


# *** NOVA FUNÇÃO PARA CANNY AUTOMÁTICO ***
def find_auto_canny_thresholds(image, sigma=0.33):
    """
    Finds optimal Canny thresholds based on the median of the image intensities.
    """
    # 1. Calculate the median of the single channel pixel intensities
    median = np.median(image)

    # 2. Apply automatic Canny thresholding using the computed median
    lower_threshold = int(max(0, (1.0 - sigma) * median))
    upper_threshold = int(min(255, (1.0 + sigma) * median))

    print(
        f"  - Auto Canny: Median={median:.0f}, Calculated Thresholds=({lower_threshold}, {upper_threshold})"
    )

    return lower_threshold, upper_threshold


# ---------------------------------------------------------------------------------
# MAIN FUNCTION TO PROCESS AND SAVE
# ---------------------------------------------------------------------------------
def process_and_save_comparison(
    image_path, canny_threshold1, canny_threshold2, is_auto=False
):
    """
    Loads an image, applies Otsu and Canny, adds descriptive text,
    combines them, and saves the result.
    The 'is_auto' flag helps in naming the output file.
    """
    original_color_img = cv2.imread(image_path)
    if original_color_img is None:
        print(f"ERROR: Could not open the image at path: {image_path}")
        return

    gray_img = cv2.cvtColor(original_color_img, cv2.COLOR_BGR2GRAY)

    _, otsu_img_binary = cv2.threshold(
        gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    canny_img_binary = cv2.Canny(gray_img, canny_threshold1, canny_threshold2)

    # Prepare images for stacking
    otsu_img_color = cv2.cvtColor(otsu_img_binary, cv2.COLOR_GRAY2BGR)
    canny_img_color = cv2.cvtColor(canny_img_binary, cv2.COLOR_GRAY2BGR)

    # Add labels
    original_labeled = add_text_to_image(original_color_img.copy(), "Original")
    otsu_labeled = add_text_to_image(otsu_img_color, "Otsu")

    canny_label = f"Canny (T={canny_threshold1},{canny_threshold2})"
    if is_auto:
        canny_label = f"Auto-Canny (T={canny_threshold1},{canny_threshold2})"

    canny_labeled = add_text_to_image(canny_img_color, canny_label)

    # Combine and save
    final_image = np.hstack([original_labeled, otsu_labeled, canny_labeled])

    base_filename = os.path.splitext(os.path.basename(image_path))[0]

    if is_auto:
        output_filename = f"{base_filename}_canny_auto.jpg"
    else:
        output_filename = (
            f"{base_filename}_canny_manual_{canny_threshold1}_{canny_threshold2}.jpg"
        )

    output_path = os.path.join(results_folder, output_filename)

    cv2.imwrite(output_path, final_image)
    print(f"  - Result saved to: {output_path}")

    # Display the window with a descriptive title
    window_title = f"{base_filename} | {canny_label}"
    cv2.imshow(window_title, final_image)


# ---------------------------------------------------------------------------------
# MAIN SCRIPT EXECUTION
# ---------------------------------------------------------------------------------
path_natural = "./images/strawberry.jpg"
path_medical = "./images/xray.jpg"
path_industrial = (
    "./images/board.jpeg"  # Ajuste se o nome do seu arquivo for 'board.jpeg'
)

image_paths = {
    "natural": path_natural,
    "medical": path_medical,
    "industrial": path_industrial,
}

# --- TESTE 1: Parâmetros AUTOMÁTICOS para cada imagem ---
print("\n--- Generating results with AUTOMATIC Canny parameters ---")
for name, path in image_paths.items():
    print(f"Processing '{name}' image...")
    # Carrega a imagem cinza uma vez para encontrar os limiares
    gray_image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
    # Encontra os limiares automáticos
    auto_t1, auto_t2 = find_auto_canny_thresholds(gray_image)
    # Processa e salva usando esses limiares
    process_and_save_comparison(path, auto_t1, auto_t2, is_auto=True)

# --- TESTE 2: Parâmetros MANUAIS "Ideais" para cada imagem ---
print("\n--- Generating results with MANUALLY tuned 'ideal' parameters ---")
process_and_save_comparison(path_natural, canny_threshold1=80, canny_threshold2=180)
process_and_save_comparison(path_medical, canny_threshold1=50, canny_threshold2=150)
process_and_save_comparison(path_industrial, canny_threshold1=100, canny_threshold2=200)

# --- TESTE 3: Variando os parâmetros MANUAIS para análise de sensibilidade ---
print("\n--- Testing Canny's parameter sensitivity with MANUAL variations ---")
# Variações para o MORANGO
print("Processing Strawberry variations...")
process_and_save_comparison(path_natural, canny_threshold1=20, canny_threshold2=60)
process_and_save_comparison(path_natural, canny_threshold1=150, canny_threshold2=230)
# Variações para a PCB
print("Processing PCB variations...")
process_and_save_comparison(path_industrial, canny_threshold1=50, canny_threshold2=100)
process_and_save_comparison(path_industrial, canny_threshold1=180, canny_threshold2=250)
# Variações para o RAIO-X
print("Processing X-Ray variations...")
process_and_save_comparison(path_medical, canny_threshold1=10, canny_threshold2=30)
process_and_save_comparison(path_medical, canny_threshold1=100, canny_threshold2=200)

# ---------------------------------------------------------------------------------
# DISPLAY AND WAIT
# ---------------------------------------------------------------------------------
print("\nAll processing complete. Press any key in one of the image windows to exit.")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Program finished.")
