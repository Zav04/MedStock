from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from dependencies import get_db_MEDSTOCK
from sqlalchemy.sql import text
from Models.Create_User import C_Create_User


router = APIRouter()


@router.put("/Update_User/{id}")
async def Update_User(id: int, user: C_Create_User, db = Depends(get_db_MEDSTOCK)):
    try:
        # Verifica se o utilizador existe
        check_user_query = text("SELECT * FROM utilizador WHERE utilizador_id = :id")
        existing_user = db.execute(check_user_query, {"id": id}).fetchone()
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="Utilizador não encontrado.")

        # Verifica se o e-mail já está em uso por outro utilizador
        if user.email:
            email_exists = db.execute(text("""
                SELECT verify_exist_email(:email)
            """), {"email": user.email}).scalar()

            if email_exists:
                raise HTTPException(status_code=400, detail="E-mail já está em uso por outro utilizador.")

        # Monta a query de atualização
        update_fields = []
        update_values = {"id": id}
        
        if user.nome is not None:
            update_fields.append("nome = :nome")
            update_values["nome"] = user.nome
        
        if user.email is not None:
            update_fields.append("email = :email")
            update_values["email"] = user.email
        
        if user.sexo is not None:
            update_fields.append("sexo = :sexo")
            update_values["sexo"] = user.sexo
        
        if user.data_nascimento is not None:
            update_fields.append("data_nascimento = :data_nascimento")
            update_values["data_nascimento"] = user.data_nascimento
        
        if user.role_id is not None:
            update_fields.append("role_id = :role_id")
            update_values["role_id"] = user.role_id

        # Verifica se há campos para atualizar
        if not update_fields:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar.")

        update_query = text(f"""
            UPDATE utilizador
            SET {", ".join(update_fields)}
            WHERE utilizador_id = :id
        """)
        db.execute(update_query, update_values)
        db.commit()
        
        return {"message": "Utilizador atualizado com sucesso", "id": id}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
