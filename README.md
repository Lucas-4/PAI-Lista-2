

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- Matplotlib (optional, for viewing results)

## Installation

1. Clone or download this project to your local machine

2. Install the required dependencies:

```bash
pip install opencv numpy matplotlib
```

## Project Structure

```
.
├── main.py                      # Main processing script
├── images/                      # Input images folder
│   ├── strawberry.jpg          # Natural image (strawberry)
│   ├── xray.jpg                # Medical image (x-ray)
│   └── board.jpeg              # Industrial image (circuit board)
└── results/                     # Output folder (created automatically)
    ├── natural_otsu.png        # Otsu segmentation results
    ├── natural_k2.png          # K-means with k=2
    ├── natural_k3.png          # K-means with k=3
    ├── natural_k4.png          # K-means with k=4
    ├── medical_*.png           # Medical image results
    ├── industrial_*.png        # Industrial image results
    ├── strawberry_chain_code_boundary.png
    └── strawberry_chain_code.txt
```

## Usage

### Running the Program

Simply run the main script:

```bash
python main.py
```

### What the Program Does

1. **Loads three test images** from the `images/` folder:
   - Natural image: `strawberry.jpg`
   - Medical image: `xray.jpg`
   - Industrial image: `board.jpeg`

2. **Applies Otsu's Thresholding** to each image:
   - Creates binary (black and white) segmented images
   - Saves results as `{image_type}_otsu.png`

3. **Applies K-Means Clustering** with different cluster values (k=2, 3, 4):
   - Groups pixels by color similarity
   - Saves each result as `{image_type}_k{value}.png`

4. **Generates Chain Code** for the strawberry boundary:
   - Uses the Otsu-segmented strawberry image
   - Traces the boundary and encodes it as directional codes
   - Saves visualization and full chain code sequence

### Expected Output

After running, the `results/` folder will contain:

**Otsu Thresholding Results** (3 files):
- `natural_otsu.png`
- `medical_otsu.png`
- `industrial_otsu.png`

**K-Means Clustering Results** (9 files):
- `natural_k2.png`, `natural_k3.png`, `natural_k4.png`
- `medical_k2.png`, `medical_k3.png`, `medical_k4.png`
- `industrial_k2.png`, `industrial_k3.png`, `industrial_k4.png`

**Chain Code Results** (2 files):
- `strawberry_chain_code_boundary.png` - Visual showing the traced boundary
- `strawberry_chain_code.txt` - Complete chain code sequence

### Console Output

The program will display:
- Processing progress for each image
- K-Means centroids (cluster centers)
- Number of unique colors
- Processing time for each operation
- Chain code statistics (boundary points, area, perimeter)

Example:
```
Otsu salvo: results/natural_otsu.png
Centróides para natural com K=2: [[231 234 234] [33 41 132]]
Cores únicas (sem padding): 2
Salvo: results/natural_k2.png
Tempo K-Means: 0.25s

...

============================================================
CHAIN CODE - Strawberry Boundary Representation
Using segmented Otsu image: results/natural_otsu.png
============================================================
Contorno encontrado com 1328 pontos
Chain code length: 1327
Área do contorno: 105735.00 pixels
Perímetro: 1328.00 pixels
```

## Understanding Chain Code

Chain code represents object boundaries using directional encoding:

```
3  2  1
4  ●  0
5  6  7
```

- **0** = Right
- **2** = Up
- **4** = Left
- **6** = Down
- **1, 3, 5, 7** = Diagonal directions

The algorithm traces around the strawberry boundary and records which direction it moves at each step, creating a compact representation of the shape.

## Customization

### Change Target Resolution
Edit `TARGET_WIDTH` in `main.py`:
```python
TARGET_WIDTH = 400  # Change to desired width
```

### Use Different Images
Replace the image files in the `images/` folder or update the paths in `main.py`:
```python
path_natural = "./images/your_image.jpg"
path_medical = "./images/your_medical.jpg"
path_industrial = "./images/your_industrial.jpg"
```

### Modify K-Means Clusters
Change the k values in the loop:
```python
for k in [2, 3, 4]:  # Modify this list
```

## Troubleshooting

**Error: "No module named 'cv2'"**
- Install OpenCV: `pip install opencv-python`

**Error: "Erro ao carregar imagem"**
- Ensure image files exist in the `images/` folder
- Check file paths and names are correct

**No results folder**
- The folder is created automatically
- Ensure you have write permissions in the project directory

## License

This project is for educational purposes.
