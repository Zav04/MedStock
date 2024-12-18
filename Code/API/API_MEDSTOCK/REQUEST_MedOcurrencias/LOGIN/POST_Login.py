from REQUESTS_MedStock.LOGIN.POST_Login import MedStock_Login
from REQUESTS_MedStock.LOGIN.GET_Login import MedStock_GetUserByEmail
from fastapi import Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK
from Models.C_Login import C_Login

router = APIRouter()

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends



@router.post("/MedOcurrencias_Login/")
async def MedStock_ValidateAndFetchUser(user: C_Login, db=Depends(get_db_MEDSTOCK)):
    try:
        login_verification_response = await MedStock_Login(user, db)
        
        if not login_verification_response.get("response", False):
            return {
                "response": False,
                "error": "Erro ao verificar o login: Credenciais inválidas ou email não registrado."
            }
        email = user.email
        user_data_response = await MedStock_GetUserByEmail(email, db)
        
        if not user_data_response.get("response", False):
            return {
                "response": False,
                "error": "Erro ao obter os dados do Utilizador."
            }
        if user_data_response["data"]["role_nome"] != "Serviço Externo":
            return {
                "response": False,
                "error": "Erro ao verificar o login: Utilizador não é um Serviço Externo."
            }
        else:
            return {
            "response": True,
            "data": user_data_response["data"]
        }
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": f"Erro na base de dados: {error_msg}"
        }
    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": f"Erro inesperado: {' '.join(error_messages)}"
        }
