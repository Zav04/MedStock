import os
import httpx
import asyncio
from Class.API_Response import APIResponse
from Class.Roles import Roles
from Class.Consumivel import Consumivel
from Class.Requerimento import Requerimento
from Class.ItemPedido import ItemPedido
from Class.Utilizador import Utilizador
from Class.Setor import SetorHospital
from Class.RequerimentoHistorico import RequerimentoHistorico
from datetime import datetime, date


async def API_GetRoles():
    URL = os.getenv('API_URL') + os.getenv('API_Get_Roles')
    async with httpx.AsyncClient() as client:
        try:    
            response = await client.get(URL, headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                response_by_api = response.json().get("response", [])
                if response_by_api==True:
                    roles = [Roles(role["role_id"], role["nome_role"]) for role in response.json().get("data", [])]
                    return APIResponse(success=True, data=roles)
                else:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
            
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                print("Erro:", error_message)
                return APIResponse(success=False, error_message=error_message)
            
            else:
                print("Erro inesperado:", response.status_code)
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
            

        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
        
        


async def API_GetConsumiveis():
    URL = os.getenv('API_URL') + os.getenv('API_GetConsumiveis')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                response_by_api = response.json().get("response", [])
                if response_by_api == True:
                    items = [
                        Consumivel(
                            item["consumivel_id"],
                            item["nome_consumivel"],
                            item["nome_tipo"],
                            item["codigo"],
                            item["quantidade_total"],
                            item["quantidade_alocada"],
                            item["quantidade_minima"],
                            item["quantidade_pedido"]
                        )
                        for item in response.json().get("data", [])
                    ]
                    return APIResponse(success=True, data=items)
                else:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
            
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            
            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
            
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


async def API_GetRequerimentosByFarmaceutico():
    URL = os.getenv('API_URL') + os.getenv('API_GetRequerimentosByFarmaceutico')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                response_by_api = response.json().get("response", False)
                if response_by_api:
                    requerimentos = []
                    for item in response.json().get("data", []):
                        itens_pedidos = []
                        for pedido in item.get("itens_pedidos", []):
                            try:
                                itens_pedidos.append(ItemPedido(
                                    nome_item=pedido.get("nome_consumivel"),
                                    quantidade=pedido.get("quantidade", 0),
                                    tipo_item=pedido.get("tipo_consumivel")
                                ))
                            except Exception as e:
                                print(f"Erro ao processar item_pedido: {pedido}, erro: {e}")

                        historico = []
                        for h in item.get("historico", []):
                            try:
                                historico.append(RequerimentoHistorico(
                                    requerimento_status=h.get("status"),
                                    descricao=h.get("descricao", ""),
                                    data=h.get("data_modificacao"),
                                    user_responsavel=h.get("user_responsavel", "Desconhecido")
                                ))
                            except Exception as e:
                                print(f"Erro ao processar histórico: {h}, erro: {e}")

                        requerimento = Requerimento(
                            requerimento_id=item["requerimento_id"],
                            setor_nome_localizacao=item["setor_nome_localizacao"],
                            nome_utilizador_pedido=item["nome_utilizador_pedido"],
                            email_utilizador_pedido=item["email_utilizador_pedido"],
                            status_atual=item["status_atual"],
                            status_anterior=item.get("status_anterior"),
                            urgente=item["urgente"],
                            itens_pedidos=itens_pedidos,
                            data_pedido=item["data_pedido"],
                            historico=historico
                        )
                        requerimentos.append(requerimento)

                    return APIResponse(success=True, data=requerimentos)
                else:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


async def API_GetRequerimentosByUser(user_id: int):
    URL = os.getenv('API_URL') + os.getenv('API_GetRequerimentosByUser') + f"?user_id={user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                response_by_api = response.json().get("response", False)
                if response_by_api:
                    requerimentos = []
                    for item in response.json().get("data", []):
                        itens_pedidos = []
                        for pedido in item.get("itens_pedidos", []):
                            try:
                                itens_pedidos.append(ItemPedido(
                                    nome_item=pedido.get("nome_consumivel"),
                                    quantidade=pedido.get("quantidade", 0),
                                    tipo_item=pedido.get("tipo_consumivel")
                                ))
                            except Exception as e:
                                print(f"Erro ao processar item_pedido: {pedido}, erro: {e}")

                        historico = []
                        for h in item.get("historico", []):
                            try:
                                historico.append(RequerimentoHistorico(
                                    requerimento_status=h.get("status"),
                                    descricao=h.get("descricao", ""),
                                    data=h.get("data_modificacao"),
                                    user_responsavel=h.get("user_responsavel", "Desconhecido")
                                ))
                            except Exception as e:
                                print(f"Erro ao processar histórico: {h}, erro: {e}")

                        requerimento = Requerimento(
                            requerimento_id=item["requerimento_id"],
                            setor_nome_localizacao=item["setor_nome_localizacao"],
                            nome_utilizador_pedido=item["nome_utilizador_pedido"],
                            email_utilizador_pedido=item["email_utilizador_pedido"],
                            status_atual=item["status_atual"],
                            status_anterior=item.get("status_anterior"),
                            urgente=item["urgente"],
                            itens_pedidos=itens_pedidos,
                            data_pedido=item["data_pedido"],
                            historico=historico
                        )
                        requerimentos.append(requerimento)

                    return APIResponse(success=True, data=requerimentos)
                else:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")



async def API_GetRequerimentosByResponsavel(user_id: int):
    URL = os.getenv('API_URL') + os.getenv('API_GetRequerimentosByResponsavel') + f"?responsavel_id={user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                response_by_api = response.json().get("response", False)
                if response_by_api:
                    requerimentos = []
                    for item in response.json().get("data", []):
                        itens_pedidos = []
                        for pedido in item.get("itens_pedidos", []):
                            try:
                                itens_pedidos.append(ItemPedido(
                                    nome_item=pedido.get("nome_consumivel"),
                                    quantidade=pedido.get("quantidade", 0),
                                    tipo_item=pedido.get("tipo_consumivel")
                                ))
                            except Exception as e:
                                print(f"Erro ao processar item_pedido: {pedido}, erro: {e}")

                        historico = []
                        for h in item.get("historico", []):
                            try:
                                historico.append(RequerimentoHistorico(
                                    requerimento_status=h.get("status"),
                                    descricao=h.get("descricao", ""),
                                    data=h.get("data_modificacao"),
                                    user_responsavel=h.get("user_responsavel", "Desconhecido")
                                ))
                            except Exception as e:
                                print(f"Erro ao processar histórico: {h}, erro: {e}")

                        requerimento = Requerimento(
                            requerimento_id=item["requerimento_id"],
                            setor_nome_localizacao=item["setor_nome_localizacao"],
                            nome_utilizador_pedido=item["nome_utilizador_pedido"],
                            email_utilizador_pedido=item["email_utilizador_pedido"],
                            status_atual=item["status_atual"],
                            status_anterior=item.get("status_anterior"),
                            urgente=item["urgente"],
                            itens_pedidos=itens_pedidos,
                            data_pedido=item["data_pedido"],
                            historico=historico
                        )
                        requerimentos.append(requerimento)

                    return APIResponse(success=True, data=requerimentos)
                else:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")



def API_GetUserByEmail(email: str):
    URL = os.getenv('API_URL') + os.getenv('API_GetUserByEmail') + f"?email={email}"
    try:
        response =httpx.get(URL, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("response"):
                user_data = response_data.get("data")
                
                if user_data:
                    raw_data_nascimento = user_data.get("data_nascimento")
                    if raw_data_nascimento:
                        try:
                            data_nascimento = datetime.strptime(raw_data_nascimento, "%Y-%m-%d").date()
                        except ValueError:
                            data_nascimento = datetime.strptime(raw_data_nascimento, "%Y-%m-%dT%H:%M:%S").date()
                    else:
                        data_nascimento = None
                    utilizador = Utilizador(
                        utilizador_id=user_data["utilizador_id"],
                        nome=user_data["nome"],
                        email=user_data["email"],
                        sexo=user_data["sexo"],
                        data_nascimento=data_nascimento,
                        role_id=user_data["role_id"],
                        role_nome=user_data["role_nome"]
                    )
                    return APIResponse(success=True, data=utilizador)
                else:
                    error_message = response_data.get("error")
                    return APIResponse(success=False, error_message=error_message)
            else:
                error_message = response_data.get("error")
                return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


async def API_GetSectors():
    URL = os.getenv('API_URL') + os.getenv('API_GetSectors')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("response"):
                    sectors = [
                        SetorHospital(
                            setor_id=sector["setor_id"],
                            nome_setor=sector["nome_setor"],
                            localizacao=sector["localizacao"]
                        )
                        for sector in response_data.get("data", [])
                    ]
                    return APIResponse(success=True, data=sectors)
                else:
                    error_message = response_data.get("error", "Erro desconhecido")
                    return APIResponse(success=False, error_message=error_message)

            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)

            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")

        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

def API_GetEmailDetails(requerimento_id: int):
    URL = os.getenv('API_URL') + "/MedStock_GetEmailDetails/"
    try:
        response =  httpx.get(
            URL,
            headers={"Content-Type": "application/json"},
            params={"requerimento_id": requerimento_id}
        )
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("response"):
                data = response_data.get("data")
                itens_pedidos = [
                    ItemPedido(
                        nome_item=item["nome_item"],
                        quantidade=item["quantidade"],
                        tipo_item=item.get("tipo_item", "")
                    )
                    for item in data["itens_pedidos"]
                ]
                return {
                    "success": True,
                    "email_remetente": data["email_remetente"],
                    "nome_responsavel": data["nome_responsavel"],
                    "hora_acao": data["hora_acao"],
                    "itens_pedidos": itens_pedidos
                }
            else:
                return {
                    "success": False,
                    "error_message": response_data.get("error", "Erro desconhecido")
                }
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return {"success": False, "error_message": error_message}
        else:
            return {"success": False, "error_message": f"Erro inesperado: {response.status_code}"}
    except httpx.RequestError as e:
        return {"success": False, "error_message": f"Erro de conexão: {e}"}



