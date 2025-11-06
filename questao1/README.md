# Questão 1 - Otsu Thresholding and K-Means Clustering

This folder contains the implementation of image segmentation techniques using Otsu's thresholding and K-Means clustering.

## Features

- **Otsu's Thresholding**: Automatic binary image segmentation
- **K-Means Clustering**: Color-based image segmentation with k=2, 3, and 4 clusters

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

## Installation

Install the required dependencies:

```bash
pip install opencv-python numpy
```

## Running the Program

From the `questao1` folder:

```bash
python main.py
```

Or from the project root:

```bash
cd questao1
python main.py
```

## Input Images

The script processes three images from the `../images/` folder:
- **Natural image**: `strawberry.jpg`
- **Medical image**: `xray.jpg`
- **Industrial image**: `board.jpeg`

## Output

All results are saved in the `questao1/results/` folder:

### Otsu Thresholding Results (3 files):
- `natural_otsu.png` - Binary segmentation of strawberry
- `medical_otsu.png` - Binary segmentation of x-ray
- `industrial_otsu.png` - Binary segmentation of circuit board

### K-Means Clustering Results (9 files):
- `natural_k2.png`, `natural_k3.png`, `natural_k4.png` - Strawberry with 2, 3, 4 clusters
- `medical_k2.png`, `medical_k3.png`, `medical_k4.png` - X-ray with 2, 3, 4 clusters
- `industrial_k2.png`, `industrial_k3.png`, `industrial_k4.png` - Circuit board with 2, 3, 4 clusters

## What the Program Does

### 1. Otsu's Thresholding
Automatically determines the optimal threshold value to separate foreground from background, creating a binary (black and white) image.

### 2. K-Means Clustering
Groups pixels into k clusters based on color similarity:
- **k=2**: Simplest segmentation with 2 colors
- **k=3**: Medium complexity with 3 colors
- **k=4**: More detailed with 4 colors

## Console Output

Example output:
```
Otsu salvo: results/natural_otsu.png
Centróides para natural com K=2: [[231 234 234] [33 41 132]]
Cores únicas (sem padding): 2
Salvo: results/natural_k2.png
Tempo K-Means: 0.25s
...
```

## Customization

### Change Image Resolution
Edit the `TARGET_WIDTH` constant:
```python
TARGET_WIDTH = 400  # Change to desired width
```

### Modify K-Means Clusters
Change the k values in the loop:
```python
for k in [2, 3, 4]:  # Add or remove values
```

## Files in This Folder

- `main.py` - Main processing script
- `README.md` - This documentation file
- `results/` - Output folder (created automatically)

## Notes

- Images are resized to 400px width for faster processing
- Otsu images are used as input for the chain code in questão 2
- All processing times are displayed in the console
