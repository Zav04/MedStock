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
            data = response.json().get("response", {})
            if "registered" in data:
                return APIResponse(success=True, data=data)
            else:
                return APIResponse(success=False, error_message="Credenciais inválidas")
        elif response.status_code == 400:
            error_message = response.json().get("error", "Erro desconhecido")
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")
