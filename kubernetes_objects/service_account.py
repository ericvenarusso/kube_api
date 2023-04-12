from typing import Dict

class ServiceAccount:
    def __init__(self, name, namespace):
        self.apiVersion: str = "v1"
        self.kind: str = "ServiceAccount"
        self.name: str = name
        self.namespace: str = namespace
        self.metadata: Dict[str, str] = {'name': self.name, "namespace": self.namespace}

    def to_dict(self) -> Dict[str, str]:
        return vars(self)
