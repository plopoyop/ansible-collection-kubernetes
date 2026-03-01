import pytest
import os
import boto3
from moto import mock_aws
from ansible.errors import AnsibleUndefinedVariable, AnsibleConnectionFailure
from ansible.parsing.dataloader import DataLoader
from plugins.vars.read_s3_tfstate import VarsModule

LOCAL_FILES_PATH = os.path.join(os.path.dirname(__file__), "resources/")
BUCKET_NAME = "tfstates"
REGION = "us-east-1"
FILES_LIST = [
    "empty_output.tfstate",
    "missing_ansible_vars.tfstate",
    "state_with_vars.tfstate",
    "state_with_vars2.tfstate",
    "state_with_nested_vars.tfstate",
    "state_with_nested_vars2.tfstate",
]


@pytest.fixture
def mock_s3_bucket(autouse=True):
    with mock_aws():
        s3 = boto3.client("s3", region_name=REGION)
        s3.create_bucket(Bucket=BUCKET_NAME)

        for file in FILES_LIST:
            local_file = os.path.join(LOCAL_FILES_PATH, file)
            with open(local_file, "rb") as f:
                s3.put_object(Bucket=BUCKET_NAME, Key=file, Body=f.read())

        yield s3


@pytest.fixture
def set_env_vars():
    os.environ["TF_BACKEND_BUCKET_NAME"] = BUCKET_NAME
    os.environ["AWS_REGION"] = REGION
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"


@pytest.fixture(autouse=True)
def reset_cache():
    VarsModule.CACHE = {}


def test_fail_when_conf_is_missing():
    with pytest.raises(AnsibleUndefinedVariable):
        plugin = VarsModule()

        plugin.get_vars({}, {}, "localhost")


def test_fail_when_tf_state_does_not_exists(set_env_vars):
    with pytest.raises(AnsibleConnectionFailure):
        os.environ["TF_TARGET"] = "missing.tf"

        plugin = VarsModule()
        plugin.get_vars({}, {}, "localhost")


def test_return_empty_when_no_outputs(mock_s3_bucket, set_env_vars):
    os.environ["TF_TARGET"] = "empty_output.tfstate"

    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")

    assert variables == {}


def test_return_empty_if_missing_state(mock_s3_bucket, set_env_vars):
    os.environ["TF_TARGET"] = "missing_ansible_vars.tfstate"

    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")

    assert variables == {}


def test_return_variables_from_single_tf_state(mock_s3_bucket, set_env_vars):
    os.environ["TF_TARGET"] = "state_with_vars.tfstate"

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


def test_return_variables_from_multiple_tf_state(mock_s3_bucket, set_env_vars):
    os.environ["TF_TARGET"] = "state_with_vars.tfstate,state_with_vars2.tfstate"

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


def test_multiple_states_deep_merges_s3_buckets(mock_s3_bucket, set_env_vars):
    os.environ["TF_TARGET"] = (
        "state_with_nested_vars.tfstate,state_with_nested_vars2.tfstate"
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
