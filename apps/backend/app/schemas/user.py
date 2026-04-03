from pydantic import BaseModel


class UserSettingsResponse(BaseModel):
    full_name: str
    email: str
    notifications_enabled: bool
    warranty_reminders_enabled: bool
    preferred_currency: str

    model_config = {
        "from_attributes": True
    }


class UserSettingsUpdate(BaseModel):
    full_name: str
    email: str
    notifications_enabled: bool
    warranty_reminders_enabled: bool
    preferred_currency: str
