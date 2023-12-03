# Splitwise backend

An expense sharing application is where you can add your expenses and split it among different people. The app keeps balances between people as in who owes how much to whom.

## Architecture

### Database Schema

### 1. User Table

The `users` table stores information about users in your application.

- **id:** Primary key, a unique identifier for each user (auto-generated UUID).
- **name:** Name of the user.
- **email:** Email address of the user.
- **mobile_number:** Mobile number of the user.


### 2. Expense Table

The `expenses` table stores information about expenses incurred.

- **id:** Primary key, a unique identifier for each expense (auto-generated UUID).
- **name:** Name of the expense.
- **date:** Date when the expense occurred (default is the current date and time).
- **amount:** Total amount of the expense.
- **payer_id:** Foreign key referencing the `id` in the `users` table, indicating the payer of the expense.
- **expense_type:** Enum representing how the expense is divided among users.
- **payer:** Relationship with the `User` table.

### 3. Passbook Table

The `passbook` table keeps a record of the amount each user owes for each expense.

- **id:** Primary key, a unique identifier for each passbook entry (auto-generated UUID).
- **expense_id:** Foreign key referencing the `id` in the `expenses` table.
- **user_id:** Foreign key referencing the `id` in the `users` table.
- **amount_owes:** Amount that the user owes for the expense.
- **expense:** Relationship with the `Expense` table.
- **user:** Relationship with the `User` table.


### Expense Handling

When an expense is added:

1. The expense details are added to the `expenses` table.
2. Entries are created in the `passbook` table, linking each user to the expense and specifying the amount owed.

### Asynchronous Email Notifications

For asynchronous email notifications:

1. A Celery task is created whenever an expense is added.
2. The Celery task, using Redis as a broker, sends emails to users notifying them that they have been added to an expense.

### Weekly Email Reminders

To send weekly email reminders about owed amounts:

1. A scheduling entry is added using RedBeat Scheduler whenever a user is created in the database.
2. RedBeat Scheduler triggers a weekly task in Celery.
3. The Celery task sends an email to the user summarizing the amounts owed to different users.


## APIs

### 1. `/users` - POST Request

#### Payload

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "mobile_number": 9876543210
}
```

- **name:** (string) Name of the user.
- **email:** (string) Email of the user.
- **mobile_number:** (integer) Mobile number of the user (between 6000000000 and 9999999999).

### 2. `/expenses` - POST Request

#### Payload

```json
{
  "name": "Dinner",
  "payer_id": "user_id_of_payer",
  "amount": 50.00,
  "expense_type": "equal",
  "user_ids": {
    "user_id_1": 25.00,
    "user_id_2": 25.00
  }
}
```

- **name:** (string) Name of the expense.
- **payer_id:** (string) User ID of the payer.
- **amount:** (float) Amount of the expense.
- **expense_type:** (enum) Type of expense ("equal", "exact", "percent").
- **user_ids:** (dictionary) User IDs and their respective amounts or percentages.

### 3. `/balances` - GET Request

#### Query Parameters

- **simplify:** (boolean) If true, simplifies data for all users.

### 4. `/balances/{payer_id}` - GET Request

#### URL Parameters

- **payer_id:** (string) User ID of the payer.

### 5. `/passbook/{user_id}` - GET Request

#### URL Parameters

- **user_id:** (string) User ID for which passbook data is requested.
