from sqlalchemy.orm import Session #type: ignore
from fastapi import HTTPException, status #type: ignore
from src.models.user_model import User
from src.models.exercise import Exercise
from src.models.workoutplan import WorkoutPlan
from src.models.workoutday import WorkoutDay
from src.models.workout_day_exercise import WorkoutDayExercise
from src.models.muscle_group import MuscleGroup
from src.models.user_workout_stats import UserWorkoutStats
from src.schemas.myworkout_schema import UpsertWorkoutPlanMetadata, UpsertWorkoutDay, SaveAIWorkoutPlanPayload, SaveUserWorkoutStatsPayload
from src.utils.response import Response


def _get_workout_plan_hierarchy(plan_id: str, db: Session) -> dict:
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")
        
    days_list = []
    for day in plan.days:
        ex_list = []
        for wde in day.exercises:
            ex_list.append({
                "id": wde.id,
                "exercise_id": wde.exercise_id,
                "sort_order": wde.sort_order,
                "sets": wde.sets_data,
                "exercise_details": {
                    "id": wde.exercise.id,
                    "name": wde.exercise.name,
                    "description": wde.exercise.description,
                    "category": wde.exercise.category,
                    "is_active": wde.exercise.is_active,
                    "muscle_group_id": wde.exercise.muscle_group_id,
                    "muscle_group_name": wde.exercise.muscle_group.name if wde.exercise.muscle_group else None
                } if wde.exercise else None
            })
        days_list.append({
            "id": day.id,
            "day_number": day.day_number,
            "label": day.label,
            "exercises": ex_list,
            "created_at": day.created_at,
            "updated_at": day.updated_at
        })
        
    return {
        "id": plan.id,
        "user_id": plan.user_id,
        "name": plan.name,
        "description": plan.description,
        "is_active": plan.is_active,
        "created_at": plan.created_at,
        "updated_at": plan.updated_at,
        "days": days_list
    }

