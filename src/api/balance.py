from fastapi import APIRouter, Query
from db.queries import (
    get_passbook_data,
    get_passbook_data_by_payer,
    get_passbook_data_by_user,
)

router = APIRouter()


@router.get("/balances")
def get_balances(simplify=Query(default=False)):
    """
    Get balances for each user from passbook
    """
    passbook_data = get_passbook_data()
    amount_owed = get_amount_owed(passbook_data)
    if simplify:
        return get_simplified_debt(amount_owed)

    return amount_owed


@router.get("/balances/{payer_id}")
def get_user_balance(payer_id: str):
    """
    Get balance for specific user
    """
    passbook_data = get_passbook_data_by_payer(payer_id)
    return get_amount_owed(passbook_data)


@router.get("/passbook/{user_id}")
def get_user_passbook(user_id: str):
    """
    Get transactions for user
    """
    passbook_data = get_passbook_data_by_user(user_id)
    return [
        {
            "date": data.expense.date,
            "name": data.expense.name,
            "amount": data.amount_owes,
        }
        for data in passbook_data
    ]


def get_amount_owed(passbook_data):
    """
    Converts passbook data to json
    """
    for data in passbook_data:
        data.payer_id = data.expense.payer_id
    # Iterate through the passbook data and update the amounts_owed dictionary
    amounts_owed = {}
    for entry in passbook_data:
        user_id = entry.user_id
        payer_id = entry.payer_id
        amount_owes = entry.amount_owes
        if user_id == payer_id:
            continue

        # If user_id is not in the dictionary, initialize it with zero
        amounts_owed.setdefault(payer_id, {}).setdefault(user_id, 0.0)

        # Update the amount owed by user_id to payer_id
        amounts_owed[payer_id][user_id] += amount_owes

    return amounts_owed


def get_simplified_debt(amount_owed: dict):
    """
    Get simplified debt
    """
    # create a list[list] contain from to amount
    amount_data = []
    for lender, borrower_dict in amount_owed.items():
        for borrower, amount in borrower_dict.items():
            amount_data.append([lender, borrower, amount])
    user_and_balance = {}
    for data in amount_data:
        lender = data[0]
        borrower = data[1]
        amount = data[2]
        user_and_balance[lender] = user_and_balance.get(lender, 0) - amount
        user_and_balance[borrower] = user_and_balance.get(borrower, 0) + amount

    amount = list(user_and_balance.values())
    users = list(user_and_balance.keys())
    data_to_return = min_cash_flow(amount)
    return convert_to_user_data(data_to_return, users)


def convert_to_user_data(data_to_return: dict, users: list) -> dict:
    """
    Changes index number to user_id
    """
    new_dict = {}
    for key, value in data_to_return.items():
        if isinstance(value, dict):
            new_dict[users[key]] = convert_to_user_data(value, users)
        else:
            new_dict[users[key]] = value
    return new_dict


def get_min(arr):
    """
    get minimum index from array
    """

    min_index = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[min_index]:
            min_index = i
    return min_index


def get_max(arr):
    """
    Get maximum index from array
    """
    max_index = 0
    for i in range(1, len(arr)):
        if arr[i] > arr[max_index]:
            max_index = i
    return max_index


def min_cash_flow(amount_list: list, data_to_return: dict = {}):
    # negative is reciever and positive is giver
    receiver = get_min(amount_list)
    giver = get_max(amount_list)

    # If both amounts are 0,
    # then all amounts are settled
    if amount_list[receiver] == 0 and amount_list[giver] == 0:
        return 0

    # Find the minimum of two amounts
    min_amount = min(-amount_list[receiver], amount_list[giver])
    amount_list[receiver] += min_amount
    amount_list[giver] -= min_amount

    # Check if the receiver key exists in data_to_return
    if receiver not in data_to_return:
        # If not, create an empty dictionary for the receiver
        data_to_return[receiver] = {}

    data_to_return[receiver][giver] = min_amount
    min_cash_flow(amount_list, data_to_return)

    return data_to_return
