import os
import httpx
import asyncio
from Class.API_Response import APIResponse
from Class.roles import Roles
from Class.itens import Itens
from Class.requerimento import Requerimento


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
                return APIResponse(success=False, error_message="Erro inesperado")
            

        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
        
        


async def API_GetItems():
    URL = os.getenv('API_URL') + os.getenv('API_Get_Items')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                response_by_api = response.json().get("response", [])
                if response_by_api == True:
                    items = [Itens(
                        item["nome_item"],
                        item["nome_tipo"],
                        item["codigo"],
                        item["quantidade_disponivel"]
                    ) for item in response.json().get("data", [])]
                    return APIResponse(success=True, data=items)
                else:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
            
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            
            else:
                return APIResponse(success=False, error_message="Erro inesperado")
            
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
        

async def API_GetRequerimentosByUser(user_id: int):
    URL = os.getenv('API_URL') + os.getenv('API_GetRequerimentosByUser') + f"?user_id={user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                response_by_api = response.json().get("response", [])
                if response_by_api == True:
                    
                    requerimentos = [
                        Requerimento(
                            requerimento_id=item["requerimento_id"],
                            setor_nome_localizacao=item["setor_nome_localizacao"],
                            nome_utilizador_pedido=item["nome_utilizador_pedido"],
                            status=item["status"],
                            urgente=item["urgente"],
                            itens_pedidos=item["itens_pedidos"],
                            data_pedido=item["data_pedido"],
                            nome_utilizador_confirmacao=item["nome_utilizador_confirmacao"],
                            data_confirmacao=item["data_confirmacao"],
                            nome_utilizador_envio=item["nome_utilizador_envio"],
                            data_envio=item["data_envio"]
                        )
                        for item in response.json().get("data", [])
                    ]
                    return APIResponse(success=True, data=requerimentos)
                else:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            else:
                return APIResponse(success=False, error_message="Erro inesperado")
        except httpx.RequestError as e:
            return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

