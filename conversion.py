from tensorflow.keras.models import load_model

# Load your existing .h5 model
model = load_model("final_cnn_model.h5")

# Save in new Keras format
model.save("model.keras")

print("✅ Conversion complete: model.keras created")
