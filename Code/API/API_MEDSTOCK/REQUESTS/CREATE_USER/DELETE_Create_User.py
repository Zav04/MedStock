from sqlalchemy.sql import text
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db_MEDSTOCK
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()


@router.delete("/Delete_User/{user_id}")
async def Delete_User(user_id: int, db = Depends(get_db_MEDSTOCK)):
    try:
        # Verificar se o utilizador existe
        result = db.execute(text("SELECT * FROM utilizador WHERE utilizador_id = :user_id"), {"user_id": user_id}).fetchone()
        
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Remover utilizador
        db.execute(text("DELETE FROM utilizador WHERE utilizador_id = :user_id"), {"user_id": user_id})
        db.commit()

        return {"message": "User deleted successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()
        error_msg = str(e.__dict__['orig'])
        error_msg = error_msg.split('\n')[0]
        return {"error": error_msg}
    
    except Exception as e:
        db.rollback()
        return {"error": str(e)}