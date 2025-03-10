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
FILES_LIST = ["empty_output.tfstate",
              "missing_ansible_vars.tfstate",
              "missing_ansible_vars.tfstate",
              "state_with_vars.tfstate",
              "state_with_vars2.tfstate"]


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
    os.environ['TF_BACKEND_BUCKET_NAME'] = BUCKET_NAME
    os.environ['AWS_REGION'] = REGION
    os.environ['AWS_ACCESS_KEY_ID'] = "testing"
    os.environ['AWS_SECRET_ACCESS_KEY'] = "testing"


@pytest.fixture(autouse=True)
def reset_cache():
    VarsModule.CACHE = {}


def test_fail_when_conf_is_missing():
    with pytest.raises(AnsibleUndefinedVariable):
        plugin = VarsModule()

        plugin.get_vars({}, {}, "localhost")


def test_fail_when_tf_state_does_not_exists(set_env_vars):
    with pytest.raises(AnsibleConnectionFailure):
        os.environ['TF_TARGET'] = "missing.tf"

        plugin = VarsModule()
        plugin.get_vars({}, {}, "localhost")


def test_return_empty_when_no_outputs(mock_s3_bucket, set_env_vars):
    os.environ['TF_TARGET'] = "empty_output.tfstate"

    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")

    assert variables == {}


def test_return_empty_if_missing_state(mock_s3_bucket, set_env_vars):
    os.environ['TF_TARGET'] = "missing_ansible_vars.tfstate"

    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")

    assert variables == {}


def test_return_variables_from_single_tf_state(mock_s3_bucket, set_env_vars):
    os.environ['TF_TARGET'] = "state_with_vars.tfstate"

    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {"key": "value"}


def test_return_variables_from_multiple_tf_state(mock_s3_bucket, set_env_vars):
    os.environ[
        'TF_TARGET'] = "state_with_vars.tfstate,state_with_vars2.tfstate"

    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {"key": "value", "key2": "value2"}
