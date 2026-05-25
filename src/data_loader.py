import cv2
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import numpy as np

def load_dataset(dataset_path, img_height, img_width):
    """
    Load all images and labels from dataset directory

    Returns:
        images: numpy array of shape (num_samples, height, width, channels)
        labels: numpy array of integer labels
        class_names: list of class names
    """
    dataset_path = Path(dataset_path)

    images = []
    labels = []
    class_names = sorted([d.name for d in dataset_path.iterdir() if d.is_dir()])

    print(f" Loading images from {len(class_names)} classes...")
    print(f"Classes: {class_names}\n")

    # Create class to index mapping
    class_to_idx = {class_name: idx for idx, class_name in enumerate(class_names)}

    # Load images with progress bar
    for class_name in class_names:
        class_folder = dataset_path / class_name
        image_files = list(class_folder.glob('*.BMP'))

        print(f"Loading {class_name}: {len(image_files)} images", end=' ')

        for img_path in tqdm(image_files, desc=class_name, leave=False):
            # Read image
            img = cv2.imread(str(img_path))

            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Resize to target dimensions
            img = cv2.resize(img, (img_width, img_height))

            # Normalize pixel values to [0, 1]
            img = img.astype('float32') / 255.0

            images.append(img)
            labels.append(class_to_idx[class_name])

        print(f"")

    # Convert to numpy arrays
    images = np.array(images)
    labels = np.array(labels)

    print(f"\n Dataset loaded successfully!")
    print(f"  Total images: {len(images)}")
    print(f"  Image shape: {images.shape}")
    print(f"  Labels shape: {labels.shape}")
    print(f"  Pixel value range: [{images.min():.2f}, {images.max():.2f}]")

    return images, labels, class_names

def split_dataset(X, y, test_split=0.15, val_split=0.15, random_state=42):
    """
    Split dataset into train, validation, and test sets

    Args:
        X: Images array
        y: Labels array
        test_split: Proportion for test set
        val_split: Proportion for validation set (from remaining data)

    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test
    """

    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y,
        test_size=test_split,
        random_state=random_state,
        stratify=y  # Maintain class distribution
    )

    # Second split: separate validation from training
    val_size_adjusted = val_split / (1 - test_split)  # Adjust proportion
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=val_size_adjusted,
        random_state=random_state,
        stratify=y_temp
    )

    print(" Dataset Split:")
    print("=" * 50)
    print(f"  Training set:   {len(X_train):4d} images ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  Validation set: {len(X_val):4d} images ({len(X_val)/len(X)*100:.1f}%)")
    print(f"  Test set:       {len(X_test):4d} images ({len(X_test)/len(X)*100:.1f}%)")
    print("=" * 50)

    # Check class distribution in each split
    print("\n Class Distribution Check:")
    train_dist = np.bincount(y_train)
    val_dist = np.bincount(y_val)
    test_dist = np.bincount(y_test)

    dist_df = pd.DataFrame({
        'Class': class_names,
        'Train': train_dist,
        'Val': val_dist,
        'Test': test_dist
    })
    print(dist_df.to_string(index=False))

    return X_train, X_val, X_test, y_train, y_val, y_test

