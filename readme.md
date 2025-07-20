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
- (Optional) Python 3.8+ for local development

### Running local version of the app

1. **Start the server**
    - macbook
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
    docker-compose up --build
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

## License

MIT License