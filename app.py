import streamlit as st
import cv2
import numpy as np
import pandas as pd
from inference_sdk import InferenceHTTPClient
from PIL import Image
import os

# Ensure output directory exists
OUTPUT_DIR = "output_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Resize settings
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

# Function to resize image
def resize_image(image):
    h, w, _ = image.shape
    if w > MAX_WIDTH or h > MAX_HEIGHT:
        scale = min(MAX_WIDTH / w, MAX_HEIGHT / h)
        new_size = (int(w * scale), int(h * scale))
        return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return image

api_key = st.secrets["ROBOWFLOW_API_KEY"]

if api_key:
    print("API key loaded successfully!")
else:
    print("API key not found!")


# Initialize Roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=api_key
)

# Streamlit UI
st.title("🔍 Pinniped Detection")

site = st.text_input("Enter Site:")
date = st.date_input("Select Date:")
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# List to store results
results_data = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Load image
        image = Image.open(uploaded_file)
        image = np.array(image)

        # Resize and compress image
        image = resize_image(image)
        temp_filename = f"temp_{uploaded_file.name}"
        cv2.imwrite(temp_filename, image, [cv2.IMWRITE_JPEG_QUALITY, 80])

        # Run inference
        result = CLIENT.infer(temp_filename, model_id="pinniped-detection/3")
        predictions = result.get("predictions", [])

        # Count objects detected
        object_count = len(predictions)

        # Draw bounding boxes
        for pred in predictions:
            x, y, w, h = int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
            cv2.rectangle(image, (x - w//2, y - h//2), (x + w//2, y + h//2), (0, 255, 0), 3)
            label = f"{pred['class']} ({pred['confidence']:.2f})"
            cv2.putText(image, label, (x - w//2, y - h//2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Save processed image to output folder
        processed_filename = os.path.join(OUTPUT_DIR, f"processed_{uploaded_file.name}")
        cv2.imwrite(processed_filename, image)

        # Convert image back for Streamlit display
        processed_image = Image.fromarray(image)
        st.image(processed_image, caption=f"Processed: {uploaded_file.name} (Detected: {object_count})", use_column_width=True)

        # Store results
        results_data.append({"Image Name": uploaded_file.name, "Object Count": object_count})

        # Remove temp files
        os.remove(temp_filename)

    # Save results to Excel
    results_df = pd.DataFrame(results_data)
    excel_filename = f"{site}_{date}_pinniped_counts.xlsx"
    results_df.to_excel(excel_filename, index=False)

    # Provide download link for results
    with open(excel_filename, "rb") as f:
        st.download_button("📥 Download Results", f, file_name=excel_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Remove Excel file after download link is available
    os.remove(excel_filename)

