# Documentation

## Objective
The objective of this project was to develop a computer vision model capable of detecting and counting pinnipeds (seals, sea lions, and walruses) in a series of images. The final output is presented as an Excel file that includes the count of detected pinnipeds, the date of upload, and the associated location for each set of images.

## Data
1. Source: The dataset consists of 146 manually annotated images collected from various locations (Nanaimo, Cowichan and Campbell). These include both populated and null images (images with no pinnipeds).
2. Annotations: A total of 229 bounding box annotations were made, with multiple pinnipeds present in several images.
3. Split: The dataset was split into: 70% Training, 20% Validation, 10% Testing
4. Preprocessing: Images were preprocessed using grayscale conversion, rotation, and other augmentation techniques to enhance generalization. After preprocessing and augmentation, the total number of images increased to 356.

## Methods and Tools
1. Annotation Tool: Roboflow was used for manual annotation of the images.
2. Model Architecture: YOLOv11 (You Only Look Once) was selected for its speed and accuracy in object detection tasks.
3. Training: The model was trained using Roboflow’s integrated training pipeline, benefiting from its augmentation and dataset management features.

 ## Evaluation Metrics:
 
 1. Precision: 76% - Precision measures how many of the detected objects were correct (i.e., true positives out of all detected positives)
 2. Recall: 63.6% - Recall measures how many of the actual pinnipeds were detected (i.e., true positives out of all actual positives).
 3. mAP@50 (Mean Average Precision at IoU threshold 0.5): 73.5% - mAP@50 is a common benchmark in object detection, evaluating the balance between precision and recall across all classes. A score above 70% is generally considered strong in real-world applications.

## Deployment
The trained model was deployed using Streamlit, enabling a user-friendly web interface. Users can upload multiple images through the app.
The model processes each image and returns:

1. The count of detected pinnipeds

2. The date and time of upload

3. The location 

Results are exported to an Excel file for further analysis or reporting.

## Model Robustness and Generalization
Overfitting Avoidance: Use of data augmentation (e.g., rotations, grayscale) increased training variety and improved generalization. Inclusion of null images helped reduce false positives and improve robustness to empty scenes. The model demonstrated consistent performance across diverse image sets, indicating good generalization without overfitting.

## Notes
With further data and refinement, this pipeline can be extended to other marine wildlife monitoring tasks or integrated into broader ecological studies.
