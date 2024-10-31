from sqlalchemy.sql import text
from fastapi import Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK
from Models.Login import C_Login
from Firebase.FireBase import login

router = APIRouter()

@router.post("/MedStock_Login/")
async def MedStock_Login(user:C_Login, db = Depends(get_db_MEDSTOCK)):
    try:
        result = login(user.email,user.password)
        if(result=="Credenciais Invalidas"):
            return {"error": result}
        return {"response": result}
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig'])
        error_msg = error_msg.split('\n')[0]
        return {"error": error_msg}
    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {"error": error_messages}