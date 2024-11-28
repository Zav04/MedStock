from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedReader_Requerimentos/")
async def get_requerimentos(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_requerimentos_for_medreader();")
        result = db.execute(query).fetchall()
        requerimentos = []
        for row in result:
            requerimentos.append({
                "requerimento_id": row.requerimento_id,
                "urgente": row.urgente,
                "itens_pedidos": row.itens_pedidos
            })

        return {
            "response": True,
            "data": requerimentos
        }

    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": f"Erro no banco de dados: {error_msg}"
        }
    except Exception as e:
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": f"Erro inesperado: {' '.join(error_messages)}"
        }
