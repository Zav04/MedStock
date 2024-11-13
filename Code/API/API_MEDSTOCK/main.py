from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from REQUESTS.LOGIN.POST_Login import router as POST_login_router
from REQUESTS.RESET_PASSWORD.POST_Reset_Password import router as POST_reset_password_router
from REQUESTS.CREATE_USER.POST_Create_User import router as POST_create_user_router
from REQUESTS.ROLES.GET_Roles import router as GET_roles_router
from REQUESTS.ITENS.GET_Itens import router as GET_itens_router
from REQUESTS.REQUERIMENTO.GET_REQUERIMENTO import router as GET_requerimento_router
api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(POST_login_router)
api.include_router(POST_reset_password_router)
api.include_router(POST_create_user_router)
api.include_router(GET_roles_router)
api.include_router(GET_itens_router)
api.include_router(GET_requerimento_router)

if __name__ == "__main__":
    #uvicorn.run("main:api", reload=True)
    uvicorn.run("main:api", host="localhost", port=5000, reload=True)
