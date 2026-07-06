from fastapi import APIRouter, Depends, Request, UploadFile, File, Form #type: ignore
from sqlalchemy.orm import Session #type: ignore
from src.core.db import get_db
from src.utils.rate_limiting import limiter
from src.modules.blogs.schemas import BlogUpsertSchema
from src.modules.blogs.service import (
    get_all_categories,
    upsert_blog_service,
    delete_blog_by_id,
    get_blogs_by_category
)

router = APIRouter()

@router.get("/categories")
@limiter.limit("50/minute")
async def get_blog_categories(request: Request, db: Session = Depends(get_db)):
    return get_all_categories(db)

@router.post("/upsert")
@limiter.limit("5/minute")
async def upsert_blog(
    request: Request,
    id: str | None = Form(None),
    created_by: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    category_id: str = Form(...),
    excerpt: str | None = Form(None),
    is_published: bool = Form(False),
    image: UploadFile | None = File(None),
    video: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    body = BlogUpsertSchema(
        id=id,
        created_by=created_by,
        title=title,
        content=content,
        category_id=category_id,
        excerpt=excerpt,
        is_published=is_published
    )
    return upsert_blog_service(body=body, image=image, video=video, db=db)

@router.delete("/{id}")
@limiter.limit("20/minute")
async def delete_blog(request: Request, id: str, db: Session = Depends(get_db)):
    return delete_blog_by_id(id, db)

@router.get("/list/{category}")
@limiter.limit("50/minute")
async def list_blogs_by_category(request: Request, category: str, db: Session = Depends(get_db)):
    return get_blogs_by_category(category, db)
