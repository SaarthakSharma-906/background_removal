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

app = FastAPI()

# AWS S3 setup
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAXNGUU7TZRV7GFHXF',  # Replace with your AWS access key
    aws_secret_access_key='uSmB5V33KeR+YirEi/cxYZGe9zHsee/UBhUoSPKR',  # Replace with your AWS secret key
    region_name='ap-south-1'  # Use correct AWS region
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
        print("Received request:", request)  # Log the incoming request data

        image_url = request.image_url
        bounding_box = request.bounding_box.dict()

        # Fetch the image to validate bounding box dimensions
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch or process the image from URL: {str(e)}")

        image_width, image_height = image.size

        # Validate bounding box dimensions
        x_min, y_min, x_max, y_max = (
            bounding_box["x_min"],
            bounding_box["y_min"],
            bounding_box["x_max"],
            bounding_box["y_max"],
        )

        if x_min < 0 or y_min < 0 or x_max > image_width or y_max > image_height:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Bounding box coordinates are out of image bounds. "
                    f"Image size: {image_width}x{image_height}, "
                    f"Provided bounding box: x_min={x_min}, y_min={y_min}, x_max={x_max}, y_max={y_max}"
                )
            )

        if x_min >= x_max or y_min >= y_max:
            raise HTTPException(
                status_code=400,
                detail="Invalid bounding box: x_min must be less than x_max and y_min must be less than y_max."
            )

        # Call the Gradio helper function to perform background removal
        processed_image = predict_background_removal(image_url, bounding_box)

        # Upload the processed image to AWS S3
        output_filename = "processed_image.png"
        try:
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=output_filename,
                Body=processed_image,
                ContentType='image/png',
                ACL='public-read'  # Make the file publicly accessible
            )
            # Use the correct region URL
            processed_image_url = f"https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{output_filename}"
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="AWS credentials are not available")

        return {
            "original_image_url": image_url,
            "processed_image_url": processed_image_url
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
