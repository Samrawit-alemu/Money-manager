# Money Manager Backend

A **personal finance management API** built with **FastAPI** and **MongoDB**.
This project helps **college students track their income and expenses**, manage their spending, and understand their financial habits through simple summaries.

Many students struggle to keep track of where their money goes (food, transport, entertainment, etc.). This system provides an easy way to **record transactions and view monthly or yearly summaries**, helping students make better financial decisions.

---

## Problem It Solves

College students often:

* Spend money without tracking it.
* Lose track of small daily expenses.
* Have difficulty understanding their monthly spending patterns.

This project solves that by allowing students to:

* Record income and expenses.
* View all their transactions in one place.
* See summaries of their spending by month or year.
* Calculate their overall financial balance.

---

## Features

### Authentication

* User registration
* User login
* JWT-based authentication
* Protected routes

### Transaction Management

* Create transactions
* View user transactions
* Update transactions
* Delete transactions

### Financial Summary

* Monthly summary of income and expenses
* Yearly summary
* Balance calculation

---

## Tech Stack

* **Backend Framework:** FastAPI
* **Database:** MongoDB
* **Authentication:** JWT (JSON Web Tokens)
* **Language:** Python
* **API Documentation:** Swagger UI (built-in with FastAPI)

---

## Project Structure

```id="79rxak"
app/
│
├── api/
│   └── v1/
│       └── endpoints/
│           ├── users.py
│           └── transactions.py
│
├── core/
│   └── security.py
│
├── db/
│   └── mongodb.py
│
├── repositories/
│   ├── user_repo.py
│   └── transaction_repo.py
│
├── schemas/
│   ├── user.py
│   └── transaction.py
│
├── services/
│   ├── user_service.py
│   └── transaction_service.py
│
└── main.py
```

---

## Installation

### 1. Clone the repository

```id="uvpoc5"
git clone <repository-url>
cd money-manager-backend
```

### 2. Create a virtual environment

```id="h6g2w8"
python -m venv venv
```

Activate it:

**Windows**

```id="aqp1o7"
venv\Scripts\activate
```

**Mac/Linux**

```id="h7p7a6"
source venv/bin/activate
```

---

### 3. Install dependencies

```id="qsq13n"
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the root directory.

Example:

```id="u6q47o"
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=money_manager
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5. Run the server

```id="h9x8c1"
uvicorn app.main:app --reload
```

Server will run at:

```id="0l2f0c"
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates documentation.

Swagger UI:

```id="1xg5g3"
http://127.0.0.1:8000/docs
```

Alternative docs:

```id="t33jot"
http://127.0.0.1:8000/redoc
```

---

## Example API Endpoints

### Authentication

```id="0xx7ql"
POST /api/v1/users/register
POST /api/v1/users/login
```

### Transactions

```id="c15k0d"
POST /api/v1/transactions
GET /api/v1/transactions
PUT /api/v1/transactions/{id}
DELETE /api/v1/transactions/{id}
```

### Summary

```id="b25ryo"
GET /api/v1/transactions/summary?month=3&year=2026
```

---

## Example Transaction Object

```id="r7v1v7"
{
  "amount": 100,
  "type": "expense",
  "category": "food",
  "description": "Lunch",
  "created_at": "2026-03-09T12:00:00"
}
```

---

## Future Improvements

* Transaction categories management
* Pagination and filtering
* Spending analytics
* Budget tracking
* Docker deployment
* Unit testing

---

## Author

Developed as a learning project to practice **FastAPI, REST API development, and clean architecture**, while also addressing a **real-life financial tracking problem faced by college students**.
