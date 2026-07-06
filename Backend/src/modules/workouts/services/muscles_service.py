from src.modules.media.service import delete_image, upload_image, upload_video, delete_video
from src.modules.workouts.schemas.muscle_schema import UpsertMuscleGroup, upsertExcercise
from sqlalchemy.orm import Session #type:ignore
from src.modules.workouts.models.muscle_group import MuscleGroup
from src.modules.workouts.models.exercise import Exercise
from src.modules.media.models import Media
from src.utils.response import Response
from fastapi import HTTPException, UploadFile #type: ignore

# Helper methods ----------------------------------------------------------
def _make_slug(name: str) -> str:
    """'Chest' → 'chest_icon_image'"""
    return f"{name.strip().lower().replace(' ', '_')}_icon_image"


# main functions ----------------------------------------------------------
def add_or_update_muscle(body: UpsertMuscleGroup,image: UploadFile | None,db: Session):
    # UPDATE
    if body.id:
        muscle = (db.query(MuscleGroup).filter(MuscleGroup.id == body.id).first())
        if not muscle:
            raise HTTPException(
                status_code=404,
                detail="Muscle group not found"
            )

        if body.name:
            muscle.name = body.name
            muscle.slug = _make_slug(body.name)

        if image:
            # Delete previous image
            if muscle.icon_public_id:
                delete_image(muscle.icon_public_id)

            upload_result = upload_image(
                image,
                public_id=muscle.slug
            )

            muscle.icon_url = upload_result["url"]
            muscle.icon_public_id = upload_result["public_id"]

        db.commit()
        db.refresh(muscle)
        return muscle

    # CREATE
    slug = _make_slug(body.name)

    upload_result = None
    if image:
        upload_result = upload_image(
            image,
            public_id=slug
        )

    muscle = MuscleGroup(
        name=body.name,
        slug=slug,
        icon_url=upload_result["url"] if upload_result else None,
        icon_public_id=upload_result["public_id"] if upload_result else None,
    )

    db.add(muscle)
    db.commit()
    db.refresh(muscle)

    return muscle

def delete_musclegroup_by_id(id: str, db: Session):
    muscle = (
        db.query(MuscleGroup)
        .filter(MuscleGroup.id == id)
        .first()
    )

    if not muscle:
        raise HTTPException(
            status_code=404,
            detail="Muscle group not found"
        )

    # Delete image from Cloudinary
    if muscle.icon_public_id:
        delete_image(muscle.icon_public_id)

    # Delete record from DB
    db.delete(muscle)
    db.commit()

    return {"message": "Muscle group deleted successfully"}

def add_or_update_excercise(body: upsertExcercise,image,video,db: Session):
    # UPDATE
    if body.id:
        exercise = (
            db.query(Exercise)
            .filter(Exercise.id == body.id)
            .first()
        )

        if not exercise:
            raise HTTPException(
                status_code=404,
                detail="Exercise not found"
            )

        exercise.name = body.name
        exercise.description = body.description
        exercise.category = body.category
        exercise.muscle_group_id = body.muscle_group_id

        # Replace image
        if image:
            old_image = (
                db.query(Media)
                .filter(
                    Media.entity_type == "exercise",
                    Media.entity_id == exercise.id,
                    Media.media_type == "image",
                )
                .first()
            )

            if old_image:
                delete_image(old_image.public_id)
                db.delete(old_image)

            result = upload_image(image)

            db.add(
                Media(
                    entity_type="exercise",
                    entity_id=exercise.id,
                    media_type="image",
                    provider="cloudinary",
                    storage_key=result["public_id"],
                    public_id=result["public_id"],
                    cdn_url=result["url"],
                    is_primary=True,
                )
            )

        # Replace video
        if video:
            old_video = (
                db.query(Media)
                .filter(
                    Media.entity_type == "exercise",
                    Media.entity_id == exercise.id,
                    Media.media_type == "video",
                )
                .first()
            )

            if old_video:
                delete_video(old_video.public_id)
                db.delete(old_video)

            result = upload_video(video)

            db.add(
                Media(
                    entity_type="exercise",
                    entity_id=exercise.id,
                    media_type="video",
                    provider="cloudinary",
                    storage_key=result["public_id"],
                    public_id=result["public_id"],
                    cdn_url=result["url"],
                    is_primary=True,
                )
            )

        db.commit()
        db.refresh(exercise)
        return exercise

    # CREATE
    exercise = Exercise(
        name=body.name,
        description=body.description,
        category=body.category,
        muscle_group_id=body.muscle_group_id,
        created_by=body.created_by,
    )

    db.add(exercise)
    db.flush()  # get exercise.id

    if image:
        result = upload_image(image)

        db.add(
            Media(
                entity_type="exercise",
                entity_id=exercise.id,
                media_type="image",
                provider="cloudinary",
                storage_key=result["public_id"],
                public_id=result["public_id"],
                cdn_url=result["url"],
                is_primary=True,
            )
        )

    if video:
        result = upload_video(video)

        db.add(
            Media(
                entity_type="exercise",
                entity_id=exercise.id,
                media_type="video",
                provider="cloudinary",
                storage_key=result["public_id"],
                public_id=result["public_id"],
                cdn_url=result["url"],
                is_primary=True,
            )
        )

    db.commit()
    db.refresh(exercise)

    return exercise

def delete_excercise_by_id(id: str, db: Session):
    exercise = (
        db.query(Exercise)
        .filter(Exercise.id == id)
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    media_items = (
        db.query(Media)
        .filter(
            Media.entity_type == "exercise",
            Media.entity_id == id,
        )
        .all()
    )

    for media in media_items:
        if media.public_id:
            if media.media_type == "image":
                delete_image(media.public_id)
            else:
                delete_video(media.public_id)

        db.delete(media)

    db.delete(exercise)
    db.commit()

    return {"message": "Exercise deleted successfully"}

def get_all_musclegroups(db: Session):
    muscles = db.query(MuscleGroup).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "image": m.icon_url
        }
        for m in muscles
    ]

def get_musclegroup_by_id(id: str, db: Session):
    muscle = db.query(MuscleGroup).filter(MuscleGroup.id == id).first()
    if not muscle:
        raise HTTPException(status_code=404, detail="Muscle group not found")
    return {
        "id": muscle.id,
        "name": muscle.name,
        "image": muscle.icon_url
    }

def get_all_exercises_by_muscle_group(muscle_group_id: str, db: Session):
    exercises = db.query(Exercise).filter(Exercise.muscle_group_id == muscle_group_id).all()
    result = []
    for ex in exercises:
        image_url = None
        video_url = None
        for m in ex.media:
            if m.media_type == "image":
                image_url = m.cdn_url
            elif m.media_type == "video":
                video_url = m.cdn_url
                
        result.append({
            "id": ex.id,
            "name": ex.name,
            "image": image_url,
            "video": video_url,
            "muscle_group_name": ex.muscle_group.name if ex.muscle_group else None,
            "description": ex.description,
            "category": ex.category
        })
    return result

def get_exercise_by_id(id: str, db: Session):
    ex = db.query(Exercise).filter(Exercise.id == id).first()
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
        
    image_url = None
    video_url = None
    for m in ex.media:
        if m.media_type == "image":
            image_url = m.cdn_url
        elif m.media_type == "video":
            video_url = m.cdn_url
            
    return {
        "id": ex.id,
        "name": ex.name,
        "image": image_url,
        "video": video_url,
        "muscle_group_name": ex.muscle_group.name if ex.muscle_group else None,
        "description": ex.description,
        "category": ex.category
    }