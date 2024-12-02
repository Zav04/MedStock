import os
import httpx
import asyncio
from Class.API_Response import APIResponse
from typing import List
from Class.ItemPedido import ItemPedido


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
    

def API_CreateGestor(nome, email, password, sexo, data_nascimento, role,setor):
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
            print("Erro:", error_message)
            return APIResponse(success=False, error_message=error_message)
        else:
            print("Erro inesperado:", response.status_code)
            return APIResponse(success=False, error_message="Erro inesperado")
    except httpx.RequestError as e:
        return APIResponse(success=False, error_message=f"Erro de conexão: {e}")

def API_CreateRequerimento(user_id_pedido, setor_id,urgente, requerimento_items):

    URL = os.getenv('API_URL') + os.getenv('API_CreateRequerimento')

    payload = {
        "user_id_pedido": user_id_pedido,
        "setor_id": setor_id,
        "urgente": urgente,
        "requerimento_items": requerimento_items
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
    

def API_SendEmailRequerimentoStatus(requerimento_id: int):
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
