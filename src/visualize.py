import matplotlib.pyplot as plt
import cv2
import numpy as np
from pathlib import Path

def show_samples(dataset_path, num_samples=3):
    """Display sample fingerprint images from each blood group"""

    dataset_path = Path(dataset_path)
    classes = sorted([d.name for d in dataset_path.iterdir() if d.is_dir()])

    # Create subplot grid
    num_classes = len(classes)
    fig, axes = plt.subplots(num_classes, num_samples, figsize=(12, 16))
    fig.suptitle('Sample Fingerprint Images by Blood Group (with Rh Factor)',
                 fontsize=16, fontweight='bold', y=0.995)

    for i, class_name in enumerate(classes):
        class_folder = dataset_path / class_name
        image_files = list(class_folder.glob('*.BMP'))[:num_samples]

        for j, img_path in enumerate(image_files):
            # Read image
            img = cv2.imread(str(img_path))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Display
            axes[i, j].imshow(img, cmap='gray')
            axes[i, j].axis('off')

            # Add title to first column
            if j == 0:
                axes[i, j].set_ylabel(f'{class_name}',
                                     fontweight='bold',
                                     fontsize=11,
                                     rotation=0,
                                     ha='right',
                                     va='center')

    plt.tight_layout()
    plt.show()
    print("Sample visualization complete!")

# Show samples
# show_samples('dataset/dataset_blood_group', num_samples=3)


def analyze_dataset(dataset_path):
    """Complete dataset analysis"""

    dataset_path = Path(dataset_path)
    classes = sorted([d.name for d in dataset_path.iterdir() if d.is_dir()])

    stats = []
    all_sizes = []

    for class_name in classes:
        class_folder = dataset_path / class_name
        image_files = list(class_folder.glob('*.BMP'))

        # Get image dimensions from first image
        if image_files:
            first_img = cv2.imread(str(image_files[0]))
            height, width = first_img.shape[:2]
            all_sizes.append((width, height))

            stats.append({
                'Blood Group': class_name,
                'Images': len(image_files),
                'Percentage': f'{len(image_files)/60:.1f}%',
                'Image Size': f'{width}x{height}'
            })

    df = pd.DataFrame(stats)

    print(" COMPLETE DATASET STATISTICS")
    print("")
    print(df.to_string(index=False))
    print("")

    total_images = df['Images'].sum()
    print(f"\n Summary:")
    print(f"  Total Images: {total_images}")
    print(f"  Number of Classes: {len(classes)}")
    print(f"  Average per class: {total_images/len(classes):.0f} images")

    # Check if all images have same size
    if len(set(all_sizes)) == 1:
        print(f"\n All images have uniform size: {all_sizes[0][0]}x{all_sizes[0][1]}")
    else:
        print(f"\n Images have different sizes - resizing needed")

    # Training split recommendation
    print(f"\n Recommended Data Split:")
    print(f"  Training: {int(total_images * 0.7)} images (70%)")
    print(f"  Validation: {int(total_images * 0.15)} images (15%)")
    print(f"  Testing: {int(total_images * 0.15)} images (15%)")

    return df

# Run analysis
# dataset_stats = analyze_dataset('dataset/dataset_blood_group')

