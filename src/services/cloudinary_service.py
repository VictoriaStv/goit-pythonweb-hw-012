import cloudinary
import cloudinary.uploader
from src.conf.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_avatar(file, public_id: str):
    result = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
    return result.get("secure_url")