def upsert_workout_plan_metadata(body: UpsertWorkoutPlanMetadata, db: Session):
    # Validate user exists
    user_exists = db.query(User).filter(User.id == body.user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
        
    try:
        if body.id:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == body.id).first()
            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Workout plan not found"
                )
            plan.user_id = body.user_id
            plan.name = body.name
            plan.description = body.description
            plan.is_active = body.is_active if body.is_active is not None else plan.is_active
        else:
            plan = WorkoutPlan(
                user_id=body.user_id,
                name=body.name,
                description=body.description,
                is_active=body.is_active if body.is_active is not None else True
            )
            db.add(plan)
            
        db.commit()
        db.refresh(plan)
        
        return Response(
            success=True,
            message="Workout plan saved successfully",
            data={
                "id": plan.id,
                "user_id": plan.user_id,
                "name": plan.name,
                "description": plan.description,
                "is_active": plan.is_active,
                "created_at": plan.created_at,
                "updated_at": plan.updated_at
            }
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def upsert_workout_day(body: UpsertWorkoutDay, db: Session):
    # 1. Validation Rules
    # Plan validation
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == body.plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )

    # Day number validation (1 to 7)
    if not (1 <= body.day_number <= 7):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Day number must be between 1 and 7 (1=Mon, 7=Sun)"
        )

    # Check maximum of 7 workout days per workout plan
    existing_days_count = db.query(WorkoutDay).filter(WorkoutDay.plan_id == body.plan_id).count()
    day_exists = db.query(WorkoutDay).filter(
        WorkoutDay.plan_id == body.plan_id,
        WorkoutDay.day_number == body.day_number
    ).first()

    if not body.id and not day_exists and existing_days_count >= 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workout plan already contains the maximum of 7 days"
        )

    # Unique day number check per plan
    if day_exists and (not body.id or day_exists.id != body.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Day number {body.day_number} already exists in this workout plan"
        )

    # Max 20 exercises check
    if len(body.exercises) > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workout day cannot have more than 20 exercises"
        )

    # Unique exercise sort orders check
    sort_orders = [ex.sort_order for ex in body.exercises]
    if len(sort_orders) != len(set(sort_orders)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate exercise sort orders in payload"
        )

    # Exercise existence check
    exercise_ids = {ex.exercise_id for ex in body.exercises}
    if exercise_ids:
        existing_count = db.query(Exercise.id).filter(Exercise.id.in_(exercise_ids)).count()
        if existing_count != len(exercise_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more exercise IDs in payload do not exist"
            )

    try:
        # 2. CRUD Day Logic
        if body.id:
            # Update day metadata
            day = db.query(WorkoutDay).filter(WorkoutDay.id == body.id).first()
            if not day:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Workout day not found"
                )
            if day.plan_id != body.plan_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot change parent workout plan of an existing day"
                )
            day.day_number = body.day_number
            day.label = f"Day {body.day_number}"

            # Delete old exercises
            db.query(WorkoutDayExercise).filter(WorkoutDayExercise.day_id == day.id).delete(synchronize_session=False)
        else:
            # Create new day
            day = WorkoutDay(
                plan_id=body.plan_id,
                day_number=body.day_number,
                label=f"Day {body.day_number}"
            )
            db.add(day)
            db.flush() # Generate ID

        # Create/recreate exercises
        for ex_item in body.exercises:
            sets_data = [
                {
                    "set_number": s.set_number,
                    "target_reps": s.target_reps,
                    "reps_performed": s.reps_performed,
                    "weight_kg": s.weight_kg,
                    "rest_seconds": s.rest_seconds
                }
                for s in ex_item.sets
            ]
            wde = WorkoutDayExercise(
                day_id=day.id,
                exercise_id=ex_item.exercise_id,
                sort_order=ex_item.sort_order,
                sets_data=sets_data
            )
            db.add(wde)

        db.commit()
        db.refresh(day)

        # Format returned day hierarchy
        ex_list = []
        for wde in day.exercises:
            ex_list.append({
                "id": wde.id,
                "exercise_id": wde.exercise_id,
                "sort_order": wde.sort_order,
                "sets": wde.sets_data,
                "exercise_details": {
                    "id": wde.exercise.id,
                    "name": wde.exercise.name,
                    "description": wde.exercise.description,
                    "category": wde.exercise.category,
                    "is_active": wde.exercise.is_active,
                    "muscle_group_id": wde.exercise.muscle_group_id,
                    "muscle_group_name": wde.exercise.muscle_group.name if wde.exercise.muscle_group else None
                } if wde.exercise else None
            })

        data = {
            "id": day.id,
            "plan_id": day.plan_id,
            "day_number": day.day_number,
            "label": day.label,
            "exercises": ex_list,
            "created_at": day.created_at,
            "updated_at": day.updated_at
        }

        return Response(
            success=True,
            message="Workout day saved successfully",
            data=data
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def delete_workout_plan_by_id(id: str, db: Session):
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
        
    db.delete(plan)
    db.commit()
    return Response(
        success=True,
        message="Workout plan deleted successfully",
        data=None
    )

def get_workout_plan_by_id(id: str, db: Session):
    data = _get_workout_plan_hierarchy(id, db)
    return Response(
        success=True,
        message="Workout plan retrieved successfully",
        data=data
    )

def get_all_workout_plans(user_id: str, db: Session):
    # Verify user exists
    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    plans = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).all()
    
    result = []
    for p in plans:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "is_active": p.is_active,
            "user": {
                "id": p.user.id,
                "username": p.user.username,
                "email": p.user.email
            } if p.user else None,
            "total_workout_days": len(p.days),
            "created_at": p.created_at,
            "updated_at": p.updated_at
        })
        
    return Response(
        success=True,
        message="Workout plans retrieved successfully",
        data=result
    )

def delete_workout_day_by_id(id: str, db: Session):
    day = db.query(WorkoutDay).filter(WorkoutDay.id == id).first()
    if not day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout day not found"
        )
    db.delete(day)
    db.commit()
    return Response(
        success=True,
        message="Workout day deleted successfully",
        data=None
    )

def get_workout_day_by_id_service(id: str, db: Session):
    day = db.query(WorkoutDay).filter(WorkoutDay.id == id).first()
    if not day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout day not found"
        )
        
    ex_list = []
    for wde in day.exercises:
        ex_list.append({
            "id": wde.id,
            "exercise_id": wde.exercise_id,
            "sort_order": wde.sort_order,
            "sets": wde.sets_data,
            "exercise_details": {
                "id": wde.exercise.id,
                "name": wde.exercise.name,
                "description": wde.exercise.description,
                "category": wde.exercise.category,
                "is_active": wde.exercise.is_active,
                "muscle_group_id": wde.exercise.muscle_group_id,
                "muscle_group_name": wde.exercise.muscle_group.name if wde.exercise.muscle_group else None
            } if wde.exercise else None
        })

    data = {
        "id": day.id,
        "plan_id": day.plan_id,
        "day_number": day.day_number,
        "label": day.label,
        "exercises": ex_list,
        "created_at": day.created_at,
        "updated_at": day.updated_at
    }

    return Response(
        success=True,
        message="Workout day retrieved successfully",
        data=data
    )

