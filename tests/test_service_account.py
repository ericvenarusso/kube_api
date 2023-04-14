from dataclasses import dataclass
from typing import List
from unittest.mock import patch

import pytest

from kubernetes_objects.service_account import ServiceAccount


@dataclass
class FakeServiceAccountParameters:
    name: str
    namespace: str


@dataclass
class FakeServiceAccountMetadata:
    metadata: FakeServiceAccountParameters


@dataclass
class FakeServiceAccountList:
    items: List[FakeServiceAccountMetadata]


class TestServiceAccount:
    @patch("kubernetes.utils.create_from_dict")
    @patch("kubernetes.client.ApiClient")
    def test_creation_with_name_expect_sucess(self, _, mock_create_from_dict):
        service_account = ServiceAccount(name="test")
        service_account.create()

        assert mock_create_from_dict.called_once_with(
            service_account.client.api_client,
            {
                "apiVersion": "v1",
                "kind": "ServiceAccount",
                "name": "test",
                "namespace": "default",
                "metadata": {"name": "test", "namespace": "default"},
            },
        )

    def test_creation_without_name_expect_error(self):
        with pytest.raises(
            ValueError, match=r"Service Accout name is required for creation"
        ):
            ServiceAccount().create()

    @patch("kubernetes.client.CoreV1Api.delete_namespaced_service_account")
    def test_deletion_with_name_expect_sucess(self, mock_delete_service_account):
        service_account = ServiceAccount(name="test")
        service_account.delete()

        assert mock_delete_service_account.called_once_with(
            name="test", namespace="default"
        )

    def test_deletion_without_name_expect_error(self):
        with pytest.raises(
            ValueError, match=r"Service Accout name is required for creation"
        ):
            ServiceAccount().delete()

    @patch(
        "kubernetes.client.CoreV1Api.list_namespaced_service_account",
        return_value=FakeServiceAccountList(
            [
                FakeServiceAccountMetadata(
                    FakeServiceAccountParameters(name="test", namespace="default")
                )
            ]
        ),
    )
    def test_service_account_nonexistence(self, _):
        service_account = ServiceAccount(name="test")
        assert service_account.exists() == True

    @patch(
        "kubernetes.client.CoreV1Api.list_namespaced_service_account",
        return_value=FakeServiceAccountList(
            [
                FakeServiceAccountMetadata(
                    FakeServiceAccountParameters(name="no_test", namespace="default")
                )
            ]
        ),
    )
    def test_service_account_existence(self, _):
        service_account = ServiceAccount(name="test")
        assert service_account.exists() == False
