# Globant Demo Project

This project is a demonstration of a FastAPI application for managing departments, jobs, and hired employees. The
application supports RESTful API endpoints for creating, reading, updating, and deleting records. Additionally, it
provides functionality for backing up and restoring data using AVRO format, as well as batch insertion of data.

## Table of Contents

- [Globant Demo Project](#globant-demo-project)
    - [Table of Contents](#table-of-contents)
    - [Features](#features)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Usage](#usage)
        - [Running the Server](#running-the-server)
        - [API Endpoints](#api-endpoints)
        - [Batch Operations](#batch-operations)
        - [Backup and Restore](#backup-and-restore)
    - [Project Structure](#project-structure)
    - [License](#license)

## Features

- CRUD operations for departments, jobs, and hired employees.
- Batch insertion of records (1 up to 1000 rows).
- Backup and restore functionality using AVRO format.
- Validation of data against predefined schemas.

## Requirements

- Python 3.10+
- Poetry
- PostgreSQL (or another supported database)
- FastAPI
- SQLAlchemy
- Pydantic
- Avro
- Fastavro

## Project Structure

```css
globant-demo
│
├── app
│ ├── __init__.py
│ ├── crud.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ └── utils.py
│
├── main.py
├── read_avro.py
├── README.md
└── pyproject.toml
```

- `app/`: Contains the main application files.
    - `crud.py`: Contains the CRUD operations.
    - `database.py`: Database setup and session management.
    - `models.py`: SQLAlchemy models.
    - `schemas.py`: Pydantic models (schemas).
    - `utils.py`: Utility functions for backup and restore.
- `main.py`: Entry point for the FastAPI application.
- `read_avro.py`: Script to read AVRO files.
- `README.md`: Project documentation.
- `pyproject.toml`: Poetry configuration file.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/globant-demo.git
   cd globant-demo
   ```

2. Install dependencies using Poetry:

   ```sh
   poetry install
   ```

3. Set up the database:

    - Configure your database settings in `app/database.py`.
    - You should be already running the server.
    - Create the database tables:

      ```sh
      poetry run python -m app.database
      ```

## Usage

### Running the Server

Start the FastAPI server using Uvicorn:

```sh
poetry run uvicorn main:app --reload
```

### Backup and Restore

- **Backup all tables:**

  ```sh
  curl -X POST "http://127.0.0.1:8000/backup/"
  ```

- **Restore all tables:**

  ```sh
  curl -X POST "http://127.0.0.1:8000/restore/"
  ```

The backup files are saved in the `backups` directory in AVRO format.

### API Endpoints

The following endpoints are available:

- **Departments**
    - `GET /departments/`: Get a list of departments.
    - `POST /departments/`: Create a new department.
    - `POST /departments/batch/`: Create multiple departments in a batch.

- **Jobs**
    - `GET /jobs/`: Get a list of jobs.
    - `POST /jobs/`: Create a new job.
    - `POST /jobs/batch/`: Create multiple jobs in a batch.

- **Hired Employees**
    - `GET /employees/`: Get a list of hired employees.
    - `POST /employees/`: Create a new hired employee.
    - `POST /employees/batch/`: Create multiple hired employees in a batch.

### Batch Operations

Batch operations allow you to insert multiple records in a single request. The batch endpoints accept a list of records
to insert.

Example request for creating multiple departments:

- POST /departments/batch/

```json
[
  {
    "job": "Data Engineer"
  },
  {
    "job": "Software Engineer"
  }
]
```

Example request for creating multiple jobs:

- POST /jobs/batch/

```json
[
  {
    "department": "Engineering"
  },
  {
    "department": "Sales"
  }
]
```

Example request for creating multiple employees:

- POST /employees/batch/

```json
[
  {
    "id": 1001,
    "name": "Jane Doe",
    "datetime": "2021-07-27T16:02:08Z",
    "department_id": 1,
    "job_id": 2
  },
  {
    "id": 1002,
    "name": "Jim Beam",
    "datetime": "2021-07-27T16:02:08Z",
    "department_id": 1,
    "job_id": 2
  }
]
```

### Reading AVRO Files

Use the `read_avro.py` script to read and print the contents of AVRO files:

1. Run the script with the path to the AVRO file:

   ```sh
   poetry run python read_avro.py backups/<avro_file_name>.avro
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

