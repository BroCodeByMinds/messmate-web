from pydantic import BaseModel, Field
from typing import Optional, Literal


class MessCreate(BaseModel):
    name: str = Field(..., description="Name of the mess")
    city: str = Field(..., description="City where the mess is located")
    type: Literal["Veg", "Non-Veg", "Both"] = Field(..., description="Type of meals served")
    monthly_price: int = Field(..., gt=0, description="Monthly subscription price")
    address: str = Field(..., description="Address or location of the mess")
    description: Optional[str] = Field(None, description="Optional description of the mess")
    contact_number: Optional[str] = Field(None, description="Optional contact number")

class MessResponse(BaseModel):
    mess_id: int = Field(..., description="Unique ID of the created mess")
    name: str = Field(..., description="Mess name")
