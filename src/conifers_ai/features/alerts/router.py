from fastapi import APIRouter

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)

@router.get("/")
def read_alerts():
    return {"message": "This is the alerts endpoint."}