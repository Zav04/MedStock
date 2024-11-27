from sqlalchemy.sql import text
from fastapi import Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK
from Models.C_Reset_Password import C_ResetPassword
from Firebase.FireBase import resetpassword

router = APIRouter()

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends

@router.post("/MedStock_Reset_Password/")
async def MedStock_Reset_Password(Reset_Email: C_ResetPassword, db=Depends(get_db_MEDSTOCK)):
    try:
        # Define a query com um placeholder para o email
        query = text("SELECT verify_exist_email(:email);")
        # Executa a query e passa o email do usuário como parâmetro
        result = db.execute(query, {"email": Reset_Email.email})
        status = result.scalar()
        
        if status == False:
            return {
                "response": status,
                "error": "Email inserido não registado"
                }
        else:
            result = resetpassword(Reset_Email.email)            
        if result == False :
            return {
                "response": status,
                "error": "Credenciais Invalidas"
                }
        return {"response": result, "data": "Email enviado com sucesso"}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False,"error": error_msg}
    
    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {"response": False,"error": error_messages}
