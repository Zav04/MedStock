from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetRealocacoes/")
async def MedStock_GetRealocacoes(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_all_realocacoes();")
        result = db.execute(query).fetchall()
        realocacoes = []
        for row in result:
            realocacoes.append({
                "requerimento_origem": row[0],
                "requerimento_destino": row[1],
                "nome_consumivel": row[2],
                "quantidade": row[3],
                "data_redistribuicao": row[4].isoformat()
            })

        return {"response": True, "data": realocacoes}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {"response": False, "error": error_messages}