import cloudinary.uploader  # type: ignore
from fastapi import UploadFile, HTTPException #type:ignore


def upload_image(
    file: UploadFile,
    public_id: str | None = None
) -> dict:
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder="axon/images",
            public_id=public_id,
            overwrite=True,
        )

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary upload failed: {str(e)}"
        )


def upload_video(
    file: UploadFile,
    public_id: str | None = None
) -> dict:
    try:
        result = cloudinary.uploader.upload(
            file.file,
            resource_type="video",
            folder="axon/videos",
            public_id=public_id,
            overwrite=True,
        )

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary video upload failed: {str(e)}"
        )
    
    
def delete_image(public_id: str) -> bool:
    try:
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type="image"
        )

        return result.get("result") == "ok"

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary delete failed: {str(e)}"
        )
        
def delete_video(public_id: str) -> bool:
    try:
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type="video"
        )

        return result.get("result") == "ok"

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary video delete failed: {str(e)}"
        )