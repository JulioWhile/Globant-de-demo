import os
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, crud

# Create the database tables
models.Base.metadata.create_all(bind=engine)

def load_departments(db: Session, csv_file: str):
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        department = schemas.DepartmentCreate(department=row['department'])
        crud.create_department(db, department)

def load_jobs(db: Session, csv_file: str):
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        job = schemas.JobCreate(job=row['job'])
        crud.create_job(db, job)

def load_employees(db: Session, csv_file: str):
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        employee = schemas.HiredEmployeeCreate(
            name=row['name'],
            datetime=row['datetime'],
            department_id=row['department_id'],
            job_id=row['job_id']
        )
        try:
            crud.create_employee(db, employee)
        except ValueError as e:
            print(f"Error inserting employee {row['name']}: {e}")

def main():
    db: Session = SessionLocal()
    try:
        load_departments(db, 'data/departments.csv')
        load_jobs(db, 'data/jobs.csv')
        load_employees(db, 'data/hired_employees.csv')
    finally:
        db.close()

if __name__ == "__main__":
    main()