def get_all_workout_days_by_plan(plan_id: str, db: Session):
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")
        
    days = db.query(WorkoutDay).filter(WorkoutDay.plan_id == plan_id).all()
    
    result = []
    for day in days:
        ex_list = []
        for wde in day.exercises:
            ex_list.append({
                "id": wde.id,
                "exercise_id": wde.exercise_id,
                "sort_order": wde.sort_order,
                "sets": wde.sets_data,
                "exercise_details": {
                    "id": wde.exercise.id,
                    "name": wde.exercise.name,
                    "description": wde.exercise.description,
                    "category": wde.exercise.category,
                    "is_active": wde.exercise.is_active,
                    "muscle_group_id": wde.exercise.muscle_group_id,
                    "muscle_group_name": wde.exercise.muscle_group.name if wde.exercise.muscle_group else None
                } if wde.exercise else None
            })
            
        result.append({
            "id": day.id,
            "plan_id": day.plan_id,
            "day_number": day.day_number,
            "label": day.label,
            "exercises": ex_list,
            "created_at": day.created_at,
            "updated_at": day.updated_at
        })
        
    return Response(
        success=True,
        message="Workout days retrieved successfully",
        data=result
    )

def save_ai_workout_plan(body: SaveAIWorkoutPlanPayload, db: Session):
    # Verify user exists
    user_exists = db.query(User).filter(User.id == body.user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    try:
        # 1. Create WorkoutPlan
        plan = WorkoutPlan(
            user_id=body.user_id,
            name=body.name,
            description=body.description,
            is_active=True
        )
        db.add(plan)
        db.flush() # get plan.id
        
        # 2. Iterate Days
        for day_item in body.days:
            day = WorkoutDay(
                plan_id=plan.id,
                day_number=day_item.day_number,
                label=f"Day {day_item.day_number}"
            )
            db.add(day)
            db.flush() # get day.id
            
            # 3. Iterate Exercises
            for ex_item in day_item.exercises:
                # Find exercise in DB by name
                exercise = db.query(Exercise).filter(Exercise.name.ilike(ex_item.exercise_name)).first()
                
                if not exercise:
                    # Check if 'Other' MuscleGroup exists
                    other_mg = db.query(MuscleGroup).filter(MuscleGroup.slug == "other").first()
                    if not other_mg:
                        other_mg = MuscleGroup(
                            name="Other",
                            slug="other"
                        )
                        db.add(other_mg)
                        db.flush() # get other_mg.id
                        
                    # Create custom exercise
                    exercise = Exercise(
                        name=ex_item.exercise_name,
                        muscle_group_id=other_mg.id,
                        created_by=body.user_id,
                        category="free_weights", # default category
                        description=f"Custom exercise added dynamically for: {ex_item.exercise_name}",
                        is_active=True
                    )
                    db.add(exercise)
                    db.flush() # get exercise.id
                    
                # Create WorkoutDayExercise
                sets_data = [
                    {
                        "set_number": s.set_number,
                        "target_reps": s.target_reps,
                        "reps_performed": s.reps_performed,
                        "weight_kg": s.weight_kg,
                        "rest_seconds": s.rest_seconds
                    }
                    for s in ex_item.sets
                ]
                
                wde = WorkoutDayExercise(
                    day_id=day.id,
                    exercise_id=exercise.id,
                    sort_order=ex_item.sort_order,
                    sets_data=sets_data
                )
                db.add(wde)
                
        db.commit()
        db.refresh(plan)
        
        # Get complete nested hierarchy to return
        data = _get_workout_plan_hierarchy(plan.id, db)
        return Response(
            success=True,
            message="AI workout plan saved successfully",
            data=data
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def get_active_workout_day(user_id: str, date_str: Optional[str], db: Session):
    # Verify user exists
    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Determine day number (1=Mon, 7=Sun)
    if date_str:
        from datetime import datetime
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
    else:
        from datetime import datetime
        dt = datetime.now() # defaults to today
        
    day_number = dt.isoweekday() # 1 to 7

    # Find the active workout plan for this user
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == user_id,
        WorkoutPlan.is_active == True
    ).first()
    
    if not plan:
        # Fallback to the latest updated workout plan
        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).order_by(WorkoutPlan.updated_at.desc()).first()
        
    if not plan:
        return Response(
            success=True,
            message="No workout plans found for this user",
            data=None
        )
        
    # Find the WorkoutDay matching day_number
    day = db.query(WorkoutDay).filter(
        WorkoutDay.plan_id == plan.id,
        WorkoutDay.day_number == day_number
    ).first()
    
    # Map day_number to name for response helper
    day_names = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    weekday_name = day_names.get(day_number, "Unknown")
    
    if not day:
        return Response(
            success=True,
            message=f"Rest day or no exercises configured for {weekday_name}",
            data={
                "plan_id": plan.id,
                "plan_name": plan.name,
                "day_number": day_number,
                "day_name": weekday_name,
                "is_rest_day": True,
                "exercises": []
            }
        )
        
    # Format exercises list
    ex_list = []
    for wde in day.exercises:
        ex_list.append({
            "id": wde.id,
            "exercise_id": wde.exercise_id,
            "sort_order": wde.sort_order,
            "sets": wde.sets_data,
            "exercise_details": {
                "id": wde.exercise.id,
                "name": wde.exercise.name,
                "description": wde.exercise.description,
                "category": wde.exercise.category,
                "is_active": wde.exercise.is_active,
                "muscle_group_id": wde.exercise.muscle_group_id,
                "muscle_group_name": wde.exercise.muscle_group.name if wde.exercise.muscle_group else None
            } if wde.exercise else None
        })
        
    return Response(
        success=True,
        message=f"Active workout day retrieved successfully for {weekday_name}",
        data={
            "plan_id": plan.id,
            "plan_name": plan.name,
            "day_id": day.id,
            "day_number": day.day_number,
            "day_label": day.label,
            "day_name": weekday_name,
            "is_rest_day": False,
            "exercises": ex_list
        }
    )

