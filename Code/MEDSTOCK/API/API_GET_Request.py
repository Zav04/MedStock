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
from Class.TipoConsumivel import Tipo_Consumivel
from Class.RequerimentoHistorico import RequerimentoHistorico
from Class.UtilizadorSetor import UtilizadorSetor
from datetime import datetime


async def API_GetRoles()-> APIResponse:
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
        
        

async def API_GetConsumiveis()-> APIResponse:
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


async def API_GetRequerimentosByFarmaceutico() -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_GetRequerimentosByFarmaceutico')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                response_by_api = response.json().get("response", False)
                if response_by_api:
                    requerimentos = []
                    for item in response.json().get("data", []):
                        itens_pedidos = [
                            ItemPedido(
                                nome_item=pedido.get("nome_consumivel"),
                                quantidade=pedido.get("quantidade", 0),
                                tipo_item=pedido.get("tipo_consumivel")
                            ) for pedido in item.get("itens_pedidos", [])
                        ]

                        historico = [
                            RequerimentoHistorico(
                                requerimento_status=h.get("status"),
                                descricao=h.get("descricao", ""),
                                data=h.get("data_modificacao"),
                                user_responsavel=h.get("user_responsavel", "Desconhecido")
                            ) for h in item.get("historico", [])
                        ]

                        requerimento = Requerimento(
                            requerimento_id=item["requerimento_id"],
                            setor_nome_localizacao=item["setor_nome_localizacao"],
                            nome_utilizador_pedido=item["nome_utilizador_pedido"],
                            email_utilizador_pedido=item["email_utilizador_pedido"],
                            status_atual=item["status_atual"],
                            status_anterior=item.get("status_anterior"),
                            urgente=item["urgente"],
                            tipo_requerimento=item["tipo_requerimento"],
                            itens_pedidos=itens_pedidos,
                            data_pedido=item["data_pedido"],
                            historico=historico
                        )
                        requerimentos.append(requerimento)

                    return APIResponse(success=True, data=requerimentos)
                else:
                    return APIResponse(success=False, error_message=response.json().get("error", "Erro desconhecido"))
            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


async def API_GetRequerimentosByUser(user_id: int) -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_GetRequerimentosByUser') + f"?user_id={user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                response_by_api = response.json().get("response", False)
                if response_by_api:
                    requerimentos = []
                    for item in response.json().get("data", []):
                        itens_pedidos = [
                            ItemPedido(
                                nome_item=pedido.get("nome_consumivel"),
                                quantidade=pedido.get("quantidade", 0),
                                tipo_item=pedido.get("tipo_consumivel")
                            ) for pedido in item.get("itens_pedidos", [])
                        ]

                        historico = [
                            RequerimentoHistorico(
                                requerimento_status=h.get("status"),
                                descricao=h.get("descricao", ""),
                                data=h.get("data_modificacao"),
                                user_responsavel=h.get("user_responsavel", "Desconhecido")
                            ) for h in item.get("historico", [])
                        ]

                        requerimento = Requerimento(
                            requerimento_id=item["requerimento_id"],
                            setor_nome_localizacao=item["setor_nome_localizacao"],
                            nome_utilizador_pedido=item["nome_utilizador_pedido"],
                            email_utilizador_pedido=item["email_utilizador_pedido"],
                            status_atual=item["status_atual"],
                            status_anterior=item.get("status_anterior"),
                            urgente=item["urgente"],
                            tipo_requerimento=item["tipo_requerimento"],
                            itens_pedidos=itens_pedidos,
                            data_pedido=item["data_pedido"],
                            historico=historico
                        )
                        requerimentos.append(requerimento)

                    return APIResponse(success=True, data=requerimentos)
                else:
                    return APIResponse(success=False, error_message=response.json().get("error", "Erro desconhecido"))
            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


async def API_GetRequerimentosByResponsavel(user_id: int) -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_GetRequerimentosByResponsavel') + f"?responsavel_id={user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                response_by_api = response.json().get("response", False)
                if response_by_api:
                    requerimentos = []
                    for item in response.json().get("data", []):
                        itens_pedidos = [
                            ItemPedido(
                                nome_item=pedido.get("nome_consumivel"),
                                quantidade=pedido.get("quantidade", 0),
                                tipo_item=pedido.get("tipo_consumivel")
                            ) for pedido in item.get("itens_pedidos", [])
                        ]

                        historico = [
                            RequerimentoHistorico(
                                requerimento_status=h.get("status"),
                                descricao=h.get("descricao", ""),
                                data=h.get("data_modificacao"),
                                user_responsavel=h.get("user_responsavel", "Desconhecido")
                            ) for h in item.get("historico", [])
                        ]

                        requerimento = Requerimento(
                            requerimento_id=item["requerimento_id"],
                            setor_nome_localizacao=item["setor_nome_localizacao"],
                            nome_utilizador_pedido=item["nome_utilizador_pedido"],
                            email_utilizador_pedido=item["email_utilizador_pedido"],
                            status_atual=item["status_atual"],
                            status_anterior=item.get("status_anterior"),
                            urgente=item["urgente"],
                            tipo_requerimento=item["tipo_requerimento"],
                            itens_pedidos=itens_pedidos,
                            data_pedido=item["data_pedido"],
                            historico=historico
                        )
                        requerimentos.append(requerimento)

                    return APIResponse(success=True, data=requerimentos)
                else:
                    return APIResponse(success=False, error_message=response.json().get("error", "Erro desconhecido"))
            else:
                return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")




def API_GetUserByEmail(email: str)-> APIResponse:
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


async def API_GetSectors()-> APIResponse:
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
        
        
async def API_GetAllTipoConsumiveis()-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_GetAllTipoConsumiveis')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("response"):
                    tipos = [
                        Tipo_Consumivel(
                            tipo_consumivel_id=tipo["tipo_id"],
                            nome_tipo=tipo["nome_tipo"]
                        )
                        for tipo in response_data.get("data", [])
                    ]
                    return APIResponse(success=True, data=tipos)
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

async def API_GetAllUsers() -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_GetAllUsers')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("response"):
                    users = [
                        Utilizador(
                            utilizador_id=user["utilizador_id"],
                            nome=user["nome"],
                            email=user["email"],
                            sexo=user["sexo"],
                            data_nascimento=user["data_nascimento"],
                            role_id=user["role_id"],
                            role_nome=user["role_nome"]
                        )
                        for user in response_data.get("data", [])
                    ]
                    return APIResponse(success=True, data=users)
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


async def API_GetUtilizadoresComSetores() -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_GetUtilizadoresComSetores')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("response"):
                    utilizadores = [
                        UtilizadorSetor(
                            utilizador_id=utilizador["utilizador_id"],
                            nome=utilizador["nome"],
                            nome_setor=utilizador["nome_setor"],
                            localizacao=utilizador["localizacao"]
                        )
                        for utilizador in response_data.get("data", [])
                    ]
                    return APIResponse(success=True, data=utilizadores)
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