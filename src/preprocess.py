import os
from pathlib import Path
from collections import Counter

# Define the correct dataset path
dataset_path = Path('dataset/dataset_blood_group')

# Get all blood group classes
classes = sorted([d.name for d in dataset_path.iterdir() if d.is_dir()])

print(f"Blood Group Classes Found: {classes}")
print(f"Total Classes: {len(classes)}\n")

# Count images per class
print("Images per class:")
print("")
class_counts = {}
for class_name in classes:
    class_folder = dataset_path / class_name
    # Count .BMP files
    image_files = list(class_folder.glob('*.BMP')) + list(class_folder.glob('*.bmp'))
    class_counts[class_name] = len(image_files)
    print(f"  {class_name:6s}: {len(image_files):4d} images")

print("")
print(f"Total Images: {sum(class_counts.values())}\n")

# Check class balance
max_count = max(class_counts.values())
min_count = min(class_counts.values())
imbalance_ratio = max_count / min_count

print(f" Class Balance Analysis:")
print(f"  Largest class: {max_count} images")
print(f"  Smallest class: {min_count} images")
print(f"  Imbalance ratio: {imbalance_ratio:.2f}")

if imbalance_ratio > 1.5:
    print("\nModerate class imbalance - recommend data augmentation")
else:
    print("\nDataset is well balanced")