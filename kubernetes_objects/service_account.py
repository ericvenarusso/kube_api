from typing import Dict

from kubernetes import utils

from kubernetes_objects.client import KubernetesClient


class ServiceAccount:
    def __init__(self, name: str = "", namespace: str = "default"):
        self.client: KubernetesClient = KubernetesClient()
        self.apiVersion: str = "v1"
        self.kind: str = "ServiceAccount"
        self.name: str = name
        self.namespace: str = namespace
        self.metadata: Dict[str, str] = {"name": self.name, "namespace": self.namespace}

    def to_dict(self):
        self_variables = vars(self)
        return {key: value for key, value in self_variables.items() if key != "client"}

    def create(self):
        if not self.name:
            raise ValueError("Service Accout name is required for creation")

        utils.create_from_dict(self.client.api_client, self.to_dict())

    def delete(self):
        if not self.name:
            raise ValueError("Service Accout name is required for creation")

        self.client.core_client.delete_namespaced_service_account(
            self.namespace, self.name
        )

    def exists(self):
        service_account_names = [
            i.metadata.name
            for i in self.client.core_client.list_namespaced_service_account(
                self.namespace
            ).items
        ]
        if self.name in service_account_names:
            return True
        return False
