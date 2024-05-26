import json
import logging
import os
from datetime import datetime

import avro.datafile
import avro.io
import avro.schema

from app.database import SessionLocal
from app.models import Department, Job, HiredEmployee

# Ensure the backups directory exists
os.makedirs('backups', exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define schema dictionaries
department_schema_dict = {
    "type": "record",
    "name": "Department",
    "fields": [{"name": "id", "type": "int"}, {"name": "department", "type": "string"}]
}

job_schema_dict = {
    "type": "record",
    "name": "Job",
    "fields": [{"name": "id", "type": "int"}, {"name": "job", "type": "string"}]
}

hired_employee_schema_dict = {
    "type": "record",
    "name": "HiredEmployee",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "datetime", "type": "string"},
        {"name": "department_id", "type": "int"},
        {"name": "job_id", "type": ["int", "null"]}
    ]
}

# Convert dictionaries to JSON strings and then to AVRO schema objects
department_schema = avro.schema.Parse(json.dumps(department_schema_dict))
job_schema = avro.schema.Parse(json.dumps(job_schema_dict))
hired_employee_schema = avro.schema.Parse(json.dumps(hired_employee_schema_dict))

def backup_table_to_avro(table, schema):
    db = SessionLocal()
    try:
        data = db.query(table).all()
        file_path = f"backups/{table.__tablename__}.avro"
        with open(file_path, 'wb') as out:
            writer = avro.datafile.DataFileWriter(out, avro.io.DatumWriter(), schema)
            for row in data:
                # Filter out SQLAlchemy internal attributes and convert datetime to string
                filtered_row = {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in row.__dict__.items() if not k.startswith('_')}
                logging.info(f"Backing up record: {filtered_row}")
                writer.append(filtered_row)
            writer.close()
        logging.info(f"Backed up {len(data)} records from {table.__tablename__} to {file_path}")
        return file_path
    finally:
        db.close()

def restore_table_from_avro(table, schema):
    db = SessionLocal()
    try:
        file_path = f"backups/{table.__tablename__}.avro"
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            logging.error(f"Backup file {file_path} does not exist or is empty.")
            return

        with open(file_path, 'rb') as avro_file:
            reader = avro.datafile.DataFileReader(avro_file, avro.io.DatumReader())
            count = 0
            for record in reader:
                logging.info(f"Restoring record: {record}")
                # Convert datetime back to datetime object if needed
                if 'datetime' in record:
                    record['datetime'] = datetime.fromisoformat(record['datetime'])
                db.add(table(**record))
                count += 1
            db.commit()
            reader.close()
        logging.info(f"Restored {count} records to {table.__tablename__} from {file_path}")
    except Exception as e:
        logging.error(f"Error restoring {table.__tablename__} from AVRO: {str(e)}")
        raise e
    finally:
        db.close()

def backup_all_tables():
    logging.info("Starting backup of all tables.")
    backup_table_to_avro(Department, department_schema)
    backup_table_to_avro(Job, job_schema)
    backup_table_to_avro(HiredEmployee, hired_employee_schema)
    logging.info("Backup of all tables completed.")

def restore_all_tables():
    logging.info("Starting restore of all tables.")
    restore_table_from_avro(Department, department_schema)
    restore_table_from_avro(Job, job_schema)
    restore_table_from_avro(HiredEmployee, hired_employee_schema)
    logging.info("Restore of all tables completed.")
