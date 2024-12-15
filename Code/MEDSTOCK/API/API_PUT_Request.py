import os
import httpx
import asyncio
from Class.API_Response import APIResponse

async def API_UpdateConsumivel(consumivel_id, quantidade_minima, quantidade_pedido)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_UpdateConsumivel')
    payload = {
        "consumivel_id": consumivel_id,
        "quantidade_minima": quantidade_minima,
        "quantidade_pedido": quantidade_pedido,
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(URL, json=payload, headers={"Content-Type": "application/json"})
            
        if response.status_code == 200:
            success = response.json().get("response", {})
            
            if not success:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

def API_CancelRequerimento(user_id:int,requerimento_id)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_CancelRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id
        }
    try:
        response = httpx.put(URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            sucess = response.json().get("response", {})
            
            if sucess == False:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
    
def API_AcceptRequerimento(user_id,requerimento_id):
    URL = os.getenv('API_URL') + os.getenv('API_AcceptRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id
        }
    try:
        response = httpx.put(URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            sucess = response.json().get("response", {})
            
            if sucess == False:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
    

def API_StandByRequerimento(user_id:int,requerimento_id: int)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_StandByRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id
        }
    try:
        response = httpx.put(URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            success = response.json().get("response", {})
            
            if success is False:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


def API_ResumeRequerimento(user_id:int,requerimento_id: int)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_ResumeRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id
        }
    try:
        response = httpx.put(URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            success = response.json().get("response", {})
            
            if success is False:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

    
    
def API_PrepareRequerimento(user_id:int,requerimento_id: int)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_PrepareRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id
        }
    try:
        response = httpx.put(URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            success = response.json().get("response", {})
            
            if success is False:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")



def API_SendRequerimento(user_id:int, requerimento_id:int)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_SendRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id
    }
    try:
        response = httpx.put(URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            success = response.json().get("response", {})
            
            if success is False:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


def API_RejectRequerimento(user_id:int,requerimento_id:int)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_RejectRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id
        }
    try:
        response = httpx.put(URL, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            sucess = response.json().get("response", {})
            
            if sucess == False:
                error_message = response.json().get("error", {})
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

    
async def API_FinishRequerimento(user_id: int, requerimento_id: int, comentario: str)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_FinishRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id,
        "comentario": comentario if comentario else None
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(URL, json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                success = response.json().get("response", {})
                
                if not success:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message=error_message)
                else:
                    data = response.json().get("data", {})
                    return APIResponse(success=True, data=data)
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                print("Erro:", error_message)
                return APIResponse(success=False, error_message=error_message)
            else:
                print("Erro inesperado:", response.status_code)
                return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

    
async def API_ReavaliationRequerimento(user_id:int, requerimento_id:int, rejected_items:str,comentario: str)-> APIResponse:    
    URL = os.getenv('API_URL') + os.getenv('API_ReavaliationRequerimento')
    payload = {
        "requerimento_id": requerimento_id,
        "user_id": user_id,
        "comentario": comentario,
        "rejected_items": rejected_items
        }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(URL, json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                sucess = response.json().get("response", {})
                
                if sucess == False:
                    error_message = response.json().get("error", {})
                    return APIResponse(success=False, error_message = error_message)
                else:
                    data = response.json().get("data", {})
                    return APIResponse(success=True, data=data)
            elif response.status_code == 400:
                error_message = response.json().get("error", "Erro desconhecido")
                print("Erro:", error_message)
                return APIResponse(success=False, error_message=error_message)
            else:
                print("Erro inesperado:", response.status_code)
                return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
    

async def API_AssociateUserToSector(utilizador_id: int, setor_id: int) -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_AssociateUtilizadorToSector')
    payload = {
        "utilizador_id": utilizador_id,
        "setor_id": setor_id
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(URL, json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("response"):
                    return APIResponse(success=True, data=response_data.get("data"))
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
