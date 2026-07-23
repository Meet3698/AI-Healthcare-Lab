from app.database.database import SessionLocal
from app.tools.medical_records_tool import (
    get_patient_records
)


db = SessionLocal()


records = get_patient_records(
    patient_id=1,
    db=db
)


print(records)


db.close()