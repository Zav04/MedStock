import os
import httpx
import asyncio
from Class.API_Response import APIResponse
from Class.roles import Roles


def API_GetRoles():
    URL = os.getenv('API_URL') + os.getenv('API_Get_Roles')
    try:
        response = httpx.get(URL, headers={"Content-Type": "application/json"})

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