from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from dependencies import get_db_MEDSTOCK
from Models.C_Update_Consumivel import C_Update_Consumivel
from Models.C_UpdateStockConsumiveis import C_UpdateStockConsumiveis
import json

router = APIRouter()

@router.put("/MedStock_UpdateConsumivel/")
async def MedStock_UpdateConsumivel(consumivel:C_Update_Consumivel,db=Depends(get_db_MEDSTOCK)
):
    try:
        query = text("""
            SELECT update_consumivel(
                :consumivel_id,
                :quantidade_minima,
                :quantidade_pedido
            ) AS success;
        """)
        
        result = db.execute(
            query, {
                "consumivel_id": consumivel.consumivel_id,
                "quantidade_minima": consumivel.quantidade_minima,
                "quantidade_pedido": consumivel.quantidade_pedido
            }
        ).fetchone()

        if result.success:
            db.commit()
            return {
                "response": True,
                "message": "Consumível atualizado com sucesso!"
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Nenhuma linha foi atualizada. Verifique o ID fornecido."
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
        return {"response": False, "error": error_messages}
    
    
@router.put("/MedStock_UpdateStock/")
async def MedStock_UpdateStock(stock_update: C_UpdateStockConsumiveis, db=Depends(get_db_MEDSTOCK)
):
    try:
        items_json = json.dumps([item.model_dump() for item in stock_update.consumiveis or []])
        
        
        query = text("""
            SELECT update_stock_consumiveis(:consumiveis::JSON);
        """)
        
        result = db.execute(
            query, {"consumiveis": items_json}
        ).fetchone()

        if result.success:
            db.commit()
            return {
                "response": True,
                "message": "Stock atualizado com sucesso!"
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao atualizar o Stock. Verifique os dados fornecidos."
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
        return {"response": False, "error": error_messages}
