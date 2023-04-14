from dataclasses import dataclass

from kubernetes import client, config


@dataclass
class KubernetesClient:
    config.load_kube_config()
    api_client: client.ApiClient = client.ApiClient()
    core_client: client.CoreV1Api = client.CoreV1Api()
