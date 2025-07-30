# Core Repository

This project is a Flask-based API for managing Formula 1 data, including seasons, drivers, circuits, constructors, races, and results. It uses SQLAlchemy for ORM and Flask-Migrate for database migrations. The application is containerized using Docker for easy setup and deployment.

## Features

- RESTful API built with Flask
- SQLAlchemy models for F1 data
- Database migrations with Flask-Migrate
- Dockerized for local development

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.12+ for local development

## Environment Setup

1. **Create virtual environment**
    - MacOS / Linux
    ```sh
    python3 -m venv venv
    ```
    - windows
    ```sh
    python -m venv venv
    ```
2. **Activate the environment**
    - macOS / Linux
    ```sh
    source venv/bin/activate
    ```
    check if you are in the right environment:
    ```sh
    which python
    ```
    should show python in in project_root/venv/bin

    - windows
    ```sh
    venv\Scripts\activate
    ```
    check if you are in the right environment:
    ```sh
    where.exe python
    ```
    should show python in in project_root/venv/Scripts

3. **Install required modules from requirements.txt**
    make sure to have project root as the working directory
    ```sh
    pip install -r requirements.txt
    ```

### Running local version of the app


1. **Start the server**
    - macOS / Linux
    ```sh
    python3 run.py
    ```

    - windows
    ```sh
    python run.py
    ```


### Running with Docker Compose

1. **Start the services:**
    ```sh
    docker-compose up -d
    ```
    This will build and start the Flask app and the database.

### Running Migrations

1. **Run migrations:**
    ```sh
    flask db upgrade
    ```

   - To generate a new migration after changing models:
     ```sh
     flask db migrate -m "Describe your change"
     flask db upgrade
     ```

### Running ruff linter

1. **Run ruff to check code style and linting:**
    ```sh
    ruff check .
    ```

2. **Run ruff and automatically fix issues:**
    ```sh
    ruff check . --fix
    ```

## License

MIT License