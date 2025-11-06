

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
