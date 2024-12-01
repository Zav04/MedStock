from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_db_MEDSTOCK

router = APIRouter()

@router.get("/MedStock_GetRoles/")
async def MedStock_GetRoles(db=Depends(get_db_MEDSTOCK)):
    try:
        query = text("SELECT get_roles();")
        result = db.execute(query).fetchall()
        roles = []
        for row in result:
            raw_data = row[0].strip("()")
            role_id, nome_role = raw_data.split(",", 1)
            role_id = int(role_id)
            nome_role = nome_role.strip().strip('"')
            roles.append({"role_id": role_id, "nome_role": nome_role})

        return {"response": True, "data": roles}
    
    except SQLAlchemyError as e:
        error_msg = str(e.__dict__['orig']).split('\n')[0]
        return {"response": False, "error": error_msg}

    except Exception as e:
        db.rollback()
        error_messages = [str(arg) for arg in e.args]
        return {"response": False, "error": error_messages}
