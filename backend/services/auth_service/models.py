from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

    user_type: str      # ✅ admin / user (LOGIN CONTROL)
    department: str     # ✅ IT, HR, etc.
    role: str           # ✅ job role (Developer, HR Manager)
    employee_id: str
# class UserRegister(BaseModel):
#     username: str
#     password: str
#     role: str = "user"  # "user" or "admin"

class UserLogin(BaseModel):
    username: str
    password: str

class Ticket(BaseModel):
    title: str
    description: str
    created_by: str
    status: str = "Open"
    priority: str = "Medium"
    department: str      # ✅ NEW
    role: str            # ✅ NEW
    employee_id: str     # ✅ NEW



from typing import Optional
from pydantic import BaseModel

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
class Comment(BaseModel):
    ticket_id: str
    username: str
    role: str        # "user" or "admin"
    message: str
    created_at: str  # ISO timestamp string