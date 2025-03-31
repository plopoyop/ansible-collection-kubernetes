import pytest
import os
from ansible.errors import AnsibleUndefinedVariable, AnsibleConnectionFailure
from ansible.parsing.dataloader import DataLoader
from plugins.vars.read_local_tfstate import VarsModule


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
    file_path = os.path.join(
        os.path.dirname(__file__), "resources/empty_output.tfstate"
    )

    os.environ["TF_STATES_PATHS"] = file_path
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {}


def test_return_empty_if_missing_state():
    file_path = os.path.join(
        os.path.dirname(__file__), "resources/missing_ansible_vars.tfstate"
    )
    os.environ["TF_STATES_PATHS"] = file_path
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {}


def test_return_variables_from_single_tf_state():
    file_path = os.path.join(
        os.path.dirname(__file__), "resources/state_with_vars.tfstate"
    )
    os.environ["TF_STATES_PATHS"] = file_path
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {"key": "value"}


def test_return_variables_from_multiple_tf_state():
    file_path = os.path.join(
        os.path.dirname(__file__), "resources/state_with_vars.tfstate"
    )
    file_path2 = os.path.join(
        os.path.dirname(__file__), "resources/state_with_vars2.tfstate"
    )

    os.environ["TF_STATES_PATHS"] = file_path + "," + file_path2
    plugin = VarsModule()
    variables = plugin.get_vars(DataLoader(), {}, "localhost")
    assert variables == {"key": "value", "key2": "value2"}
