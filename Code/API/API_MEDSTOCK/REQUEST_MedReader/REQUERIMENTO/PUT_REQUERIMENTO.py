from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from datetime import datetime
from dependencies import get_db_MEDSTOCK
from Models.C_Update_Requerimento_Preparacao import C_UpdateRequerimentoPreparacao
from Models.C_RequerimentoRequest import C_RequerimentoRequest
from REQUESTS_MedStock.REQUERIMENTO.POST_REQUERIMENTO import MedStock_SendEmailRequerimentoStatus

router = APIRouter()

@router.put("/MedReader_Update_Requerimento_Preparacao/")
async def MedStock_Update_Requerimento_Preparacao(
    payload: C_UpdateRequerimentoPreparacao, db=Depends(get_db_MEDSTOCK)
):
    try:
        query = text("SELECT update_requerimento_preparacao(:user_id, :requerimento_id);")
        
        params = {
            "user_id": payload.user_id,
            "requerimento_id": payload.requerimento_id
        }

        result = db.execute(query, params).scalar()

        if result:
            db.commit()

            email_request = C_RequerimentoRequest(requerimento_id=payload.requerimento_id)
            email_response = await MedStock_SendEmailRequerimentoStatus(email_request, db)

            if not email_response["response"]:
                return {
                    "response": False,
                    "error": f"Requerimento atualizado, mas houve erro no envio do e-mail: {email_response['error']}"
                }
            
            return {
                "response": True,
                "data": f"Requerimento {payload.requerimento_id} atualizado com sucesso."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": f"Falha ao atualizar o requerimento {payload.requerimento_id}."
            }
    except SQLAlchemyError as e:
        db.rollback()
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": f"Erro no banco de dados: {error_msg}"
        }
    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": f"Erro inesperado: {' '.join(error_messages)}"
        }
