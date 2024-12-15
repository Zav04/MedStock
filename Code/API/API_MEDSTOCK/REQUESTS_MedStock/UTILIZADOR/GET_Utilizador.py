from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetAllUsers/")
async def MedStock_GetAllUsers(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_all_utilizadores();")
        result = db.execute(query).fetchall()

        users = []
        for row in result:
            user = {
                "utilizador_id": row.utilizador_id,
                "nome": row.nome,
                "email": row.email,
                "sexo": row.sexo,
                "data_nascimento": row.data_nascimento,
                "role_id": row.role_id,
                "role_nome": row.role_nome
            }
            users.append(user)

        return {
            "response": True,
            "data": users
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
        


@router.get("/MedStock_GetUtilizadoresComSetores/")
async def MedStock_GetUtilizadoresComSetores(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_utilizadores_com_setores_alocados();")
        result = db.execute(query).fetchall()

        utilizadores = []
        for row in result:
            utilizador = {
                "utilizador_id": row.utilizador_id,
                "nome": row.nome,
                "nome_setor": row.nome_setor,
                "localizacao": row.localizacao
            }
            utilizadores.append(utilizador)
        
        return {
            "response": True,
            "data": utilizadores
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

