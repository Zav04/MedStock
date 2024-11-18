from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetSectors/")
async def MedStock_GetSectors(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_all_sectors();")
        result = db.execute(query).fetchall()
        sectors = []
        for row in result:
            sector = {
                "setor_id": row.setor_id,
                "nome_setor": row.nome_setor,
                "localizacao": row.localizacao
            }
            sectors.append(sector)
        
        return {
            "response": True,
            "data": sectors
        }

    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": error_msg
        }

    except Exception as e:
        return {
            "response": False,
            "error": str(e)
        }
