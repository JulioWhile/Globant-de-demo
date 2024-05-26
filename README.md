# Project Title

## Description
A FastAPI project to handle employee data with PostgreSQL, Docker, and AVRO backups.

## Installation
1. Clone the repository
2. Create a virtual environment: `poetry install`
3. Run Docker: `docker-compose up --build`

## API Endpoints
- POST /departments/
- POST /jobs/
- POST /employees/

## Backup and Restore
Backup: `backup_table_to_avro(table_name, schema)`
Restore: `restore_table_from_avro(table_name, schema)`

## Running Tests
`pytest`

## License
MIT
