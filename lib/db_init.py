from lib.generate_dummy import Session

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()