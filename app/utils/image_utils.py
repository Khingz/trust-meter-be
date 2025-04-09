from io import BytesIO
import requests
import magic
from app.utils.cloudinary import upload_image_to_cloudinary

def convert_image_to_bytes(image_url: str):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(image_data.read())
        # Reset pointer to start from the begining of byte 
        image_data.seek(0)
        return image_data, mime_type
    else:
        raise ValueError(f"Failed to download image from {image_url}")
def handle_image_upload(image_url):
    """ Handle image download and upload to cloud service"""
    image_data, mime_type = convert_image_to_bytes(image_url)
    print(image_data)
    img_url = upload_image_to_cloudinary(image_data, mime_type)
    return img_url  