import os
import streamlit as st
import pandas as pd
from PIL import Image
from inference_sdk import InferenceHTTPClient
import base64
from io import BytesIO

api_key = os.getenv("ROBOWFLOW_API_KEY")

# Connect to local Roboflow Inference Server
client = InferenceHTTPClient(
    api_url="http://localhost:9001",  # Running on local machine
    api_key=api_key  # Replace with your actual API key
)

# Directory for saving processed images
OUTPUT_FOLDER = "images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# App Title
st.title("🐟 Pinniped Detection App")

# Upload multiple images
uploaded_files = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# If files are uploaded
if uploaded_files:
    results = []
    progress_bar = st.progress(0)  # Progress bar

    for idx, uploaded_file in enumerate(uploaded_files):
        # Read image
        image = Image.open(uploaded_file)
        image_path = os.path.join(OUTPUT_FOLDER, uploaded_file.name)
        image.save(image_path)

        # Run inference
        result = client.run_workflow(
            workspace_name="pinniped-detection",
            workflow_id="detect-count-and-visualize-pinniped",
            images={"image": image_path}
        )

        # Ensure the response is a list and contains predictions
        if not result or not isinstance(result, list) or "predictions" not in result[0]:
            st.error("⚠️ Error: No predictions found. Check the inference server output.")
        else:
            # Extract detections correctly from the nested JSON
            detections = result[0]["predictions"]["predictions"]  
            pinniped_count = len(detections)
            st.write(f"Pinniped Count: {pinniped_count}")
            output_image_base64 = result[0].get("output_image")

            if output_image_base64:
                output_image_bytes = base64.b64decode(output_image_base64)
                output_image = Image.open(BytesIO(output_image_bytes))
                st.image(output_image, caption="📸 Processed Image with Bounding Boxes")
            else:
                st.error("⚠️ No output image found in the response.")

        results.append({"Image Name": uploaded_file.name, "Pinniped Count": pinniped_count})

        progress_bar.progress((idx + 1) / len(uploaded_files))

    # Display Results in Table
    df = pd.DataFrame(results)
    st.write("### Detection Results", df)

    # Save results as Excel
    excel_path = "pinniped_counts.xlsx"
    df.to_excel(excel_path, index=False)

    # Provide download buttons
    with open(excel_path, "rb") as f:
        st.download_button("📥 Download Excel Results", f, file_name="pinniped_counts.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


