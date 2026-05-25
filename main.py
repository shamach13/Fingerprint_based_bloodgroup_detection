import numpy as np
import tensorflow as tf

# Dataset Configuration
DATASET_PATH = 'dataset/dataset_blood_group'
IMG_HEIGHT = 96
IMG_WIDTH = 96  # We'll resize to square for easier processing
IMG_CHANNELS = 3

# Training Configuration
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.15
TEST_SPLIT = 0.15

# Model Configuration
NUM_CLASSES = 8  # A+, A-, B+, B-, AB+, AB-, O+, O-
CLASS_NAMES = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']

# Random Seed for Reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

print(" Configuration Set:")
print(f"  Image Size: {IMG_WIDTH}x{IMG_HEIGHT}x{IMG_CHANNELS}")
print(f"  Batch Size: {BATCH_SIZE}")
print(f"  Epochs: {EPOCHS}")
print(f"  Classes: {NUM_CLASSES}")
print(f"  Validation Split: {VALIDATION_SPLIT * 100}%")
print(f"  Test Split: {TEST_SPLIT * 100}%")