# Questão 2 - Chain Code Boundary Representation

This folder contains a standalone implementation of the chain code algorithm for representing object boundaries.

## What is Chain Code?

Chain code is a technique for representing the boundary of an object by encoding the direction of movement as you trace around its edge. Instead of storing every pixel coordinate, you only need:
- A starting point (x, y)
- A sequence of directional codes

## Direction Encoding (8-connectivity)

```
3  2  1
4  ●  0
5  6  7
```

- **0** = Right (East)
- **1** = Up-Right (Northeast)
- **2** = Up (North)
- **3** = Up-Left (Northwest)
- **4** = Left (West)
- **5** = Down-Left (Southwest)
- **6** = Down (South)
- **7** = Down-Right (Southeast)

## Prerequisites

Before running this script, you need to:

1. Run the main project script to generate the Otsu-segmented strawberry image:
   ```bash
   cd ..
   python main.py
   ```

2. This will create `results/natural_otsu.png`, which this script uses as input.

## Running the Chain Code Script

From the `questao2` folder:

```bash
python main.py
```

Or from the project root:

```bash
cd questao2
python main.py
```

## Input

The script reads:
- **Otsu-segmented image**: `../results/natural_otsu.png` (binary strawberry image)
- **Original image**: `../images/strawberry.jpg` (for visualization)

## Output

The script generates two files in the `questao2` folder:

1. **strawberry_chain_code_boundary.png**
   - Visual showing the original strawberry with boundary (left)
   - Binary Otsu image with boundary traced in green (right)

2. **strawberry_chain_code.txt**
   - Complete chain code sequence
   - Direction encoding explanation
   - Statistics: total boundary points, contour area, perimeter
   - First 100 codes preview
   - Full chain code sequence

## Example Output

```
============================================================
CHAIN CODE - Strawberry Boundary Representation
Using segmented Otsu image: ../results/natural_otsu.png
============================================================

Contorno encontrado com 1328 pontos
Chain code length: 1327
Área do contorno: 105735.00 pixels
Perímetro: 1328.00 pixels

Primeiros 100 códigos: 6666666666666666666666666666...

Resultados salvos em questao2/:
  - strawberry_chain_code_boundary.png
  - strawberry_chain_code.txt
```

## How It Works

1. **Load Segmented Image**: Reads the binary Otsu-segmented strawberry
2. **Find Contours**: Detects the boundary of the white object (strawberry)
3. **Select Largest Contour**: Picks the biggest boundary (the strawberry itself)
4. **Trace Boundary**: Walks around the boundary pixel by pixel
5. **Encode Directions**: At each step, records which direction the boundary moves
6. **Save Results**: Outputs visualization and text file with chain code

## Understanding the Chain Code

The chain code `6666...0000...2222...4444...` means:
- Many **6's**: Moving down along one edge
- Many **0's**: Moving right along the bottom
- Many **2's**: Moving up along the opposite edge  
- Many **4's**: Moving left along the top

This traces a complete loop around the strawberry boundary!

## Files in This Folder

- `main.py` - Chain code implementation script
- `README.md` - This documentation file
- `strawberry_chain_code_boundary.png` - Output visualization (generated)
- `strawberry_chain_code.txt` - Output chain code (generated)

## Troubleshooting

**Error: "Erro ao carregar imagem Otsu"**
- Make sure you've run the main project script first: `python ../main.py`
- Check that `../results/natural_otsu.png` exists

**Error: "Nenhum contorno encontrado"**
- The Otsu segmentation might not have detected the strawberry
- Try adjusting the input image or thresholding parameters