def save_user_workout_stats(body: SaveUserWorkoutStatsPayload, db: Session):
    # Verify user exists
    user_exists = db.query(User).filter(User.id == body.user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    # Verify workout plan exists
    plan_exists = db.query(WorkoutPlan).filter(WorkoutPlan.id == body.workout_plan_id).first()
    if not plan_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
        
    try:
        # Convert Pydantic schemas list to simple python list of dicts for JSON column
        exercises_list = []
        for ex in body.exercises_data:
            sets_list = []
            for s in ex.sets:
                sets_list.append({
                    "set_number": s.set_number,
                    "target_reps": s.target_reps,
                    "reps_performed": s.reps_performed,
                    "weight_kg": s.weight_kg,
                    "rest_seconds": s.rest_seconds,
                    "is_completed": s.is_completed
                })
            exercises_list.append({
                "exercise_id": ex.exercise_id,
                "exercise_name": ex.exercise_name,
                "sort_order": ex.sort_order,
                "sets": sets_list
            })
            
        stats = UserWorkoutStats(
            user_id=body.user_id,
            workout_plan_id=body.workout_plan_id,
            day_number=body.day_number,
            day_label=body.day_label,
            exercises_data=exercises_list
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)
        
        return Response(
            success=True,
            message="Workout stats logged successfully",
            data={
                "id": stats.id,
                "user_id": stats.user_id,
                "workout_plan_id": stats.workout_plan_id,
                "day_number": stats.day_number,
                "day_label": stats.day_label,
                "exercises_data": stats.exercises_data,
                "created_at": stats.created_at
            }
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def get_user_workout_stats_service(user_id: str, db: Session):
    # Verify user exists
    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    stats_list = db.query(UserWorkoutStats).filter(
        UserWorkoutStats.user_id == user_id
    ).order_by(UserWorkoutStats.created_at.desc()).all()
    
    data = []
    for s in stats_list:
        data.append({
            "id": s.id,
            "user_id": s.user_id,
            "workout_plan_id": s.workout_plan_id,
            "day_number": s.day_number,
            "day_label": s.day_label,
            "exercises_data": s.exercises_data,
            "created_at": s.created_at
        })
        
    return Response(
        success=True,
        message="User workout stats retrieved successfully",
        data=data
    )

