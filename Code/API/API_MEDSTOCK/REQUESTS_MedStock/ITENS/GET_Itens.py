from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetItems/")
async def MedStock_GetItems(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_item_details();")
        result = db.execute(query).fetchall()
        
        items = []
        for row in result:
            item_id,nome_item, nome_tipo, codigo, quantidade_disponivel = row
            items.append({
                "item_id": item_id,
                "nome_item": nome_item,
                "nome_tipo": nome_tipo,
                "codigo": codigo,
                "quantidade_disponivel": quantidade_disponivel
            })

        return {"response": True, "data": items}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {"response": False, "error": error_messages}
