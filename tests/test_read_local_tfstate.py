import pytest
import os
from ansible.errors import AnsibleUndefinedVariable, AnsibleConnectionFailure
from ansible.parsing.dataloader import DataLoader
from plugins.vars.read_local_tfstate import VarsModule

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


@pytest.fixture(autouse=True)
def reset_cache():
    VarsModule.CACHE = {}


def test_fail_when_conf_is_missing():
    with pytest.raises(AnsibleUndefinedVariable):
        plugin = VarsModule()
        plugin.get_vars({}, {}, "localhost")


def test_fail_when_tf_state_does_not_exists():
    with pytest.raises(AnsibleConnectionFailure):
        os.environ["TF_STATES_PATHS"] = "./missing.tf"
        plugin = VarsModule()
        plugin.get_vars({}, {}, "localhost")


def test_return_empty_when_no_outputs():
    os.environ["TF_STATES_PATHS"] = os.path.join(RESOURCES, "empty_output.tfstate")
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {}


def test_return_empty_if_missing_state():
    os.environ["TF_STATES_PATHS"] = os.path.join(
        RESOURCES, "missing_ansible_vars.tfstate"
    )
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {}


def test_return_variables_from_single_tf_state():
    os.environ["TF_STATES_PATHS"] = os.path.join(RESOURCES, "state_with_vars.tfstate")
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {
        "clusters": {
            "cluster-0": {
                "name": "cluster-0",
                "id": "abc123",
                "endpoint": "https://192.168.49.2:8443",
            }
        },
        "s3_buckets": {
            "app-data": {
                "name": "dev-app-data",
                "access_key_id": "key1",
                "secret_access_key": "secret1",
                "endpoint": "https://s3.example.com",
                "region": "us-east-1",
            }
        },
    }


def test_return_variables_from_multiple_tf_state():
    os.environ["TF_STATES_PATHS"] = ",".join(
        [
            os.path.join(RESOURCES, "state_with_vars.tfstate"),
            os.path.join(RESOURCES, "state_with_vars2.tfstate"),
        ]
    )
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {
        "clusters": {
            "cluster-0": {
                "name": "cluster-0",
                "id": "abc123",
                "endpoint": "https://192.168.49.2:8443",
            },
            "cluster-1": {
                "name": "cluster-1",
                "id": "def456",
                "endpoint": "https://192.168.49.3:8443",
            },
        },
        "s3_buckets": {
            "app-data": {
                "name": "dev-app-data",
                "access_key_id": "key1",
                "secret_access_key": "secret1",
                "endpoint": "https://s3.example.com",
                "region": "us-east-1",
            },
            "backups": {
                "name": "dev-backups",
                "access_key_id": "key2",
                "secret_access_key": "secret2",
                "endpoint": "https://s3.example.com",
                "region": "us-east-1",
            },
        },
    }


def test_multiple_states_deep_merges_s3_buckets():
    os.environ["TF_STATES_PATHS"] = ",".join(
        [
            os.path.join(RESOURCES, "state_with_nested_vars.tfstate"),
            os.path.join(RESOURCES, "state_with_nested_vars2.tfstate"),
        ]
    )
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {
        "s3_buckets": {
            "app-data": {
                "name": "dev-app-data",
                "access_key_id": "key1",
                "secret_access_key": "secret1",
                "endpoint": "https://s3.example.com",
                "region": "us-east-1",
            },
            "backups": {
                "name": "dev-backups",
                "access_key_id": "key2",
                "secret_access_key": "secret2",
                "endpoint": "https://s3.example.com",
                "region": "us-east-1",
            },
            "logs": {
                "name": "dev-logs",
                "access_key_id": "key3",
                "secret_access_key": "secret3",
                "endpoint": "https://s3.example.com",
                "region": "us-east-1",
            },
            "assets": {
                "name": "dev-assets",
                "access_key_id": "key4",
                "secret_access_key": "secret4",
                "endpoint": "https://s3.example.com",
                "region": "us-east-1",
            },
        }
    }
