# FastAPI Authentication
FastAPI Authentication offers a secure, scalable solution for user authentication and authorization using FastAPI, AWS Cognito, and GraphQL. The project is structured following best practices, making it well-suited for modern web applications requiring robust security and flexible API design.

## Project Structure

Here's a breakdown of the project structure:
```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── core
│   │   ├── config.py
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   └── middlewares.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── graphql
│   │   │   ├── __init__.py
│   │   │   ├── directives
│   │   │   │   ├── custom_directives.py
│   │   │   │   └── __init__.py
│   │   │   ├── middleware
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_middleware.py
│   │   │   │   └── logging_middleware.py
│   │   │   ├── resolvers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── document_resolvers.py
│   │   │   │   └── user_resolvers.py
│   │   │   ├── schema
│   │   │   │   ├── __init__.py
│   │   │   │   ├── mutations.py
│   │   │   │   ├── queries.py
│   │   │   │   ├── subscriptions.py
│   │   │   │   └── types
│   │   │   │       ├── __init__.py
│   │   │   │       ├── common_types.py
│   │   │   │       ├── document_types.py
│   │   │   │       └── user_types.py
│   │   │   └── subscriptions
│   │   │       ├── __init__.py
│   │   │       └── user_subscriptions.py
│   │   └── routers
│   │       ├── __init__.py
│   │       ├── auth_router.py
│   │       ├── document_router.py
│   │       └── user_router.py
│   ├── services
│   │   ├── aws
│   │   │   ├── __init__.py
│   │   │   ├── cognito
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── token_management.py
│   │   │   │   └── user_management.py
│   │   │   ├── dynamodb
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   ├── models
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── document_table.py
│   │   │   │   │   └── user_table.py
│   │   │   │   ├── services
│   │   │   │   │   ├── document_service.py
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── user_service.py
│   │   │   │   └── utils
│   │   │   │       ├── __init__.py
│   │   │   │       ├── query_utils.py
│   │   │   │       └── schema_validation.py
│   │   │   └── s3
│   │   │       ├── client.py
│   │   │       ├── file_operations.py
│   │   │       ├── __init__.py
│   │   │       └── utils
│   │   │           └── __init__.py
│   │   ├── __init__.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── file_utils.py
│   │       └── path_utils.py
│   └── tests
│       ├── README.md
│       ├── __init__.py
│       ├── api
│       │   ├── __init__.py
│       │   ├── graphql
│       │   │   ├── __init__.py
│       │   │   ├── resolvers
│       │   │   │   ├── __init__.py
│       │   │   │   ├── test_document_resolvers.py
│       │   │   │   └── test_user_resolvers.py
│       │   │   ├── schema
│       │   │   │   ├── __init__.py
│       │   │   │   ├── test_mutations.py
│       │   │   │   ├── test_queries.py
│       │   │   │   └── test_subscriptions.py
│       │   │   └── subscriptions
│       │   │       ├── __init__.py
│       │   │       └── test_user_subscriptions.py
│       │   └── routers
│       │       ├── __init__.py
│       │       ├── test_auth_router.py
│       │       ├── test_document_router.py
│       │       └── test_user_router.py
│       └── services
│           ├── aws
│           │   ├── cognito
│           │   │   ├── __init__.py
│           │   │   ├── test_auth.py
│           │   │   ├── test_token_management.py
│           │   │   └── test_user_management.py
│           │   ├── dynamodb
│           │   │   ├── __init__.py
│           │   │   ├── test_document_service.py
│           │   │   └── test_user_service.py
│           │   ├── __init__.py
│           │   └── s3
│           │       ├── __init__.py
│           │       └── test_file_operations.py
│           └── __init__.py
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Dockerfile.dev
├── Dockerfile.prod
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting Started

Follow these steps to get the project up and running in a development environment.

### Prerequisites

Ensure you have the following installed:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mojtaba-arvin/fastapi-authentication
   cd fastapi-authentication
   ```
2. **Build and start the development environment:**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```
   This command will:
    - Build the Docker image using the Dockerfile.dev.
    - Mount the project directory to the /app directory inside the container.
    - Expose the application on port 8000 with live reloading enabled.
3. **Access the application:**

    Open your web browser and go to http://localhost:8000. You should see a welcome message:

    `{"message": "Welcome to the FastAPI application!"}`

4. **Stopping the development environment:**
   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```





