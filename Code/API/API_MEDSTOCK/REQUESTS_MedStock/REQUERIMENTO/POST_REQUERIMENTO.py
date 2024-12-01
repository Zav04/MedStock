from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_CreateRequerimento import C_CreateRequerimento
from Models.C_Email_Avaliation import C_Email_Avaliation
from send_email import enviarEmailRequerimentoAceito, enviarEmailRequerimentoRecusado
from REQUESTS_MedStock.REQUERIMENTO.GET_REQUERIMENTO import MedStock_GetRequerimentosByUser
from Models.C_RequerimentoRequest import C_RequerimentoRequest
import json

router = APIRouter()


@router.post("/MedStock_CreateRequerimento/")
async def MedStock_CreateRequerimento(requerimento: C_CreateRequerimento, db=Depends(get_db_MEDSTOCK)):
    try:
        items_json = json.dumps([item.model_dump() for item in requerimento.requerimento_items or []])

        query = text("""
            SELECT create_requerimento(:user_id_pedido, :setor_id, :items_list, :urgente);
        """)

        result = db.execute(query, {
            "user_id_pedido": requerimento.user_id_pedido,
            "setor_id": requerimento.setor_id,
            "items_list": items_json,
            "urgente": requerimento.urgente
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Requerimento criado com sucesso."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao criar o requerimento."
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


@router.post("/MedStock_SendEmailAvaliation/")
async def MedStock_SendEmailAvaliation(request: C_RequerimentoRequest, db=Depends(get_db_MEDSTOCK)):
    try:
        
        requerimento_id = request.requerimento_id
        query = text("SELECT * FROM get_requerimento_avaliation_details(:p_requerimento_id);")
        result = db.execute(query, {"p_requerimento_id": requerimento_id}).fetchone()

        if not result:
            return {
                "response": False,
                "error": "Requerimento não encontrado."
            }

        requerimento_id = result.requerimento_id
        email_utilizador_pedido = result.email_utilizador_pedido
        nome_utilizador_confirmacao = result.nome_utilizador_confirmacao
        data_confirmacao = result.data_confirmacao
        itens_pedidos = result.itens_pedidos
        status = result.status

        if status not in (1, 5):
            return {
                "response": False,
                "error": "O requerimento ainda não foi avaliado ou não possui um status válido para envio de e-mail."
            }

        if status == 1:
            email_sent = enviarEmailRequerimentoAceito(
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                data_confirmacao=data_confirmacao,
                nome_utilizador_confirmacao=nome_utilizador_confirmacao
            )
            email_message = "E-mail de aceitação enviado com sucesso!"
        elif status == 5:
            email_sent = enviarEmailRequerimentoRecusado(
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                data_confirmacao=data_confirmacao,
                nome_utilizador_confirmacao=nome_utilizador_confirmacao
            )
            email_message = "E-mail de recusa enviado com sucesso!"
        else:
            return {
                "response": False,
                "error": "O status do requerimento não é suportado para envio de e-mail."
            }

        if email_sent:
            return {
                "response": True,
                "data": email_message
            }
        else:
            return {
                "response": False,
                "error": "Erro ao enviar o e-mail."
            }

    except Exception as e:
        return {
            "response": False,
            "error": str(e)
        }
