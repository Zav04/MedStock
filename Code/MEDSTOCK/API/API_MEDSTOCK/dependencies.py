from DATABASE.database import SessionLocal_MEDSTOCK

def get_db_MEDSTOCK():
    db = SessionLocal_MEDSTOCK()
    try:
        yield db
    finally:
        db.close()
