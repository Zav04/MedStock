from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_CreateRequerimentoExterno import C_CreateRequerimentoExterno

router = APIRouter()

@router.post("/MedStock_CreateRequerimentoExterno/")
async def MedStock_CreateRequerimentoExterno(requerimentoexterno: C_CreateRequerimentoExterno, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("""
            SELECT create_requerimento_externo(:user_id_pedido, :paciente_nome, :paciente_estado);
        """)

        result = db.execute(query, {
            "user_id_pedido": requerimentoexterno.user_id_pedido,
            "paciente_nome": requerimentoexterno.paciente_nome,
            "paciente_estado": requerimentoexterno.paciente_estado,
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Externo criado com sucesso."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao criar o requerimento."
            }

    except SQLAlchemyError as e:
        db.rollback()
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