from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from dependencies import get_db_MEDSTOCK
from Models.C_SetorCreateRequest import C_SetorCreateRequest

router = APIRouter()
@router.post("/MedStock_CreateSetorHospitalar/")
async def MedStock_CreateSetorHospitalar(setor: C_SetorCreateRequest, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT create_setor_hospitalar(:p_nome_setor, :p_localizacao);
        """)
        result = db.execute(query, {
            "p_nome_setor": setor.nome_setor,
            "p_localizacao": setor.localizacao
        })

        success = result.scalar()

        if success:
            db.commit()
            return {"response": True, "data": "Setor hospitalar criado com sucesso."}
        else:
            db.rollback()
            return {"response": False, "error": "Erro ao criar setor hospitalar."}

    except SQLAlchemyError as e:
        db.rollback()
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        db.rollback()
        error_msg = [str(arg) for arg in e.args]
        return {"response": False, "error": error_msg}
