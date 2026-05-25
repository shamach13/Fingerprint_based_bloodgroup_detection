import numpy as np
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
from tensorflow.keras.models import load_model


app = FastAPI()

model = load_model("final_cnn_model.keras")

# Get input shape from model
_, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS = model.input_shape

print("Model expects:", model.input_shape)

# SAME order as training (VERY IMPORTANT)
class_names = [
    "A+", "A-", "AB+", "AB-",
    "B+", "B-", "O+", "O-"
]

@app.get("/")
def home():
    return {"message": "Blood Group Prediction API running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    try:
        # Read image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        if IMG_CHANNELS == 3:
            image = image.convert("RGB")
        else:
            image = image.convert("L")

        # Resize EXACTLY as model expects
        image = image.resize((IMG_WIDTH, IMG_HEIGHT))

        # Convert to numpy
        image = np.array(image) / 255.0

        # If grayscale → add channel dim
        if IMG_CHANNELS == 1:
            image = np.expand_dims(image, axis=-1)

        # Add batch dimension
        image = np.expand_dims(image, axis=0)

        predictions = model.predict(image, verbose=0)

        predicted_index = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))

        predicted_label = class_names[predicted_index]

        # Top 3 predictions
        top3_idx = np.argsort(predictions[0])[-3:][::-1]
        top3 = [
            {
                "label": class_names[i],
                "confidence": float(predictions[0][i])
            }
            for i in top3_idx
        ]

        return {
            "prediction": predicted_label,
            "confidence": confidence,
            "top_3_predictions": top3
        }

    except Exception as e:
        return {"error": str(e)}
