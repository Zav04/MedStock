from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetConsumiveis/")
async def MedStock_GetConsumiveis(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_consumiveis_details();")
        result = db.execute(query).fetchall()
        
        items = []
        for row in result:
            (
                consumivel_id,
                nome_consumivel, 
                nome_tipo, 
                codigo, 
                quantidade_total, 
                quantidade_alocada, 
                quantidade_minima, 
                quantidade_pedido
            ) = row
            
            items.append({
                "consumivel_id":consumivel_id,
                "nome_consumivel": nome_consumivel,
                "nome_tipo": nome_tipo,
                "codigo": codigo,
                "quantidade_total": quantidade_total,
                "quantidade_alocada": quantidade_alocada,
                "quantidade_minima": quantidade_minima,
                "quantidade_pedido": quantidade_pedido,
            })

        return {"response": True, "data": items}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {"response": False, "error": error_messages}



@router.get("/MedStock_GetAllTipoConsumiveis/")
async def MedStock_GetAllTipoConsumiveis(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_all_tipo_consumiveis();")
        result = db.execute(query).fetchall()

        tipos = []
        for row in result:
            tipo_id, nome_tipo = row
            
            tipos.append({
                "tipo_id": tipo_id,
                "nome_tipo": nome_tipo,
            })

        return {"response": True, "data": tipos}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        error_messages = [str(arg) for arg in e.args]
        return {"response": False, "error": error_messages}
