from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from CREATE_USER.PUT_Create_User import router as PUT_Create_User_router

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(PUT_Create_User_router)

if __name__ == "__main__":
    uvicorn.run("main:api", host="localhost", port=5000, reload=True)
