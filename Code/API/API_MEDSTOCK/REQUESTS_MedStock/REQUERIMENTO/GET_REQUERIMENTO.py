from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetRequerimentosByUser/")
async def MedStock_GetRequerimentosByUser(user_id: int, db = Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_requerimentos_by_user(:user_id);")
        result = db.execute(query, {"user_id": user_id}).fetchall()
        
        requerimentos = []
        for row in result:
            requerimento = {
                "requerimento_id": row.requerimento_id,
                "setor_nome_localizacao": row.setor_nome_localizacao,
                "nome_utilizador_pedido": row.nome_utilizador_pedido,
                "status": row.status,
                "urgente": row.urgente,
                "itens_pedidos": row.itens_pedidos,
                "data_pedido": row.data_pedido,
                "historico": row.historico
            }
            requerimentos.append(requerimento)
        
        return {
            "response": True,
            "data": requerimentos
        }

    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": error_msg
        }

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": error_messages
        }

@router.get("/MedStock_GetRequerimentosByFarmaceutico/")
async def MedStock_GetRequerimentosByFarmaceutico(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_requerimentos_by_farmaceutico();")
        result = db.execute(query).fetchall()
        
        requerimentos = []
        for row in result:
            requerimento = {
                "requerimento_id": row.requerimento_id,
                "setor_nome_localizacao": row.setor_nome_localizacao,
                "nome_utilizador_pedido": row.nome_utilizador_pedido,
                "status": row.status,
                "urgente": row.urgente,
                "itens_pedidos": row.itens_pedidos,
                "data_pedido": row.data_pedido,
                "historico": row.historico
            }
            requerimentos.append(requerimento)
        
        return {
            "response": True,
            "data": requerimentos
        }

    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": error_msg
        }

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": error_messages
        }


@router.get("/MedStock_GetRequerimentosByResponsavel/")
async def MedStock_GetRequerimentosByResponsavel(responsavel_id: int, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT * FROM get_requerimentos_by_responsavel(:responsavel_id);")
        
        result = db.execute(query, {"responsavel_id": responsavel_id}).fetchall()
        
        requerimentos = []
        for row in result:
            requerimento = {
                "requerimento_id": row.requerimento_id,
                "setor_nome_localizacao": row.setor_nome_localizacao,
                "nome_utilizador_pedido": row.nome_utilizador_pedido,
                "status": row.status,
                "urgente": row.urgente,
                "itens_pedidos": row.itens_pedidos,
                "data_pedido": row.data_pedido,
                "historico": row.historico
            }
            requerimentos.append(requerimento)
        
        return {
            "response": True,
            "data": requerimentos
        }

    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {
            "response": False,
            "error": error_msg
        }

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": error_messages
        }

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": error_messages
        }
