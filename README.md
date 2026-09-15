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

## Project Timeline
- Day 1: Model training
- Day 2: Integration & alerts
- Day 3: Field testing
```

---

## **4. src/train.ipynb**

I'll give you this code **AFTER** you:
1. Finish installing packages
2. Create Roboflow account
3. Get the dataset download code from Roboflow

**Why wait?** The notebook needs your specific Roboflow API key and dataset code.

---

## **5. src/detector.py** 

I'll give you this **AFTER** training completes (Day 2), because it needs:
- Your trained model (`best.pt`)
- Your DroidCam IP address
- Your CallMeBot API key

---

## **6. src/alert.py**

I'll give you this on **Day 2** when we set up CallMeBot.

---

## **7. .gitignore** (If using Git)
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