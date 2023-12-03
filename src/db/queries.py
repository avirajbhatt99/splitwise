from uuid import uuid4
from .postgre import session as db
from .models import User, Expense, Passbook


def get_user_by_email(email: str):
    return db.query(User).filter(User.email == email).first()


def add_user_data(user_data: dict):
    """
    add user to table
    """
    # check if user exists
    if get_user_by_email(user_data["email"]) != None:
        raise Exception

    user = User(
        id=uuid4().hex,
        name=user_data["name"],
        mobile_number=user_data["mobile_number"],
        email=user_data["email"],
    )
    db.add(user)
    db.commit()
    return user


def get_all_users():
    """
    fetch all users from database
    """
    return db.query(User).all()


def get_user_by_id(user_id: str):
    """
    get user by id
    """
    return db.query(User).filter(User.id == user_id).first()


def get_expense_by_id(expense_id: str):
    """
    get expense by id
    """
    return db.query(Expense).filter(Expense.id == expense_id).first()


def get_expense_by_payer_id(payer_id: str):
    """
    Get expense by payer id
    """
    expenses = db.query(Expense).filter(Expense.payer_id == payer_id).all()
    return [expense.id for expense in expenses]


def get_passbook_by_expense_id(expense_id: str):
    """
    get passbook data by expense id
    """
    return db.query(Passbook).filter(Passbook.expense_id == expense_id).all()


def add_expense_data(expense_data: dict, amount_owed: dict):
    """
    add expense
    """
    expense = Expense(
        id=uuid4().hex,
        name=expense_data["name"],
        payer_id=expense_data["payer_id"],
        amount=expense_data["amount"],
        expense_type=expense_data["expense_type"],
    )
    db.add(expense)
    # payer_name = expense.payer.name
    for user, amount in amount_owed.items():
        passbook_entry = Passbook(
            id=uuid4().hex, expense_id=expense.id, user_id=user, amount_owes=amount
        )
        db.add(passbook_entry)

    db.commit()
    return expense


def get_passbook_data():
    """
    Get passbook data
    """
    passbook = db.query(Passbook).all()
    return passbook


def get_passbook_data_by_payer(payer_id: str):
    """
    get passbook data for specific payer
    """
    expense_ids = get_expense_by_payer_id(payer_id)

    passbook = db.query(Passbook).filter(Passbook.expense_id.in_(expense_ids)).all()
    return passbook


def get_passbook_data_by_user(user_id: str):
    """
    get passbook data for specific payer
    """

    passbook = db.query(Passbook).filter(Passbook.user_id == user_id).all()
    return passbook
