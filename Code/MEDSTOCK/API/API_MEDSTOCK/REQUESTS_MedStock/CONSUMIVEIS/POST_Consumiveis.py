from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_ConsumivelCreateRequest import C_ConsumivelCreateRequest

router = APIRouter()

@router.post("/MedStock_CreateConsumivel/")
async def MedStock_CreateConsumivel(request: C_ConsumivelCreateRequest, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("""
            SELECT create_consumivel(:p_nome_consumivel, :p_codigo, :p_tipo_id);
        """)

        result = db.execute(query, {
            "p_nome_consumivel": request.nome_consumivel,
            "p_codigo": request.codigo,
            "p_tipo_id": request.tipo_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {"response": True, "data": "Consumível criado com sucesso."}
        else:
            db.rollback()
            return {"response": False, "error": "Erro ao criar o consumível."}

    except SQLAlchemyError as e:
        db.rollback()
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        db.rollback()
        return {"response": False, "error": str(e)}