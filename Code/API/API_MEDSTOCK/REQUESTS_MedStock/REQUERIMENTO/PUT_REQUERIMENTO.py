from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_Update_Requerimento import C_Update_Requerimento
from Models.C_ReavaliationRequerimento import C_ReavaliationRequerimento
from Models.C_RequerimentoExterno import C_RequerimentoExterno
from Models.C_RequerimentoAlocacao import C_RequerimentoAtualizacao
import json

from fastapi import Request

router = APIRouter()


@router.put("/MedStock_CancelRequerimento/")
async def MedStock_CancelRequerimento(requerimento: C_Update_Requerimento, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT update_requerimento_cancel(:p_requerimento_id,:p_user_id);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Cancelado."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao cancelar o requerimento."
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
        return {
            "response": False,
            "error": error_messages
        }
        
@router.put("/MedStock_RejectRequerimento/")
async def MedStock_RejectRequerimento(requerimento: C_Update_Requerimento, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT update_requerimento_reject(:p_requerimento_id,:p_user_id);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Recusado."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao recusar o requerimento."
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
        return {
            "response": False,
            "error": error_messages
        }


@router.put("/MedStock_AcceptRequerimento/")
async def MedStock_AcceptRequerimento(requerimento: C_Update_Requerimento, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT update_requerimento_accept(:p_requerimento_id,:p_user_id);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Aceite."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao aceitar o requerimento."
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
        return {
            "response": False,
            "error": error_messages
        }
        
        


@router.put("/MedStock_StandByRequerimento/")
async def MedStock_StandByRequerimento(requerimento: C_Update_Requerimento, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT update_requerimento_standby(:p_requerimento_id,:p_user_id);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Colocado em Stand-By."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao colocar o requerimento em Stand-By."
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
        return {
            "response": False,
            "error": error_messages
        }
        
        
@router.put("/MedStock_ResumeRequerimento/")
async def MedStock_ResumeRequerimento(requerimento: C_Update_Requerimento, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT update_requerimento_resume(:p_requerimento_id,:p_user_id);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Colocado na Lista de Espera."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao colocar o requerimento na Lista de Espera."
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
        return {
            "response": False,
            "error": error_messages
        }
        
@router.put("/MedStock_PrepareRequerimento/")
async def MedStock_PrepareRequerimento(requerimento: C_Update_Requerimento, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT update_requerimento_preparation(:p_requerimento_id,:p_user_id);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Colocado em Stand-By."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao colocar o requerimento em Stand-By."
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
        return {
            "response": False,
            "error": error_messages
        }
        
@router.put("/MedStock_SendRequerimento/")
async def MedStock_SendRequerimento(requerimento: C_Update_Requerimento, db=Depends(get_db_MEDSTOCK)):
    try:

        query = text("""
            SELECT update_requerimento_send(:p_requerimento_id,:p_user_id);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Aceite."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao aceitar o requerimento."
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
        return {
            "response": False,
            "error": error_messages
        }

@router.put("/MedStock_FinishRequerimento/")
async def MedStock_FinishRequerimento(requerimento: C_ReavaliationRequerimento, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("""
            SELECT update_requerimento_finish(:p_user_id, :p_requerimento_id, :p_comentario);
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id,
            "p_comentario": requerimento.comentario if hasattr(requerimento, 'comentario') else None
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento Finalizado com sucesso."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao finalizar o requerimento."
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
        return {
            "response": False,
            "error": error_messages
        }

        
        
        
@router.put("/MedStock_ReavaliationRequerimento/")
async def MedStock_ReavaliationRequerimento(requerimento: C_ReavaliationRequerimento, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("""
            SELECT update_requerimento_reavaliation(
                :p_user_id, 
                :p_requerimento_id, 
                :p_comentario, 
                :consumiveis_rejeitados
            );
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_user_id": requerimento.user_id,
            "p_comentario": requerimento.comentario or None,
            "consumiveis_rejeitados": requerimento.rejected_items or None
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento em Reavaliação com sucesso."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao enviar o requerimento para reavaliação."
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
        return {
            "response": False,
            "error": error_messages
        }


@router.put("/MedStock_UpdateRequerimentoExterno/")
async def MedStock_UpdateRequerimentoExterno(requerimento: C_RequerimentoExterno, db=Depends(get_db_MEDSTOCK)):
    try:
        items_json = json.dumps([item.model_dump() for item in requerimento.items_list or []])
        
        query = text("""
            SELECT update_requerimento_externo(
                :p_requerimento_id,
                :p_setor_id,
                :items_list,
                :p_user_id
            );
        """)

        result = db.execute(query, {
            "p_requerimento_id": requerimento.requerimento_id,
            "p_setor_id": requerimento.setor_id,
            "items_list": items_json,
            "p_user_id": requerimento.user_id
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "message": "Requerimento externo atualizado com sucesso."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao atualizar o requerimento externo."
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
        return {
            "response": False,
            "error": error_messages
        }
        
        
@router.put("/MedStock_UpdateConsumivelAlocado/")
async def MedStock_UpdateConsumivelAlocado(consumivel: C_RequerimentoAtualizacao,db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("""
            SELECT update_requerimento_quantidade_alocada(:p_requerimento_id, :p_consumiveis);
        """)
        consumiveis_serializados = [c.dict() for c in consumivel.consumiveis]

        result = db.execute(query, {
            "p_requerimento_id": consumivel.requerimento_id,
            "p_consumiveis": json.dumps(consumiveis_serializados)
        })
        
        success = result.scalar()
        
        if success:
            db.commit()
            return {
                "response": True,
                "data": "Quantidade alocada atualizada com sucesso."
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
        return {
            "response": False,
            "error": error_messages
        }
