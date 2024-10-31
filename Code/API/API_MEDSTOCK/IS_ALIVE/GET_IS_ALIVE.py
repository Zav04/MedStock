from sqlalchemy.sql import text
from fastapi import Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/Is_Alive/")
async def Is_Alive(db = Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT Is_Alive();")
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
