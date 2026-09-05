import os
import uuid
import aioboto3
import logging
from fastapi import UploadFile, HTTPException

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ENDPOINT_URL_S3 = os.getenv("AWS_ENDPOINT_URL_S3")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "auto")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Public domain to access files (e.g. Cloudflare custom domain or public bucket URL)
PUBLIC_FILE_URL = os.getenv("PUBLIC_FILE_URL", "")

async def save_upload_file(upload_file: UploadFile, dest_folder: str = "uploads") -> str:
    if not upload_file or not upload_file.filename:
        return None
    
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if upload_file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Faqat rasm yoki PDF fayllarga ruxsat berilgan")
    
    content = await upload_file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fayl hajmi 5 MB dan oshmasligi kerak")
    
    ext = os.path.splitext(upload_file.filename)[1].lower()
    allowed_exts = ['.jpg', '.jpeg', '.png', '.pdf']
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail="Noto'g'ri fayl formati")
        
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_key = f"{dest_folder}/{unique_name}"
    
    # If S3 credentials exist, upload to S3 (Cloudflare R2)
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_ENDPOINT_URL_S3 and AWS_BUCKET_NAME:
        try:
            session = aioboto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION_NAME
            )
            async with session.client("s3", endpoint_url=AWS_ENDPOINT_URL_S3) as s3:
                await s3.put_object(
                    Bucket=AWS_BUCKET_NAME,
                    Key=file_key,
                    Body=content,
                    ContentType=upload_file.content_type
                )
            # Return absolute URL if PUBLIC_FILE_URL is set, else return key
            if PUBLIC_FILE_URL:
                return f"{PUBLIC_FILE_URL.rstrip('/')}/{file_key}"
            return file_key
        except Exception as e:
            logging.error(f"S3 ga yuklashda xatolik: {e}")
            raise HTTPException(status_code=500, detail="Faylni serverga yuklashda xatolik yuz berdi")
    else:
        # Fallback to local storage
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        file_path = os.path.join(dest_folder, unique_name)
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path.replace("\\", "/")
