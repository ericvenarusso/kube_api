import uvicorn
from fastapi import FastAPI

from routers import service_account


app = FastAPI(
    title="kube_api",
    version="0.0.1",
    description="Api that creates kubernetes objects"
)

app.include_router(service_account.router)
