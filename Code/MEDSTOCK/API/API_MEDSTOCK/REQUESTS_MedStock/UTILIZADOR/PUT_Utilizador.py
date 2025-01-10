from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_Gestor_Sector import C_Gestor_Sector

router = APIRouter()

@router.put("/MedStock_AssociateUtilizadorToSector/")
async def MedStock_AssociateUserToSector(user:C_Gestor_Sector, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT update_utilizador_to_setor(:utilizador_id, :setor_id);")
        result = db.execute(query, {
            "utilizador_id": user.utilizador_id,
            "setor_id": user.setor_id
        })
        success = result.scalar()

        if success:
            db.commit()
            return {"response": True, "data": "Utilizador associado ao setor com sucesso e role alterada para 'Gestor Responsável'."}
        else:
            db.rollback()
            return {"response": False, "error": "Erro ao associar utilizador ao setor."}

    except SQLAlchemyError as e:
        db.rollback()
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        db.rollback()
        return {"response": False, "error": str(e)}
