from tensorflow.keras.preprocessing.image import ImageDataGenerator

def data_augmentation():
    # Create data augmentation generator for training
    train_datagen = ImageDataGenerator(
        rotation_range=20,  # Rotate images up to 20 degrees
        width_shift_range=0.1,  # Shift images horizontally
        height_shift_range=0.1,  # Shift images vertically
        shear_range=0.1,  # Shear transformation
        zoom_range=0.1,  # Zoom in/out
        horizontal_flip=True,  # Random horizontal flip
        fill_mode='nearest'  # Fill missing pixels
    )

    # No augmentation for validation/test (only rescaling already done)
    val_datagen = ImageDataGenerator()
    test_datagen = ImageDataGenerator()

    print(" Data Augmentation Configured:")
    print("   Training: Augmentation enabled")
    print("   Validation: No augmentation")
    print("   Test: No augmentation")
    print("\nAugmentation techniques:")
    print("  - Rotation (±20°)")
    print("  - Width/Height shift (10%)")
    print("  - Shear transformation")
    print("  - Zoom (±10%)")
    print("  - Horizontal flip")

    return train_datagen, val_datagen, test_datagen