# Background Removal API Project

## Overview
This project provides a web-based API for removing the background from images using specified bounding box coordinates. It leverages machine learning models through the Gradio interface and integrates with AWS S3 for storing and sharing processed images.

## Features
- **FastAPI**-based RESTful API.
- Gradio-based background removal model.
- AWS S3 integration for processed image storage.
- Bounding box customization for precise background removal.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd background_removal-main
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

## Tools, Frameworks, and Libraries Used
- **FastAPI**: Framework for building fast and efficient APIs with Python.
- **Uvicorn**: Lightning-fast ASGI server for serving the FastAPI application.
- **Gradio**: Interactive UI framework for building machine learning demos and applications.
- **AWS S3**: Cloud storage service for storing processed images.
- **Requests**: Python library for making HTTP requests to fetch and send data.
- **Pillow**: Imaging library for basic image processing tasks.
- **OpenCV**: Advanced image manipulation and computer vision.
- **NumPy**: Numerical computations for handling image arrays.

## API Endpoints

### 1. Root Endpoint
**GET** `/`
- Returns a welcome message.

### 2. Background Removal Endpoint
**POST** `/remove_background`
- **Description**: Removes the background from an image using bounding box coordinates.
- **Request Body** (JSON):
  ```json
  {
    "image_url": "http://example.com/image.jpg",
    "bounding_box": {
      "x_min": 50,
      "y_min": 50,
      "x_max": 200,
      "y_max": 200
    }
  }
  ```
- **Response** (JSON):
  ```json
  {
    "original_image_url": "http://example.com/image.jpg",
    "processed_image_url": "https://processedimg.s3.ap-south-1.amazonaws.com/processed_image.png"
  }
  ```

## Postman Collection
To test the API endpoints, a Postman collection is included in the repository:
1. Import the Postman collection JSON file into Postman.
2. Update the environment variables (if any) such as `BASE_URL` to point to your running API server eg http://127.0.0.1:8000
3. Use the predefined requests to test the API.

### Running the Postman Collection
1. Open Postman and navigate to the collection.
2. Run the `Background Removal` request under the collection.
3. Verify the responses for successful background removal and AWS S3 image URL.

## Project Structure
- **`main.py`**: Entry point for the FastAPI application, containing API endpoints.
- **`gradio_helper.py`**: Helper functions for interacting with the Gradio-based model.
- **`requirements.txt`**: Python dependencies.
- **`__init__.py`**: Package initializer.
- **`README.md`**: Project documentation.
- **`postman_collection.json`**: Postman collection file for testing API endpoints.

## Dependencies
- **FastAPI**: Framework for building APIs.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **Requests**: HTTP library for downloading images.
- **Pillow**: Python Imaging Library for image processing.
- **NumPy**: Array manipulations for image data.
- **OpenCV**: Advanced image processing.
- **Mask R-CNN ResNet50 FPN**: Object segmentation model for background removal.
- **Hugging Face Space**: Platform for running and sharing machine learning models, ensuring the background removal model is available continuously.
- **AWS S3**: Cloud storage service for storing processed images.

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Usage Guide
1. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

2. Send a POST request to `/remove_background` with a JSON body containing the image URL and bounding box coordinates.

3. Retrieve the processed image URL from the API response.




## Contact
For inquiries or support, please contact Saarthak Sharma, Raj Krishna , Naman Gupta and Sanskriti Goyal at 21ume043@lnmiit.ac.in.
