import os
import httpx
import asyncio
from Class.API_Response import APIResponse


def API_Login(email, password)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_Login')
    payload = {
        "email": email,
        "password": password
    }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        
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
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


def API_ResetPassword(email)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_ResetPassword')
    payload = {
        "email": email,
    }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        
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
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


def API_CreateUser(nome, email, password, sexo, data_nascimento, role)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_CreateUser')
    payload = {
        "nome": nome,
        "email": email,
        "password": password,
        "sexo": sexo,
        "data_nascimento": data_nascimento,
        "role": role
        }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        
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
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
    

def API_CreateGestor(nome, email, password, sexo, data_nascimento, role,setor)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_CreateUserGestorResponsavel')
    payload = {
        "nome": nome,
        "email": email,
        "password": password,
        "sexo": sexo,
        "data_nascimento": data_nascimento,
        "role": role,
        "setor":setor
        }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        
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
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

def API_CreateRequerimento(user_id_pedido, setor_id,urgente, requerimento_consumivel)-> APIResponse:

    URL = os.getenv('API_URL') + os.getenv('API_CreateRequerimento')

    payload = {
        "user_id_pedido": user_id_pedido,
        "setor_id": setor_id,
        "urgente": urgente,
        "requerimento_consumiveis": requerimento_consumivel
    }

    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            success = response.json().get("response", {})
            
            if not success:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", {})
                return APIResponse(success=True, data=data)

        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro de validação desconhecido")
            return APIResponse(success=False, error_message=error_message)

        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")

    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")



def API_CreateUser_SendEmail(email, password)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_CreateUserSendEmail')
    payload = {
        "email": email,
        "password": password,
        }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        
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
            return APIResponse(success=False, error_message=error_message)
        else:

            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
    

def API_SendEmailRequerimentoStatus(requerimento_id: int)-> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_SendEmailRequerimentoStatus')
    payload = {"requerimento_id": requerimento_id}

    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("response") is False:
                error_message = response_data.get("error", "Erro desconhecido")
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

def API_CreateConsumivel(nome_consumivel: str, codigo: str, tipo_id: int)-> APIResponse:

    URL = os.getenv('API_URL') + os.getenv('API_CreateConsumivel')
    payload = {
        "nome_consumivel": nome_consumivel,
        "codigo": codigo,
        "tipo_id": tipo_id
    }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
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



def API_CreateSetorHospitalar(nome_setor: str, localizacao: str) -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_CreateSetorHospitalar')
    payload = {
        "nome_setor": nome_setor,
        "localizacao": localizacao
    }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("response"):
                return APIResponse(success=True, data=response_data.get("data"))
            else:
                return APIResponse(success=False, error_message=response_data.get("error"))
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
    
    
    
def API_CreateRedistribuicao(consumivel_id: int, requerimento_origem: int, requerimento_destino: int, quantidade: int) -> APIResponse:
    URL = os.getenv('API_URL') + os.getenv('API_CreateRedistribuicao')
    payload = {
        "consumivel_id": consumivel_id,
        "requerimento_origem": requerimento_origem,
        "requerimento_destino": requerimento_destino,
        "quantidade": quantidade,
    }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            success = response.json().get("response", False)
            if not success:
                error_message = response.json().get("error", "Erro desconhecido")
                return APIResponse(success=False, error_message=error_message)
            else:
                data = response.json().get("data", "Redistribuição criada com sucesso.")
                return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")



def API_External_CreatePedidoFornecedor(fornecedor_id: int, pedidos: list) -> APIResponse:
    URL = os.getenv('API_EXTERNAL_URL') + os.getenv('API_EXTERNAL_POST_REQUERIMENTO')  
    payload = {
        "fornecedor_id": fornecedor_id,
        "pedidos": pedidos
    }
    try:
        response = httpx.post(URL, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            return APIResponse(success=True, data=data)
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            return APIResponse(success=False, error_message=error_message)
        else:
            return APIResponse(success=False, error_message=f"Erro inesperado: {response.status_code}")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
    
    
