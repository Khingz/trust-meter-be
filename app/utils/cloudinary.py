from cloudinary.uploader import upload
from fastapi import HTTPException
import cloudinary
from app.utils.settings import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


upload_options = {
   "resource_type": "image",
   "transform": [
         {"width": 800, "height": 800, "crop": "limit"},
         {"quality": "auto"},
   ]
}

allowed_formats = {"image/jpeg", "image/png", "image/jpg"}

def get_image_public_id(image_url: str):
    """Get public id from image url"""
    return image_url.split("/")[-1].split(".")[0]


def upload_image_to_cloudinary(file: bytes, file_type: str, folder: str = None):
    """Upload image to cloudinary"""
    if file_type not in allowed_formats:
        raise HTTPException(status_code=400, detail="Invalid file format, Allowed types: jpeg, jpg, png")
    if folder:
        upload_options["folder"] = folder
    try:
        response = upload(file, **upload_options)
        return response["secure_url"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))