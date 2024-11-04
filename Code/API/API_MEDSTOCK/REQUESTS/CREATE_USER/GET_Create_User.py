from sqlalchemy.sql import text
from fastapi import APIRouter, Depends
from dependencies import get_db_MEDSTOCK
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()


@router.get("/Users/")
async def Get_Users(db = Depends(get_db_MEDSTOCK)):
    try:
        result = db.execute(text("SELECT * from utilizador;"))
        result = [dict(row) for row in result.mappings().all()]
        return {"response": result}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig'])
        error_msg = error_msg.split('\n')[0]
        return {"error": error_msg}
    
    except Exception as e:
        return {"error": str(e)}
