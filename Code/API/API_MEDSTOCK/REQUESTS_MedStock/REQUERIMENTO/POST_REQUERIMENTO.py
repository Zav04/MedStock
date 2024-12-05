from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_CreateRequerimento import C_CreateRequerimento
from send_email import (enviarEmailRequerimentoAceito, enviarEmailRequerimentoRecusado, 
                        enviarEmailRequerimentoPreparacao, enviarEmailRequerimentoStandBy,
                        enviarEmailRequerimentoProntoEntrega,enviarEmailRequerimentoListaEspera, enviarEmailRequerimentoEntregue)
from Models.C_RequerimentoRequest import C_RequerimentoRequest
import json

router = APIRouter()


@router.post("/MedStock_CreateRequerimento/")
async def MedStock_CreateRequerimento(requerimento: C_CreateRequerimento, db=Depends(get_db_MEDSTOCK)):
    try:
        items_json = json.dumps([item.model_dump() for item in requerimento.requerimento_consumiveis or []])

        query = text("""
            SELECT create_requerimento(:user_id_pedido, :p_setor_id, :items_list, :urgente);
        """)

        result = db.execute(query, {
            "user_id_pedido": requerimento.user_id_pedido,
            "p_setor_id": requerimento.setor_id,
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


@router.post("/MedStock_SendEmailRequerimentoStatus/")
async def MedStock_SendEmailRequerimentoStatus(request: C_RequerimentoRequest, db=Depends(get_db_MEDSTOCK)):
    try:
        requerimento_id = request.requerimento_id
        query = text("SELECT * FROM get_requerimento_details(:p_requerimento_id);")
        result = db.execute(query, {"p_requerimento_id": requerimento_id}).fetchone()

        if not result:
            return {
                "response": False,
                "error": "Requerimento não encontrado."
            }

        # Mapeamento dos campos retornados pelo PostgreSQL
        requerimento_id = result.requerimento_id
        setor_nome_localizacao = result.setor_nome_localizacao
        nome_utilizador_pedido = result.nome_utilizador_pedido
        email_utilizador_pedido = result.email_utilizador_pedido
        nome_gestor_responsavel = result.nome_gestor_responsavel
        email_gestor_responsavel = result.email_gestor_responsavel
        status = result.status
        urgente = result.urgente
        itens_pedidos = result.itens_pedidos
        data_pedido = result.data_pedido
        nome_utilizador_confirmacao = result.nome_utilizador_confirmacao
        data_confirmacao = result.data_confirmacao
        nome_utilizador_envio = result.nome_utilizador_envio
        data_envio = result.data_envio
        nome_utilizador_preparacao = result.nome_utilizador_preparacao
        data_preparacao = result.data_preparacao

        # Lógica para envio de e-mail com base no status
        if status == 1:
            email_sent = enviarEmailRequerimentoAceito(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                data_confirmacao=data_confirmacao,
                nome_utilizador_confirmacao=nome_utilizador_confirmacao
            )
            email_message = "E-mail de requerimento aceite enviado com sucesso!"
        elif status == 2:
            email_sent = enviarEmailRequerimentoPreparacao(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos
            )
            email_message = "E-mail de requerimento em preparação enviado com sucesso!"
        elif status == 3:
            email_sent = enviarEmailRequerimentoProntoEntrega(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                nome_utilizador_confirmacao=nome_utilizador_preparacao,
                data_preparacao=data_preparacao
            )
            email_message = "E-mail de requerimento pronto para entrega enviado com sucesso!"
        elif status == 5:
            email_sent = enviarEmailRequerimentoRecusado(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                data_confirmacao=data_confirmacao,
                nome_utilizador_confirmacao=nome_utilizador_confirmacao
            )
            email_message = "E-mail de requerimento recusado enviado com sucesso!"
        elif status == 6:
            email_sent = enviarEmailRequerimentoStandBy(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos
            )
            email_message = "E-mail de requerimento em stand-by enviado com sucesso!"
        elif status == 8:
            email_sent = enviarEmailRequerimentoEntregue(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                nome_entregador=nome_utilizador_envio,
                data_entrega=data_envio
            )
            email_message = "E-mail de requerimento em validação enviado com sucesso!"
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


