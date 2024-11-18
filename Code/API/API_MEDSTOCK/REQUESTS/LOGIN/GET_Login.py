from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetUserByEmail/")
async def MedStock_GetUserByEmail(email: str, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_user_by_email(:email);")
        
        result = db.execute(query, {"email": email}).fetchone()
        
        if not result:
            return {
                "response": False,
                "error": f"O utilizador com o email '{email}' não encontrado."
            }

        user_data = {
            "utilizador_id": result.utilizador_id,
            "nome": result.nome,
            "email": result.email,
            "sexo": result.sexo,
            "data_nascimento": result.data_nascimento,
            "role_id": result.role_id,
            "role_nome": result.role_nome,
        }

        return {
            "response": True,
            "data": user_data
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
