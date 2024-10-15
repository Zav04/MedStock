from sqlalchemy.sql import text
from fastapi import Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK
from Models.IsAlive import IsAlive

router = APIRouter()

@router.put("/IsAlive/")
async def is_alive(db = Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT IsAlive();")
        result = db.execute(query)
        alive_status = result.scalar()
        return {"response": alive_status}
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig'])
        error_msg = error_msg.split('\n')[0]
        return {"error": error_msg}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
