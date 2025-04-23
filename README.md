# pinniped-counts
Computer vision project to count number of pinnipeds in each image. An object detection model (YOLOv11) trained on RoboFlow deployed using streamlit - https://app.roboflow.com/pinniped-detection. 
Streamlit app: https://pinniped-counts-psf.streamlit.app/

This Computer Vision model was trained on Roboflow, an interface for CV applications created to ease training and deployment of image models. The images collected from cameras at 3 locations (Nanaimo, Cowichan and Campbell River) were manually annotated on the Roboflow platform, split for training and testing and trained on YOLOv11 – a state-of-the-art object detection algorithm designed for speed, accuracy, and real-time applications. They are known for their efficiency in detecting objects in images in a single forward pass through a neural network.
This refined model has been deployed using Streamlit, an open-source Python framework that enables rapid development of interactive web interfaces. The app calls the roboflow model which has been deployed on the cloud using an API call, each time the app is initiated. The user can upload multiple images, and input the date and location on the app. The app then processes all these images and provides counts of pinnipeds in each image, and stores it in a downloadable excel sheet. 

