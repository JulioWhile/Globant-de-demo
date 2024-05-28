import pandas as pd
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)


def load_departments(db: Session, csv_file: str):
    df = pd.read_csv(csv_file, header=None, names=["id", "department"], dtype={"id": int})

    # Debugging: Print the first few rows of the dataframe
    print("Departments DataFrame:")
    print(df.head())

    for _, row in df.iterrows():
        department = schemas.DepartmentCreate(department=row["department"])
        crud.create_department(db=db, department=department)


def load_jobs(db: Session, csv_file: str):
    df = pd.read_csv(csv_file, header=None, names=["id", "job"], dtype={"id": int})

    # Debugging: Print the first few rows of the dataframe
    print("Jobs DataFrame:")
    print(df.head())

    for _, row in df.iterrows():
        job = schemas.JobCreate(job=row["job"])
        crud.create_job(db=db, job=job)


def load_employees(db: Session, csv_file: str):
    df = pd.read_csv(csv_file, header=None, names=["id", "name", "datetime", "department_id", "job_id"],
                     dtype={"id": int})

    # Debugging: Print the first few rows of the dataframe
    print("Hired Employees DataFrame:")
    print(df.head())

    for _, row in df.iterrows():
        try:
            # Create an instance of the Pydantic schema
            employee_data = schemas.HiredEmployeeCreate(
                id=row["id"],
                name=row["name"],
                datetime=row["datetime"],
                department_id=row["department_id"],
                job_id=row["job_id"]
            )

            # Use the CRUD function to create the employee in the database
            crud.create_employee(db, employee_data)
        except ValidationError as e:
            print(f"Validation error for row {row['id']}: {e}")
        except ValueError as e:
            print(f"Value error for row {row['id']}: {e}")


def main():
    db: Session = SessionLocal()
    try:
        load_departments(db, "data/departments.csv")
        load_jobs(db, "data/jobs.csv")
        load_employees(db, "data/hired_employees.csv")
    finally:
        db.close()


if __name__ == "__main__":
    main()
