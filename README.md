# 606-Project-Backend

## Overview

This repository contains the **backend implementation** for the **Expense Tracker** project, which was developed as part of the **Software Engineering Master's** course at **Texas A&M University**. The backend follows a **microservices architecture**, with separate services for **user authentication, transaction management, and a central service registry**.

## Features

- **Microservices Architecture**: Decoupled services for user authentication and expense tracking.
- **Service Registry**: A centralized registry that routes requests to microservices.
- **User Authentication**: Signup and login functionality.
- **Expense Tracking**: Add, edit, delete, and fetch expenses.
- **Monthly Budget Management**: Users can set and track budgets.
- **Inter-Service Communication**: RESTful API with service discovery.

## Technologies Used

- **Python** - Core backend implementation.
- **HTTPServer (BaseHTTPRequestHandler)** - API request handling.
- **REST API** - For frontend communication.
- **Microservices Architecture** - Services for authentication, transactions, and routing.
- **Proxy-based Service Discovery** - Handles API request forwarding.

## Repository Structure

```
606-Project-Backend/
│── service_registry/   # Manages service registration and request routing
│── transaction/        # Handles expense and budget management
│── user/               # Manages user authentication (login/signup)
│── .gitignore          # Git ignore file
│── README.md           # Project documentation
```

## Setup and Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-username/606-Project-Backend.git
   cd 606-Project-Backend
   ```

2. **Install dependencies** (if required):
   ```sh
   pip install requests
   ```

3. **Start the Service Registry**:
   ```sh
   cd service_registry
   python app.py
   ```
   - Runs the **Service Registry** on **port 8000**, which routes API requests.

4. **Start the User Service**:
   ```sh
   cd user
   python app.py
   ```
   - Runs the **User Service** on **port 8001** (handles authentication).

5. **Start the Transaction Service**:
   ```sh
   cd transaction
   python app.py
   ```
   - Runs the **Transaction Service** on **port 8002** (handles expenses and budgets).

## API Endpoints

The backend exposes the following **REST API endpoints**, all accessible via the **Service Registry (localhost:8000)**.

### **User Authentication Service**
| Method | Endpoint   | Description |
|--------|-----------|-------------|
| POST   | `/login`  | User authentication |
| POST   | `/signup` | User registration |

### **Transaction Service**
| Method | Endpoint             | Description |
|--------|----------------------|-------------|
| GET    | `/expenses`          | Fetch expenses for a user |
| POST   | `/expenses`          | Add a new expense |
| PUT    | `/expenses/{id}`     | Update an existing expense |
| DELETE | `/expense`           | Delete an expense |
| GET    | `/monthly_budget`    | Get user's monthly budget |
| POST   | `/monthly_budget`    | Update user's budget |

## Microservices Communication

- The **User Service** (port `8001`) manages authentication.
- The **Transaction Service** (port `8002`) handles expenses and budgets.
- The **Service Registry (Proxy)** (port `8000`) routes API requests dynamically.

Each microservice **registers itself** with the **service registry** at startup. This allows dynamic service discovery.

## Future Enhancements

- **Database Integration**: Use PostgreSQL or MongoDB instead of in-memory storage.
- **API Gateway**: Implement an advanced gateway for request routing.
- **Authentication Security**: Use JWT authentication.
- **Docker & Kubernetes Deployment**: Containerize and orchestrate the backend.

## Contributors

- **[Akshat Punjabi]** – Texas A&M University
- **[Xinyu Wu]** – Texas A&M University

## License

This project is for academic purposes and is **not licensed for commercial use**.
