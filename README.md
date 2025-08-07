# Project README

Welcome to our project! This repository contains the source code for a Python-based web application designed using FastAPI, SQLModel, and Docker. Below you'll find detailed instructions on setting up your development environment, running the application, and performing tests.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)

---

## Project Overview

This project is a web application built using Python's FastAPI framework for handling HTTP requests and SQLModel for database operations. The application supports user registration, organization management, and token-based authentication. The infrastructure is containerized using Docker, ensuring consistency across different environments.

---

## Prerequisites

Before getting started, ensure you have the following installed on your machine:

- Docker & Docker Compose (`docker-compose`)
- Git (`git`)

---

## Getting Started

To set up and run the project locally, follow these steps:

### Clone the Repository

```bash
git clone <https://github.com/ParzivalXIII/inventory-management-system>
cd <src>
```

### Build and Run Docker Containers

To build and run the application along with its dependencies, execute the following command:

```bash
docker-compose up --build
```

This command will build the Docker images specified in `Dockerfile`, create necessary containers, and start the application.

---

## Running the Application

Once Docker containers are up and running, you can access the application via:

```
http://localhost:8000
```

For API documentation and testing, navigate to:

```
http://localhost:8000/docs
```

This will open the Swagger UI interface where you can explore and interact with the available APIs.

---

## Running Tests

To run the unit tests, you can use the predefined session fixture in `src/tests/test_src.py`. Execute the following command within the Docker container:

```bash
pytest src/tests/
```

This will run all tests found in the `src/tests/` directory. Ensure the application is stopped while running tests to avoid conflicts.

---

## Configuration

The application configuration is managed through environment variables, which can be set either directly or via a `.env` file. The default location for the `.env` file is expected to be in the same directory as `src/core/config.py`.

You can customize the settings by creating a `test.env` file:

```plaintext
SECRET_KEY=mysecretkey
DATABASE_URL=sqlite:///./test.db
```

Refer to `src/core/config.py` for a list of all configurable parameters.

---

## Directory Structure

Here's a brief overview of the project's directory structure:

```
project_root/
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── auth/
│   │   └── router.py
│   |   └── dependencies.py
|   |   └── utils.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models.py
│   ├── main.py
|   ├── router.py
|   ├── schemas.py
|   ├── crud.py
│   └── tests/
│       └── test_src.py
|       └── test_auth.py
└── README.md
└── requirements.txt
└── pyproject.toml
└── *.env

```

- **Dockerfile**: Defines the Docker image for building and running the application.
- **docker-compose.yml**: Orchestrates the Docker services.
- **src/**: Contains the application source code.
  - **auth/**: Handles user authentication and authorization.
  - **core/**: Includes core configurations and database utilities.
  - **models.py**: Defines database models using SQLModel.
  - **main.py**: Entry point of the application.
  - **tests/**: Contains test cases for the application.
- **README.md**: This file providing setup and usage instructions.

---

## Contributing

We welcome contributions to improve and expand the project. Please follow these guidelines when contributing:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes and commit them with descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request detailing the changes made.

Thank you for your interest in this project! If you encounter any issues or have suggestions, feel free to open an issue on the GitHub repository.

---

## Author

This project was created and is maintained by https://github.com/ParzivalXIII. You can contact me via Twitter [@ParzivalXIII].

If you have any questions, feedback, or would like to contribute, please don't hesitate to reach out!