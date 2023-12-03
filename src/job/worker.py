import requests
from db.queries import get_passbook_by_expense_id, get_passbook_data_by_user
from conf import MAILGUN_API_KEY, MAILGUN_DOMAIN

mailgun_api_key = MAILGUN_API_KEY
mailgun_domain = MAILGUN_DOMAIN


def send_email_to_user(expense_id: str):
    """
    Send email for expense
    """
    passbook_data = get_passbook_by_expense_id(expense_id)
    for data in passbook_data:
        payer_name = data.expense.payer.name
        user_name = data.user.name
        amount_owed = data.amount_owes
        expense_name = data.expense.name
        to = data.user.email
        if payer_name == user_name:
            continue

        # Mailgun API endpoint
        url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"

        # Mailgun API key
        auth = ("api", mailgun_api_key)

        template = create_template(user_name, expense_name, amount_owed, payer_name)
        data = {
            "from": "test@example.com",
            "to": to,
            "subject": "You are added to a expense",
            "html": template,
        }
        # send email
        requests.post(url, auth=auth, data=data)


def create_template(
    user_name: str,
    expense_name: str,
    amount_owed: float,
    payer_name: str,
):
    """
    template for mail
    """
    html_template = f"""
        <html>
        <head></head>
        <body>
            <p>Hello {user_name},</p>
            <p>You have been added to the expense '<strong>{expense_name}</strong>' and you owe <strong>{amount_owed}</strong> to {payer_name}.</p>
            <p>Thank you,<br/>
            The Splitwise Team</p>
        </body>
        </html>
        """

    return html_template


def send_weekly_email_to_user(user_id: str):
    """
    Send weekly email to user how much they owe to someone
    """
    passbook_data = get_passbook_data_by_user(user_id)
    if len(passbook_data) == 0:
        return
    email_data = {}
    user_name = passbook_data[0].user.name
    user_email = passbook_data[0].user.email
    for entry in passbook_data:
        if entry.expense.payer.name not in email_data:
            email_data[entry.expense.payer.name] = entry.amount_owes
        else:
            email_data[entry.expense.payer.name] = (
                email_data[entry.expense.payer.name] + entry.amount_owes
            )

    # Mailgun API endpoint
    url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"

    # Mailgun API key
    auth = ("api", mailgun_api_key)

    template = weekly_template(user_name, email_data)
    data = {
        "from": "test@example.com",
        "to": "avirajbhatt@gmail.com",
        "subject": "Your weekly expense report",
        "html": template,
    }
    # send email
    requests.post(url, auth=auth, data=data)


def weekly_template(user_name: str, email_data: dict):
    """
    Create weekly email template
    """
    list_element = ""
    for payer_name, amount in email_data.items():
        list_element += f"<li>You owe {amount} to {payer_name}</li>\n"
    html_template = f"""
        <html>
        <head></head>
        <body>
            <p>Hello {user_name},</p>
            <ul>
            {list_element}
            </ul>
            <p>Thank you,<br/>
            The Splitwise Team</p>
        </body>
        </html>
        """
    return html_template
