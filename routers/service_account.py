from fastapi import APIRouter, HTTPException
from kubernetes import client, config, utils

from kubernetes_objects.service_account import ServiceAccount

router = APIRouter()
config.load_kube_config()
k8s_client = client.ApiClient()
core_client = client.CoreV1Api()


@router.get("/service-account")
async def get_service_account():
    service_account = []
    for i in core_client.list_service_account_for_all_namespaces().items:
        service_account.append(
            {"name": i.metadata.name, "namespace": i.metadata.namespace}
        )
    return {"message": service_account}


@router.post("/service-account", status_code=200)
async def post_service_account(name: str, namespace: str):
    service_account = ServiceAccount(name, namespace)
    if service_account.exists():
        raise HTTPException(
            status_code=409, detail=f"Service Account {name} already exists"
        )

    service_account.create()
    return {"message": f"Service Account {name} was successfully created"}


@router.delete("/service-account")
def delete_service_account(name: str, namespace: str):
    service_account = ServiceAccount(name, namespace)
    if not service_account.exists():
        raise HTTPException(
            status_code=404, detail=f"Service Account {name} do not exists"
        )

    service_account.delete()
    return {"message": f"Service Account {name} was successfully deleted"}
