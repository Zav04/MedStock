from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK
from Models.C_CreateRequerimento import C_CreateRequerimento
from send_email import (enviarEmailRequerimentoAceito, enviarEmailRequerimentoRecusado, 
                        enviarEmailRequerimentoPreparacao, enviarEmailRequerimentoStandBy,
                        enviarEmailRequerimentoProntoEntrega,enviarEmailRequerimentoListaEspera, enviarEmailRequerimentoEntregue,
                        enviarEmailRequerimentoCriado)
from Models.C_RequerimentoRequest import C_RequerimentoRequest
from Models.C_CreateRedistribuicao import C_CreateRedistribuicao
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

        requerimento_id = result.scalar()

        if requerimento_id:
            db.commit()
            
            email_request = C_RequerimentoRequest(requerimento_id=requerimento_id)
            email_response = await MedStock_SendEmailRequerimentoStatus(email_request, db)
            
            if email_response["response"]:
                return {
                    "response": True,
                    "data": f"Requerimento {requerimento_id} criado com sucesso. E-mail enviado ao requerente."
                }
            else:
                return {
                    "response": True,
                    "data": f"Requerimento {requerimento_id} criado com sucesso. Erro ao enviar e-mail: {email_response['error']}."
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

        requerimento_id = result.requerimento_id
        nome_utilizador_pedido = result.nome_utilizador_pedido
        email_utilizador_pedido = result.email_utilizador_pedido
        status_atual = result.status_atual
        itens_pedidos = result.itens_pedidos
        historico = result.historico
        
        ultima_entrada = historico[-1]
        user_responsavel = ultima_entrada["user_responsavel"]
        data_modificacao = ultima_entrada["data_modificacao"]
        
        if status_atual == 0:
            email_sent = enviarEmailRequerimentoCriado(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
            )
            email_message = "E-mail de requerimento enviado com sucesso!"
        elif status_atual == 1:
            email_sent = enviarEmailRequerimentoAceito(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                user_responsavel=user_responsavel,
                data_modificacao=data_modificacao,
            )
            email_message = "E-mail de requerimento aceite enviado com sucesso!"
        elif status_atual == 2:
            email_sent = enviarEmailRequerimentoPreparacao(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
            )
            email_message = "E-mail de requerimento em preparação enviado com sucesso!"
        elif status_atual == 3:
            email_sent = enviarEmailRequerimentoProntoEntrega(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                user_responsavel=user_responsavel,
                data_modificacao=data_modificacao,
            )
            email_message = "E-mail de requerimento pronto para entrega enviado com sucesso!"
        elif status_atual == 5:
            email_sent = enviarEmailRequerimentoRecusado(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                user_responsavel=user_responsavel,
                data_modificacao=data_modificacao,
            )
            email_message = "E-mail de requerimento recusado enviado com sucesso!"
        elif status_atual == 6:
            email_sent = enviarEmailRequerimentoStandBy(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
            )
            email_message = "E-mail de requerimento em stand-by enviado com sucesso!"
        elif status_atual == 8:
            email_sent = enviarEmailRequerimentoEntregue(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
                user_responsavel=user_responsavel,
                data_modificacao=data_modificacao,
            )
            email_message = "E-mail de requerimento entregue enviado com sucesso!"
        elif status_atual == 10:
            email_sent = enviarEmailRequerimentoListaEspera(
                nome_utilizador_pedido=nome_utilizador_pedido,
                receiver_email=email_utilizador_pedido,
                requerimento_id=requerimento_id,
                itens_pedidos=itens_pedidos,
            )
            email_message = "E-mail de requerimento voltou para a lista de espera enviado com sucesso!"      
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


@router.post("/MedStock_CreateRedistribuicao/")
async def MedStock_CreateRedistribuicao(redistribuicao: C_CreateRedistribuicao, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("""
            SELECT create_redistribuicao(
                :p_consumivel_id,
                :p_requerimento_origem,
                :p_requerimento_destino,
                :p_quantidade
            );
        """)

        result = db.execute(query, {
            "p_consumivel_id": redistribuicao.consumivel_id,
            "p_requerimento_origem": redistribuicao.requerimento_origem,
            "p_requerimento_destino": redistribuicao.requerimento_destino,
            "p_quantidade": redistribuicao.quantidade
        })

        success = result.scalar()

        if success:
            db.commit()
            return {
                "response": True,
                "data": "Redistribuição criada com sucesso."
            }
        else:
            db.rollback()
            return {
                "response": False,
                "error": "Erro ao criar a redistribuição."
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