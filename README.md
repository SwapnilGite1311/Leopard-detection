# Leopard Detection System

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Update `config.yaml` with your DroidCam IP and phone number
3. Train model: Open `src/train.ipynb` in VS Code
4. Run detection: `python src/detector.py`

## Requirements
- RTX 3050 GPU
- Python 3.8+
- Android phone with DroidCam app
- Same WiFi network for phone and laptop

---

## ** .gitignore** (If using Git)
```
# Python
leopard_env/
__pycache__/
*.pyc
*.pyo
*.egg-info/

# Data
data/dataset/
models/runs/
detections/
*.pt
*.jpg
*.png

# Config
config_local.yaml
