import os
import httpx
import asyncio
from Class.API_Response import APIResponse

def API_Login(email, password):
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
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


def API_ResetPassword(email):
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
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


def API_CreateUser(nome, email, password, sexo, data_nascimento, role):
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
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")


def API_CreateUser_SendEmail(email, password):
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
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")