from fastapi import APIRouter, HTTPException
from .models import AddUserReq, UserResponse
from db.queries import add_user_data, get_all_users
from job.tasks import create_weekly_email_entry


router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def add_user(body: AddUserReq):
    try:
        user = add_user_data(dict(body))
        create_weekly_email_entry(user.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/users", response_model=list[UserResponse])
async def get_users():
    return get_all_users()
