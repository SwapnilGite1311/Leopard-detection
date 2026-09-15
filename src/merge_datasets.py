import os
import shutil
import yaml
from pathlib import Path

print("🔄 Merging datasets...")

# Dataset paths
datasets = [
    "data/leopard_detection-5",
    "data/Leopard-Detection-1",
    "data/sugarcane-14"
]

# Output merged dataset path
merged_path = "data/merged_dataset"

# Create merged dataset structure
os.makedirs(f"{merged_path}/train/images", exist_ok=True)
os.makedirs(f"{merged_path}/train/labels", exist_ok=True)
os.makedirs(f"{merged_path}/valid/images", exist_ok=True)
os.makedirs(f"{merged_path}/valid/labels", exist_ok=True)

# Copy files from each dataset
for dataset in datasets:
    dataset_name = os.path.basename(dataset)
    print(f"\n📂 Processing {dataset_name}...")
    
    # Copy training images and labels
    if os.path.exists(f"{dataset}/train/images"):
        for img in os.listdir(f"{dataset}/train/images"):
            src = f"{dataset}/train/images/{img}"
            dst = f"{merged_path}/train/images/{dataset_name}_{img}"
            shutil.copy(src, dst)
        
        for label in os.listdir(f"{dataset}/train/labels"):
            src = f"{dataset}/train/labels/{label}"
            dst = f"{merged_path}/train/labels/{dataset_name}_{label}"
            shutil.copy(src, dst)
        
        print(f"  ✅ Copied training data")
    
    # Copy validation images and labels
    if os.path.exists(f"{dataset}/valid/images"):
        for img in os.listdir(f"{dataset}/valid/images"):
            src = f"{dataset}/valid/images/{img}"
            dst = f"{merged_path}/valid/images/{dataset_name}_{img}"
            shutil.copy(src, dst)
        
        for label in os.listdir(f"{dataset}/valid/labels"):
            src = f"{dataset}/valid/labels/{label}"
            dst = f"{merged_path}/valid/labels/{dataset_name}_{label}"
            shutil.copy(src, dst)
        
        print(f"  ✅ Copied validation data")

# Create data.yaml for merged dataset
data_yaml = {
    'path': '../data/merged_dataset',
    'train': 'train/images',
    'val': 'valid/images',
    'nc': 1,
    'names': ['leopard']
}

with open(f"{merged_path}/data.yaml", 'w') as f:
    yaml.dump(data_yaml, f)

print(f"\n✅ Merge complete!")
print(f"📊 Merged dataset location: {merged_path}")
print(f"   Train images: {len(os.listdir(f'{merged_path}/train/images'))}")
print(f"   Valid images: {len(os.listdir(f'{merged_path}/valid/images'))}")