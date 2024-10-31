from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from IS_ALIVE.GET_IS_ALIVE import router as GET_IS_ALIVE_router
from LOGIN.POST_Login import router as POST_login_router

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(GET_IS_ALIVE_router)
api.include_router(POST_login_router)

if __name__ == "__main__":
    #uvicorn.run("main:api", reload=True)
    uvicorn.run("main:api", host="localhost", port=5000, reload=True)
