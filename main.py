from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas, utils
from app.database import SessionLocal, engine
from app.config import settings  # Import settings

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employees/", response_model=schemas.HiredEmployee)
def create_employee(employee: schemas.HiredEmployeeCreate, db: Session = Depends(get_db)):
    try:
        db_employee = crud.create_employee(db, employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_employee


def process_in_batches(db, items, model, batch_size):
    total = len(items)
    successful_inserts = 0

    for i in range(0, total, batch_size):
        batch = items[i:i + batch_size]
        try:
            db_items = [model(**item.dict()) for item in batch]
            db.add_all(db_items)
            db.commit()
            successful_inserts += len(db_items)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    return successful_inserts


@app.post("/employees/batch/")
def create_employees_batch(employees: List[schemas.HiredEmployeeCreate], db: Session = Depends(get_db)):
    batch_size = settings.BATCH_SIZE
    successful_inserts = process_in_batches(db, employees, models.HiredEmployee, batch_size)

    return {
        "status": "Batch insert completed",
        "successful_inserts": successful_inserts,
        "failed_inserts": len(employees) - successful_inserts
    }


@app.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    try:
        db_department = crud.create_department(db, department)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_department


@app.post("/departments/batch/")
def create_departments_batch(departments: List[schemas.DepartmentCreate], db: Session = Depends(get_db)):
    batch_size = settings.BATCH_SIZE
    successful_inserts = process_in_batches(db, departments, models.Department, batch_size)

    return {
        "status": "Batch insert completed",
        "successful_inserts": successful_inserts,
        "failed_inserts": len(departments) - successful_inserts
    }


@app.post("/jobs/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    try:
        db_job = crud.create_job(db, job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_job


@app.post("/jobs/batch/")
def create_jobs_batch(jobs: List[schemas.JobCreate], db: Session = Depends(get_db)):
    batch_size = settings.BATCH_SIZE
    successful_inserts = process_in_batches(db, jobs, models.Job, batch_size)

    return {
        "status": "Batch insert completed",
        "successful_inserts": successful_inserts,
        "failed_inserts": len(jobs) - successful_inserts
    }


@app.post("/backup/")
def backup_tables():
    try:
        utils.backup_all_tables()
        return {"status": "Backup completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/restore/")
def restore_tables():
    try:
        utils.restore_all_tables()
        return {"status": "Restore completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
