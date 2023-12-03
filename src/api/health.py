from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"message": "App is running"}
