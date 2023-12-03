from pydantic import BaseModel, Field, EmailStr, conint
from db.models import ExpenseType


class AddUserReq(BaseModel):
    """
    To validate Add user request payload
    """

    name: str = Field(description="Name of the user")
    email: EmailStr = Field(description="Email of the user")
    mobile_number: conint(gt=6000000000, lt=9999999999) = Field(
        description="Mobile number of the user"
    )


class UserResponse(BaseModel):
    """
    User response model
    """

    id: str
    name: str
    email: str
    mobile_number: int


class AddExpenseReq(BaseModel):
    """
    To validate Add expense request payload
    """

    name: str = Field(description="Name of the expense")
    payer_id: str = Field(description="user_id of the payer")
    amount: float = Field(description="Amount of the expense")
    expense_type: ExpenseType = Field(description="the way in which expense is divided")
    user_ids: dict = Field(
        description="""user_ids which needs to be added in expense, key as id and value as amount 
                                or percentage if expense type is not equal"""
    )
