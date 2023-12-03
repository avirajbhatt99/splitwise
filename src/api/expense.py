from fastapi import APIRouter, HTTPException
from .models import AddExpenseReq
from db.queries import add_expense_data
from job.tasks import send_email
from job.worker import send_weekly_email_to_user

router = APIRouter()


@router.post("/expenses")
async def add_expense(body: AddExpenseReq):
    """
    Add expense endpoint
    """
    expense_type = body.expense_type.value
    no_of_users = len(body.user_ids)
    # check if no_of_users is more than 1000
    if no_of_users > 1000:
        raise HTTPException(status_code=400, detail="Expense can on;y have 1000 users")
    # check if expense amount is more than 10000000
    if body.amount > 10000000:
        raise HTTPException(
            status_code=400, detail="Expense amount can not be more than 1,00,00,000"
        )
    if expense_type == "equal":
        amount_owed_by_each_user = round((body.amount / no_of_users), 2)
        if amount_owed_by_each_user * no_of_users != body.amount:
            extra_amount = body.amount - (amount_owed_by_each_user * no_of_users)
        else:
            extra_amount = 0
        amount_owed = {
            key: (amount_owed_by_each_user + extra_amount)
            if key == body.payer_id
            else amount_owed_by_each_user
            for key, _ in body.user_ids.items()
        }

    elif expense_type == "percent":
        # check if percentage is equal to 100
        if sum(body.user_ids.values()) != 100:
            raise HTTPException(status_code=400, detail="Percentage not equal to 100")

        amount_owed = {
            key: (value / 100 * body.amount) for key, value in body.user_ids.items()
        }

    elif expense_type == "exact":
        # check if sum of amount is equal to total amount
        if sum(body.user_ids.values()) != body.amount:
            raise HTTPException(
                status_code=400, detail="Amounts not equal to total amount"
            )

        amount_owed = body.user_ids

    expense = add_expense_data(dict(body), amount_owed)
    send_email.apply_async(args=[expense.id])
