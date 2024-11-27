from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_CreateRequerimento import C_CreateRequerimento
import json

router = APIRouter()


@router.post("/MedStock_CreateRequerimento/")
async def MedStock_CreateRequerimento(requerimento: C_CreateRequerimento, db=Depends(get_db_MEDSTOCK)):
    try:
        items_json = json.dumps([item.model_dump() for item in requerimento.requerimento_items or []])

        query = text("""
            SELECT create_requerimento(:user_id_pedido, :setor_id, :items_list, :urgente);
        """)

        result = db.execute(query, {
            "user_id_pedido": requerimento.user_id_pedido,
            "setor_id": requerimento.setor_id,
            "items_list": items_json,
            "urgente": requerimento.urgente
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento criado com sucesso."
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
