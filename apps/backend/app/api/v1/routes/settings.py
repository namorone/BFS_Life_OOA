from fastapi import APIRouter
from app.schemas.user import UserSettingsResponse, UserSettingsUpdate

router = APIRouter(prefix="/settings", tags=["settings"])

fake_settings = {
    "full_name": "Roman Borovets",
    "email": "roman.borovets@gmail.com",
    "notifications_enabled": True,
    "warranty_reminders_enabled": True,
    "preferred_currency": "USD",
}


@router.get("", response_model=UserSettingsResponse)
def get_settings():
    return fake_settings


@router.put("", response_model=UserSettingsResponse)
def update_settings(payload: UserSettingsUpdate):
    fake_settings.update(payload.model_dump())
    return fake_settings
