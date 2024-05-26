import logging
import avro.schema
import avro.datafile
import avro.io
from .database import SessionLocal

def setup_logging():
    logging.basicConfig(filename="logs/app.log", level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(message)s")

def log_error(error_message):
    logging.error(error_message)

def backup_table_to_avro(table_name: str, schema: dict):
    db = SessionLocal()
    try:
        data = db.query(table_name).all()
        file_path = f"backups/{table_name}.avro"
        with open(file_path, 'wb') as out:
            writer = avro.datafile.DataFileWriter(out, avro.io.DatumWriter(), schema)
            for row in data:
                writer.append(row.__dict__)
            writer.close()
        return file_path
    finally:
        db.close()

def restore_table_from_avro(table_name: str, schema: dict):
    db = SessionLocal()
    try:
        file_path = f"backups/{table_name}.avro"
        with open(file_path, 'rb') as avro_file:
            reader = avro.datafile.DataFileReader(avro_file, avro.io.DatumReader())
            for record in reader:
                table_name(**record)
                db.add(table_name(**record))
            db.commit()
            reader.close()
    finally:
        db.close()