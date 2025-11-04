import cv2
import numpy as np
import matplotlib.pyplot as plt
import os  # A biblioteca 'os' nos ajuda a interagir com o sistema operacional, como criar pastas.

# ---------------------------------------------------------------------------------
# STEP 0: SETUP THE RESULTS DIRECTORY
# ---------------------------------------------------------------------------------
# Define o nome da pasta onde os resultados serão salvos.
results_folder = "results"
# Verifica se a pasta já existe. Se não, cria a pasta.
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
    print(f"Directory '{results_folder}' was created.")


# ---------------------------------------------------------------------------------
# HELPER FUNCTION TO ADD TEXT TO IMAGES
# ---------------------------------------------------------------------------------
def add_text_to_image(image, text):
    """
    Adds white text with a black background (for better readability) at the bottom-left of an image.
    This is useful for labeling the images directly.
    """
    # Define a fonte, escala, cor e espessura do texto.
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    color = (255, 255, 255)  # White color for text
    thickness = 2

    # Pega o tamanho do texto para criar um fundo preto para ele.
    (text_width, text_height), baseline = cv2.getTextSize(
        text, font, font_scale, thickness
    )

    # Define a posição do texto (canto inferior esquerdo).
    org = (10, image.shape[0] - 10)  # 10 pixels from the bottom-left corner

    # Desenha um retângulo preto de fundo para o texto se destacar.
    cv2.rectangle(
        image,
        (org[0] - 5, org[1] + 5),
        (org[0] + text_width + 5, org[1] - text_height - 5),
        (0, 0, 0),
        -1,
    )

    # Escreve o texto na imagem.
    cv2.putText(image, text, org, font, font_scale, color, thickness, cv2.LINE_AA)

    return image


# ---------------------------------------------------------------------------------
# STEP 2: MODIFIED FUNCTION TO PROCESS AND SAVE
# ---------------------------------------------------------------------------------
def process_and_save_comparison(image_path, canny_threshold1, canny_threshold2):
    """
    Loads an image, applies Otsu and Canny, adds descriptive text to each result,
    combines them into a single image, and saves it to the results folder.
    """
    # --- PART A: IMAGE LOADING AND PREPARATION ---
    original_color_img = cv2.imread(image_path)
    if original_color_img is None:
        print(f"ERROR: Could not find or open the image at path: {image_path}")
        return

    gray_img = cv2.cvtColor(original_color_img, cv2.COLOR_BGR2GRAY)

    # --- PART B: APPLYING ALGORITHMS ---
    _, otsu_img_binary = cv2.threshold(
        gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    canny_img_binary = cv2.Canny(gray_img, canny_threshold1, canny_threshold2)

    # --- PART C: PREPARING IMAGES FOR VISUALIZATION/SAVING ---
    # Para juntar as imagens, todas precisam ter o mesmo formato (3 canais de cor).
    # Convertemos as imagens em escala de cinza de volta para o formato de 3 canais (BGR).
    otsu_img_color = cv2.cvtColor(otsu_img_binary, cv2.COLOR_GRAY2BGR)
    canny_img_color = cv2.cvtColor(canny_img_binary, cv2.COLOR_GRAY2BGR)

    # Adiciona texto descritivo a cada imagem.
    original_labeled = add_text_to_image(original_color_img.copy(), "Original")
    otsu_labeled = add_text_to_image(otsu_img_color, "Otsu")
    canny_labeled = add_text_to_image(
        canny_img_color, f"Canny (T_low={canny_threshold1}, T_high={canny_threshold2})"
    )

    # --- PART D: COMBINING AND SAVING THE FINAL IMAGE ---
    # np.hstack empilha as imagens horizontalmente.
    # [original_labeled, otsu_labeled, canny_labeled] é uma lista com as 3 imagens.
    final_image = np.hstack([original_labeled, otsu_labeled, canny_labeled])

    # Cria um nome de arquivo descritivo.
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    output_filename = f"{base_filename}_canny_{canny_threshold1}_{canny_threshold2}.jpg"
    output_path = os.path.join(results_folder, output_filename)

    # Salva a imagem combinada na pasta de resultados.
    cv2.imwrite(output_path, final_image)
    print(f"Result saved to: {output_path}")

    # Opcional: Mostrar a imagem combinada na tela também.
    cv2.imshow(f"Comparison for {base_filename}", final_image)


# ---------------------------------------------------------------------------------
# STEP 3: MAIN SCRIPT EXECUTION
# ---------------------------------------------------------------------------------
# Define os caminhos para as imagens de entrada.
# (Note que renomeei 'board.jpeg' para um nome mais genérico no código)
path_natural = "./images/strawberry.jpg"
path_medical = "./images/xray.jpg"
path_industrial = (
    "./images/board.jpeg"  # Ajuste se o nome do seu arquivo for 'board.jpeg'
)

# --- TESTE 1: Parâmetros "Ideais" para cada imagem ---
print("\n--- Generating results with 'ideal' parameters ---")
process_and_save_comparison(path_natural, canny_threshold1=80, canny_threshold2=180)
process_and_save_comparison(path_medical, canny_threshold1=50, canny_threshold2=150)
process_and_save_comparison(path_industrial, canny_threshold1=100, canny_threshold2=200)

# --- TESTE 2: Variando os parâmetros para a imagem do morango para análise de sensibilidade ---
print("\n--- Testing Canny's parameter sensitivity on the strawberry image ---")
# Limiares baixos (deve pegar muito ruído)
process_and_save_comparison(path_natural, canny_threshold1=20, canny_threshold2=60)
# Limiares altos (deve perder detalhes)
process_and_save_comparison(path_natural, canny_threshold1=150, canny_threshold2=230)

# --- TESTE 3: Variando os parâmetros para a imagem da PCB ---
print("\n--- Testing Canny's parameter sensitivity on the PCB image ---")
# Limiares baixos (pode pegar ruído da superfície da placa)
process_and_save_comparison(path_industrial, canny_threshold1=50, canny_threshold2=100)
# Limiares altos (pode perder as trilhas mais finas)
process_and_save_comparison(path_industrial, canny_threshold1=180, canny_threshold2=250)


# ---------------------------------------------------------------------------------
# STEP 4: DISPLAY AND WAIT
# ---------------------------------------------------------------------------------
# cv2.imshow é não-bloqueante, então as imagens podem fechar imediatamente.
# Usamos cv2.waitKey(0) para pausar o script e esperar que uma tecla seja pressionada.
# Isso manterá todas as janelas abertas.
print("\nAll processing complete. Press any key in one of the image windows to exit.")
cv2.waitKey(0)
# Destroi todas as janelas abertas pelo OpenCV quando terminar.
cv2.destroyAllWindows()

print("Program finished.")
