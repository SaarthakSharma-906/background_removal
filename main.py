from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gradio_helper import predict_background_removal
from typing import Dict
import os
import requests
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# AWS S3 setup using environment variables
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'ap-south-1')  # Default region if not provided
)

BUCKET_NAME = 'processedimg'  # Replace with your S3 bucket name

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Background Remover API!"}

class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int

class ImageRequest(BaseModel):
    image_url: str
    bounding_box: BoundingBox

@app.post("/remove_background")
async def remove_background_from_image(request: ImageRequest):
    try:
        image_url = request.image_url
        bounding_box = request.bounding_box.dict()

        # Fetch and validate the image
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        image_width, image_height = image.size
        x_min, y_min, x_max, y_max = (
            bounding_box["x_min"],
            bounding_box["y_min"],
            bounding_box["x_max"],
            bounding_box["y_max"],
        )

        if x_min < 0 or y_min < 0 or x_max > image_width or y_max > image_height:
            raise HTTPException(
                status_code=400,
                detail=f"Bounding box is out of bounds for image size {image_width}x{image_height}."
            )

        # Call the Gradio helper function
        processed_image = predict_background_removal(image_url, bounding_box)

        # Upload to S3
        output_filename = "processed_image.png"
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=output_filename,
            Body=processed_image,
            ContentType='image/png',
            ACL='public-read'
        )

        processed_image_url = f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{output_filename}"
        return {
            "original_image_url": image_url,
            "processed_image_url": processed_image_url
        }

    except HTTPException as http_exc:
        raise http_exc
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials are not available.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
