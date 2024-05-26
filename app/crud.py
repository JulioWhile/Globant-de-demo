from sqlalchemy.orm import Session
from . import models, schemas

def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_employee(db: Session, employee_id: int):
    return db.query(models.HiredEmployee).filter(models.HiredEmployee.id == employee_id).first()

def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(department=department.department)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(job=job.job)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def create_employee(db: Session, employee: schemas.HiredEmployeeCreate):
    db_employee = get_employee(db, employee_id=employee.id)
    if db_employee:
        raise ValueError(f"Employee with id {employee.id} already exists")

    db_employee = models.HiredEmployee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
