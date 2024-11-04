from sqlalchemy.sql import text
from fastapi import APIRouter, Depends
from dependencies import get_db_MEDSTOCK
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()


@router.get("/Items/")
async def Get_Items(db = Depends(get_db_MEDSTOCK)):
    try:
        result = db.execute(text("SELECT nome_item, quantidade_disponivel from item;"))  
        result = [dict(row) for row in result.mappings().all()]
        return {"response": result}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig'])
        error_msg = error_msg.split('\n')[0]
        return {"error": error_msg}
    
    except Exception as e:
        return {"error": str(e)}

@router.get("/Item/{item_id}")
async def Get_Item_by_Id(item_id: int, db = Depends(get_db_MEDSTOCK)):
    try:
        result = db.execute(text(f"SELECT nome_item, quantidade_disponivel from item where item_id = {item_id};"))
        result = [dict(row) for row in result.mappings().all()]
        return {"response": result}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig'])
        error_msg = error_msg.split('\n')[0]
        return {"error": error_msg}
    
    except Exception as e:
        return {"error": str(e)}
