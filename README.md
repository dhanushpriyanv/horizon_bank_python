# Horizon Bank .NET 7 Application

This is a .NET 7 Web API application converted from the original Python Flask banking application. It provides banking functionality including customer management, account operations, and transaction processing.

## Architecture

The application follows Clean Architecture principles with the following layers:

- **HorizonBank.API**: Web API layer with controllers and middleware
- **HorizonBank.Core**: Domain entities, DTOs, interfaces, and exceptions
- **HorizonBank.Infrastructure**: Data access, repositories, and services

## Features

- Customer management (CRUD operations)
- Account management with balance tracking
- Transaction processing (transfers, bill payments, deposits)
- Oracle database integration with Entity Framework Core
- Exception handling middleware
- Swagger API documentation
- CORS support for frontend integration
- Structured logging with Serilog

## Prerequisites

- .NET 7 SDK
- Oracle Database (XE or higher)
- Visual Studio 2022 or VS Code

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd horizon-bank-dotnet
   ```

2. **Update connection string**
   Update the connection string in `appsettings.json` to match your Oracle database configuration.

3. **Restore packages**
   ```bash
   dotnet restore
   ```

4. **Run the application**
   ```bash
   cd HorizonBank.API
   dotnet run
   ```

5. **Access the API**
   - API: `https://localhost:7000` or `http://localhost:5000`
   - Swagger UI: `https://localhost:7000/swagger`

## API Endpoints

### Customers
- `GET /api/customers` - Get all customers
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers` - Create new customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Accounts
- `GET /api/accounts` - Get all accounts
- `GET /api/accounts/{id}` - Get account by ID
- `GET /api/accounts/customer/{customerId}` - Get account by customer ID
- `POST /api/accounts/create` - Create new account
- `POST /api/accounts/add-money` - Add money to account

### Transactions
- `GET /api/transactions` - Get all transactions
- `GET /api/transactions/{id}` - Get transaction by ID
- `GET /api/transactions/customer/{customerId}` - Get transactions by customer
- `POST /api/transactions` - Transfer money between accounts
- `POST /api/transactions/bill-pay` - Pay bills
- `POST /api/transactions/add-money` - Add money to account

## Database Schema

The application uses Oracle sequences and the following tables:
- `CUSTOMERS` - Customer information
- `ACCOUNTS` - Account details with balances
- `TRANSACTIONS` - Transaction history

## Key Differences from Python Version

1. **Type Safety**: Strong typing with C# vs dynamic typing in Python
2. **Dependency Injection**: Built-in DI container vs manual dependency management
3. **Entity Framework**: ORM with migrations vs raw SQL queries
4. **Async/Await**: Native async support throughout the application
5. **AutoMapper**: Object mapping vs manual serialization
6. **Middleware Pipeline**: Built-in middleware vs Flask decorators
7. **Configuration**: appsettings.json vs environment variables

## Testing

The application includes comprehensive error handling and logging. You can test the API using:
- Swagger UI (built-in)
- Postman
- curl commands
- Unit tests (can be added in separate test projects)

## Deployment

The application can be deployed to:
- IIS
- Azure App Service
- Docker containers
- Kubernetes clusters

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request