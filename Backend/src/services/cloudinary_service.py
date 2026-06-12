import cloudinary.uploader #type: ignore

def upload_image(file):
    result = cloudinary.uploader.upload(
        file.file,
        folder="axon/images"
    )

    return result["secure_url"]

def upload_video(file):
    result = cloudinary.uploader.upload(
        file.file,
        resource_type="video",
        folder="axon/videos"
    )

    return result["secure_url"]