from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from REQUESTS.CREATE_USER.POST_Create_User import router as POST_create_user_router
from REQUESTS.CREATE_USER.PUT_Create_User import router as PUT_create_user_router
from REQUESTS.CREATE_USER.GET_Create_User import router as GET_create_user_router
from REQUESTS.CREATE_USER.DELETE_Create_User import router as DELETE_create_user_router
from REQUESTS.ITEMS.GET_Items import router as GET_Items_router
# from REQUESTS.ITEMS.PUT_Item import router as PUT_Item_router
# from REQUESTS.ITEMS.DELETE_Item import router as DELETE_Item_router
from REQUESTS.LOGIN.POST_Login import router as POST_login_router
from REQUESTS.RESET_PASSWORD.POST_Reset_Password import router as POST_reset_password_router
from REQUESTS.ROLES.GET_Roles import router as GET_roles_router

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(POST_create_user_router)
api.include_router(PUT_create_user_router)
api.include_router(GET_create_user_router)
api.include_router(DELETE_create_user_router)
api.include_router(POST_reset_password_router)
api.include_router(GET_Items_router)
# api.include_router(PUT_Item_router)
# api.include_router(DELETE_Item_router)
api.include_router(GET_roles_router)

if __name__ == "__main__":
    # uvicorn.run("main:api", reload=True)
    uvicorn.run("main:api", host="localhost", port=5000, reload=True)
    