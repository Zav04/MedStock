from sqlalchemy.sql import text
from fastapi import Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK
from Models.Login import C_Login
from Firebase.FireBase import login

router = APIRouter()

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends

@router.post("/MedStock_Login/")
async def MedStock_Login(user: C_Login, db=Depends(get_db_MEDSTOCK)):
    try:
        # Define a query com um placeholder para o email
        query = text("SELECT verify_exist_email(:email);")
        # Executa a query e passa o email do usuário como parâmetro
        result = db.execute(query, {"email": user.email})
        status = result.scalar()
        
        if status == False:
            return {
                "response": status,
                "error": "Email inserido não registado"
                }
        else:
            result = login(user.email, user.password)            
        if result == False :
            return {
                "response": result,
                "error": "Credenciais Invalidas"
                }
            
        return {
            "response": True,
            "data": result
            }
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": error_msg
            }
    
    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": error_messages
            }
