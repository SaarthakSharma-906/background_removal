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

## Project Structure
- **`main.py`**: Entry point for the FastAPI application, containing API endpoints.
- **`gradio_helper.py`**: Helper functions for interacting with the Gradio-based model.
- **`requirements.txt`**: Python dependencies.
- **`__init__.py`**: Package initializer.
- **`README.md`**: Project documentation.

## Dependencies
- **FastAPI**: Framework for building APIs.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **Requests**: HTTP library for downloading images.
- **Pillow**: Python Imaging Library for image processing.
- **NumPy**: Numerical computations.
- **OpenCV**: Advanced image processing.

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

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Contributions
Contributions are welcome! Please open an issue or submit a pull request for any suggestions or fixes.

## Contact
For inquiries or support, please contact [Your Name] at [Your Email].
