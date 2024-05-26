from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas, utils
from app.database import SessionLocal, engine

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

@app.post("/employees/batch/")
def create_employees_batch(employees: List[schemas.HiredEmployeeCreate], db: Session = Depends(get_db)):
    successful_inserts = []
    failed_inserts = []

    for employee in employees:
        try:
            db_employee = crud.create_employee(db, employee)
            successful_inserts.append(db_employee)
        except ValueError as e:
            failed_inserts.append({"employee": employee.dict(), "error": str(e)})

    return {
        "status": "Batch insert completed",
        "successful_inserts": len(successful_inserts),
        "failed_inserts": failed_inserts
    }

@app.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    try:
        db_department = crud.create_department(db, department)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_department

@app.post("/jobs/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    try:
        db_job = crud.create_job(db, job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_job

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
