# Skill: Create Cloudinary Upload

This skill documents how to integrate image and video uploads using the custom Cloudinary service layer.

## Guidelines

1. **Service Imports**:
   Use the utility uploaders and deleters:
   ```python
   from src.services.cloudinary_service import upload_image, upload_video, delete_image, delete_video
   ```
2. **Uploading Media**:
   - `upload_image(file)` and `upload_video(file)` accept a `fastapi.UploadFile` object.
   - They return a dictionary containing `"public_id"` and `"url"`.
3. **Database Representation**:
   - Save upload keys/URLs to the `Media` model database table:
     ```python
     from src.models.media_model import Media
     ```
   - Store details with `entity_type` (e.g. `"blog"`, `"user_profile"`), `entity_id` (the parent entity UUID), `media_type` (`"image"` or `"video"`), and `provider="cloudinary"`.
4. **Deleting Media**:
   - When modifying/deleting parent entities, delete the corresponding file from Cloudinary first to prevent orphan files:
     ```python
     if old_media.public_id:
         delete_image(old_media.public_id)  # or delete_video for videos
     db.delete(old_media)
     ```

## Code Example

```python
from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.models.media_model import Media
from src.services.cloudinary_service import upload_image

def attach_profile_image(user_id: str, image: UploadFile, db: Session):
    # 1. Upload file to Cloudinary
    result = upload_image(image)
    
    # 2. Persist media record to DB
    media = Media(
        entity_type="user_profile",
        entity_id=user_id,
        media_type="image",
        provider="cloudinary",
        storage_key=result["public_id"],
        public_id=result["public_id"],
        cdn_url=result["url"],
        is_primary=True
    )
    db.add(media)
    db.commit()
    return result["url"]
```
