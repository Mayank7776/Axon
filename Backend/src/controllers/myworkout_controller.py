from fastapi import APIRouter, Request, Depends #type: ignore
from sqlalchemy.orm import Session #type:ignore
from src.utils.rate_limiting import limiter
from src.core.db import get_db
from src.services.myworkout_service import *
from src.schemas.myworkout_schema import UpsertWorkoutPlanMetadata, UpsertWorkoutDay, SaveAIWorkoutPlanPayload

router = APIRouter()

@router.get("/all-plan")
@limiter.limit("20/minute")
async def get_all_myworkout_plan(request: Request, user_id: str, db: Session = Depends(get_db)):
    return get_all_workout_plans(user_id, db)

@router.get("/plan/{id}")
@limiter.limit("20/minute")
async def get_myworkout_plan(request: Request, id: str, db: Session = Depends(get_db)):
    return get_workout_plan_by_id(id, db)

@router.post("/upsert-plan")
@limiter.limit("20/minute")
async def upsert_myworkout_plan(request: Request, body: UpsertWorkoutPlanMetadata, db: Session = Depends(get_db)):
    return upsert_workout_plan_metadata(body, db)

@router.delete("/delete-plan/{id}")
@limiter.limit("20/minute")
async def delete_myworkout_plan(request: Request, id: str, db: Session = Depends(get_db)):
    return delete_workout_plan_by_id(id, db)

@router.get("/all-day")
@limiter.limit("20/minute")
async def get_all_myworkout_day(request: Request, plan_id: str, db: Session = Depends(get_db)):
    return get_all_workout_days_by_plan(plan_id, db)

@router.get("/day/{id}")
@limiter.limit("20/minute")
async def get_workout_day(request: Request, id: str, db: Session = Depends(get_db)):
    return get_workout_day_by_id_service(id, db)

@router.post("/upsert-day")
@limiter.limit("20/minute")
async def upsert_myworkout_day(request: Request, body: UpsertWorkoutDay, db: Session = Depends(get_db)):
    return upsert_workout_day(body, db)

@router.delete("/delete-day/{id}")
@limiter.limit("50/minute")
async def delete_myworkout_day(request: Request, id: str, db: Session = Depends(get_db)):
    return delete_workout_day_by_id(id, db)

@router.post("/save-ai-plan")
@limiter.limit("20/minute")
async def save_ai_myworkout_plan(request: Request, body: SaveAIWorkoutPlanPayload, db: Session = Depends(get_db)):
    return save_ai_workout_plan(body, db)


