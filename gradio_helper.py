import os
import shutil
from gradio_client import Client
from typing import Dict

# Function to interact with Gradio
def predict_background_removal(image_url: str, coordinates: Dict) -> bytes:
    client = Client("Saarthak2002/bg_removal")
    result = client.predict(
        image_url=image_url,
        x_min=coordinates['x_min'],
        y_min=coordinates['y_min'],
        x_max=coordinates['x_max'],
        y_max=coordinates['y_max'],
        api_name="/predict"
    )
    
    # Debugging: Check the type and value of the result
    print("Result Type:", type(result))
    print("Result:", result)

    # Ensure the directory for saving images exists
    output_dir = "processed_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    processed_image_path = os.path.join(output_dir, "processed_image.png")

    if isinstance(result, bytes):
        # Save the result as an image file if it's already in bytes
        with open(processed_image_path, "wb") as f:
            f.write(result)
    elif isinstance(result, str):
        # If the result is a file path, copy the file and read it as bytes
        if os.path.isfile(result):
            shutil.copy(result, processed_image_path)
        else:
            raise ValueError(f"Result file path is invalid: {result}")
    else:
        raise ValueError("Unexpected result type from Gradio API.")

    # Read and return the image in bytes
    with open(processed_image_path, "rb") as f:
        image_bytes = f.read()

    return image_bytes
