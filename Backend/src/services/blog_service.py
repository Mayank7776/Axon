import re
from fastapi import HTTPException, UploadFile #type: ignore
from sqlalchemy.orm import Session #type: ignore
from src.models.health_blog import Blog
from src.models.category import BlogCategory
from src.models.media_model import Media
from src.schemas.blog_schema import BlogUpsertSchema
from src.services.cloudinary_service import upload_image, upload_video, delete_image, delete_video

def get_all_categories(db: Session):
    categories = db.query(BlogCategory).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug
        }
        for c in categories
    ]

def _slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s.strip('-')

def _generate_unique_slug(title: str, db: Session, current_blog_id: str | None = None) -> str:
    base_slug = _slugify(title)
    if not base_slug:
        base_slug = "post"
    
    slug = base_slug
    counter = 1
    while True:
        query = db.query(Blog).filter(Blog.slug == slug)
        if current_blog_id:
            query = query.filter(Blog.id != current_blog_id)
        existing = query.first()
        if not existing:
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1

def upsert_blog_service(
    body: BlogUpsertSchema,
    image: UploadFile | None,
    video: UploadFile | None,
    db: Session
):
    # Validate category exists
    category = db.query(BlogCategory).filter(BlogCategory.id == body.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")

    # UPDATE
    if body.id:
        blog = db.query(Blog).filter(Blog.id == body.id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        blog.title = body.title
        blog.content = body.content
        blog.category_id = body.category_id
        blog.excerpt = body.excerpt
        blog.is_published = body.is_published
        blog.slug = _generate_unique_slug(body.title, db, current_blog_id=blog.id)

        # Replace image if a new one is uploaded
        if image:
            old_image = (
                db.query(Media)
                .filter(
                    Media.entity_type == "blog",
                    Media.entity_id == blog.id,
                    Media.media_type == "image",
                )
                .first()
            )
            if old_image:
                if old_image.public_id:
                    delete_image(old_image.public_id)
                db.delete(old_image)

            result = upload_image(image)
            db.add(
                Media(
                    entity_type="blog",
                    entity_id=blog.id,
                    media_type="image",
                    provider="cloudinary",
                    storage_key=result["public_id"],
                    public_id=result["public_id"],
                    cdn_url=result["url"],
                    is_primary=True,
                )
            )

        # Replace video if a new one is uploaded
        if video:
            old_video = (
                db.query(Media)
                .filter(
                    Media.entity_type == "blog",
                    Media.entity_id == blog.id,
                    Media.media_type == "video",
                )
                .first()
            )
            if old_video:
                if old_video.public_id:
                    delete_video(old_video.public_id)
                db.delete(old_video)

            result = upload_video(video)
            db.add(
                Media(
                    entity_type="blog",
                    entity_id=blog.id,
                    media_type="video",
                    provider="cloudinary",
                    storage_key=result["public_id"],
                    public_id=result["public_id"],
                    cdn_url=result["url"],
                    is_primary=True,
                )
            )

        db.commit()
        db.refresh(blog)
        return blog

    # CREATE
    if not image:
        raise HTTPException(status_code=400, detail="Image is compulsory for new blogs")

    slug = _generate_unique_slug(body.title, db)

    blog = Blog(
        created_by=body.created_by,
        title=body.title,
        slug=slug,
        content=body.content,
        category_id=body.category_id,
        excerpt=body.excerpt,
        is_published=body.is_published,
    )
    db.add(blog)
    db.flush()  # to obtain blog.id

    # Upload and assign image
    image_result = upload_image(image)
    db.add(
        Media(
            entity_type="blog",
            entity_id=blog.id,
            media_type="image",
            provider="cloudinary",
            storage_key=image_result["public_id"],
            public_id=image_result["public_id"],
            cdn_url=image_result["url"],
            is_primary=True,
        )
    )

    # Upload and assign video (optional)
    if video:
        video_result = upload_video(video)
        db.add(
            Media(
                entity_type="blog",
                entity_id=blog.id,
                media_type="video",
                provider="cloudinary",
                storage_key=video_result["public_id"],
                public_id=video_result["public_id"],
                cdn_url=video_result["url"],
                is_primary=True,
            )
        )

    db.commit()
    db.refresh(blog)
    return blog

def delete_blog_by_id(id: str, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    media_items = db.query(Media).filter(Media.entity_type == "blog", Media.entity_id == id).all()
    for m in media_items:
        if m.public_id:
            if m.media_type == "image":
                delete_image(m.public_id)
            else:
                delete_video(m.public_id)
        db.delete(m)

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}

def get_blogs_by_category(category_filter: str, db: Session):
    query = db.query(Blog)
    if category_filter.lower() != "all":
        query = query.join(BlogCategory).filter(BlogCategory.slug == category_filter.lower())
    
    blogs = query.all()
    
    result = []
    for blog in blogs:
        image_url = None
        video_url = None
        for m in blog.media:
            if m.media_type == "image":
                image_url = m.cdn_url
            elif m.media_type == "video":
                video_url = m.cdn_url

        result.append({
            "id": blog.id,
            "created_by": blog.created_by,
            "title": blog.title,
            "slug": blog.slug,
            "excerpt": blog.excerpt,
            "content": blog.content,
            "category_id": blog.category_id,
            "category": {
                "id": blog.category.id,
                "name": blog.category.name,
                "slug": blog.category.slug
            } if blog.category else None,
            "is_published": blog.is_published,
            "created_at": blog.created_at.isoformat() if blog.created_at else None,
            "updated_at": blog.updated_at.isoformat() if blog.updated_at else None,
            "image": image_url,
            "video": video_url
        })
    return result
