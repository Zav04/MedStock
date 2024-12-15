from sqlalchemy.sql import text
from fastapi import Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK
from Models.C_Create_User import C_Create_User
from Models.C_Create_Gestor_Responsavel import C_Create_Gestor_Responsavel
from Models.C_Create_User_Email import C_Create_User_Email
from Firebase.FireBase import singup
from datetime import datetime
from send_email import enviarEmailRegistro

router = APIRouter()

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends

@router.post("/MedStock_CreateUser/")
async def MedStock_CreateUser(user: C_Create_User, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT create_utilizador(:nome, :email,:sexo, :data_nascimento, :role);")
        
        data_nascimento = datetime.strptime(user.data_nascimento, "%d-%m-%Y").date()
        
        params = {
            "nome": user.nome,
            "email": user.email,
            "sexo": user.sexo,
            "data_nascimento": data_nascimento,
            "role": user.role
            }

        result = db.execute(query, params)
        status = result.scalar()
        if status == False:
            return {
                "response": status,
                "error": "Email inserido não registado"
                }
        else:
            result = singup(user.email, user.password)            
            if result == False :
                return {
                    "response": result,
                    "error": "Erro ao criar conta."
                    }
        db.commit()
        return {
            "response": True,
            "data": "Conta Criada com sucesso."
            }
    except SQLAlchemyError as e:
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
        

@router.post("/MedStock_CreateGestorResponsavel/")
async def MedStock_CreateGestorResponsavel(user: C_Create_Gestor_Responsavel, db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT create_gestor_responsavel(:nome, :email,:sexo, :data_nascimento, :role, :setor);")
        
        data_nascimento = datetime.strptime(user.data_nascimento, "%d-%m-%Y").date()
        
        params = {
            "nome": user.nome,
            "email": user.email,
            "sexo": user.sexo,
            "data_nascimento": data_nascimento,
            "role": user.role,
            "setor": user.setor
            }

        result = db.execute(query, params)
        status = result.scalar()
        if status == False:
            return {
                "response": status,
                "error": "Email inserido não registado"
                }
        else:
            result = singup(user.email, user.password)            
            if result == False :
                return {
                    "response": result,
                    "error": "Erro ao criar conta."
                    }
        db.commit()
        return {
            "response": True,
            "data": "Conta Criada com sucesso."
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



@router.post("/MedStock_CreateUserSendEmail/")
async def MedStock_CreateUserSendEmail(user: C_Create_User_Email):
    try:
        
        response=enviarEmailRegistro(user.email,user.password)
        if response == False:
            return {
                "response": False,
                "error": "Erro ao Enviar Email."
                }
        else:
            return {
            "response": True,
            "data": "Utilizador Notificado."
            }            
    except Exception as e:
        error_messages = [str(arg) for arg in e.args]
        return {
            "response": False,
            "error": error_messages
            }
