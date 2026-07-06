from src.modules.workouts.services.muscles_service import (
    add_or_update_excercise,
    add_or_update_muscle,
    delete_excercise_by_id,
    delete_musclegroup_by_id,
    get_all_musclegroups,
    get_musclegroup_by_id,
    get_all_exercises_by_muscle_group,
    get_exercise_by_id,
)
from fastapi import APIRouter, Depends, Request, UploadFile, File, Form #type: ignore
from sqlalchemy.orm import Session #type:ignore
from src.core.db import get_db
from src.utils.rate_limiting import limiter
from src.modules.workouts.schemas.muscle_schema import UpsertMuscleGroup, upsertExcercise

router = APIRouter()

@router.get("/get-musclegroup")
@limiter.limit("50/minute")
async def get_all_musclegroup(request: Request, db: Session = Depends(get_db)):
    return get_all_musclegroups(db)

@router.get("/get-musclegroup/{id}")
@limiter.limit("50/minute")
async def get_musclegroup(request: Request, id: str, db: Session = Depends(get_db)):
    return get_musclegroup_by_id(id, db)

@router.post("/upsert-musclegroup")
@limiter.limit("5/minute")
async def upsert_musclegroup(
    request: Request,
    id: str | None = Form(None),
    name: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session=Depends(get_db),
):
    body = UpsertMuscleGroup(id=id, name=name)

    return add_or_update_muscle(
        body=body,
        image=image,
        db=db
    )

@router.post("/delete-musclegroup/{id}")
@limiter.limit("20/minute")
async def delete_musclegroup(request: Request, id: str, db: Session = Depends(get_db)):
    return delete_musclegroup_by_id(id, db)


@router.get("/get-all-excercise")
@limiter.limit("50/minute")
async def get_all_excercise(request: Request, id: str, db: Session = Depends(get_db)):
    return get_all_exercises_by_muscle_group(id, db)

@router.get("/get-excercise/{id}")
@limiter.limit("50/minute")
async def get_excercise(request: Request, id: str, db: Session = Depends(get_db)):
    return get_exercise_by_id(id, db)

@router.post("/upsert-excercise")
@limiter.limit("5/minute")
async def upsert_excericse(
    request: Request,
    id: str | None = Form(None),
    muscle_group_id: str = Form(...),
    created_by: str | None = Form(None),
    name: str = Form(...),
    description: str | None = Form(None),
    category: str = Form(...),
    image: UploadFile | None = File(None),
    video: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    model = upsertExcercise(
        id=id,
        muscle_group_id=muscle_group_id,
        created_by=created_by,
        name=name,
        description=description,
        category=category,
    )

    return add_or_update_excercise(
        body=model,
        image=image,
        video=video,
        db=db,
    )

@router.post("/delete-excercise/{id}")
@limiter.limit("20/minute")
async def delete_excercise(request: Request, id: str, db: Session = Depends(get_db)):
    return delete_excercise_by_id(id, db)

