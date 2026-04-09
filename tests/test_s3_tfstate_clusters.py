import json
import os
import pytest
from unittest.mock import MagicMock, patch
from plugins.inventory.s3_tfstate_clusters import (
    InventoryModule,
    _extract_clusters,
    _build_inventory,
)

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


# --- Tests for _extract_clusters (shared logic, same as local) ---


def test_extract_clusters_single():
    with open(os.path.join(RESOURCES, "clusters_single.tfstate")) as f:
        tfstate = json.load(f)
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert len(clusters) == 1
    assert "prod-cluster" in clusters
    assert clusters["prod-cluster"]["tags"] == ["production", "eu-west"]


def test_extract_clusters_empty():
    clusters = _extract_clusters({}, "compute_clusters")
    assert clusters == {}


def test_extract_clusters_no_matching_key():
    with open(os.path.join(RESOURCES, "clusters_no_output.tfstate")) as f:
        tfstate = json.load(f)
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert clusters == {}


# --- Tests for _build_inventory (shared logic, same as local) ---


def test_build_inventory_creates_tag_groups():
    inventory = MagicMock()
    inventory.groups = {}
    clusters = {
        "c1": {"name": "c1", "kubeconfig": "", "tags": ["staging", "apps"]},
    }
    _build_inventory(inventory, clusters)
    inventory.add_group.assert_any_call("staging_clusters")
    inventory.add_group.assert_any_call("apps_clusters")
    inventory.add_child.assert_any_call("staging_clusters", "c1")
    inventory.add_child.assert_any_call("apps_clusters", "c1")


# --- Tests for InventoryModule ---


def test_verify_file_valid(tmp_path):
    plugin = InventoryModule()
    yml_file = tmp_path / "s3_tfstate_clusters.yml"
    yml_file.write_text("plugin: plopoyop.kubernetes.s3_tfstate_clusters")
    yaml_file = tmp_path / "s3_tfstate_clusters.yaml"
    yaml_file.write_text("plugin: plopoyop.kubernetes.s3_tfstate_clusters")
    assert plugin.verify_file(str(yml_file)) is True
    assert plugin.verify_file(str(yaml_file)) is True


def test_verify_file_invalid(tmp_path):
    plugin = InventoryModule()
    other = tmp_path / "other.yml"
    other.write_text("")
    old_name = tmp_path / "terraform_s3.yml"
    old_name.write_text("")
    assert plugin.verify_file(str(other)) is False
    assert plugin.verify_file(str(old_name)) is False


@patch("plugins.inventory.s3_tfstate_clusters.HAS_BOTO3", False)
def test_parse_raises_without_boto3():
    plugin = InventoryModule()
    plugin._read_config_data = MagicMock()
    plugin.get_option = MagicMock(return_value=None)

    inventory = MagicMock()
    loader = MagicMock()

    from ansible.errors import AnsibleParserError

    with pytest.raises(AnsibleParserError, match="boto3"):
        plugin.parse(inventory, loader, "/path/to/s3_tfstate_clusters.yml")


@patch("plugins.inventory.s3_tfstate_clusters.HAS_BOTO3", True)
def test_parse_raises_without_bucket_name():
    plugin = InventoryModule()
    plugin._read_config_data = MagicMock()
    plugin.get_option = MagicMock(return_value=None)

    inventory = MagicMock()
    loader = MagicMock()

    from ansible.errors import AnsibleParserError

    with pytest.raises(AnsibleParserError, match="bucket_name"):
        plugin.parse(inventory, loader, "/path/to/s3_tfstate_clusters.yml")


@patch("plugins.inventory.s3_tfstate_clusters.HAS_BOTO3", True)
def test_parse_raises_without_targets():
    plugin = InventoryModule()
    plugin._read_config_data = MagicMock()

    def get_option_side_effect(key):
        if key == "bucket_name":
            return "my-bucket"
        return None

    plugin.get_option = MagicMock(side_effect=get_option_side_effect)

    inventory = MagicMock()
    loader = MagicMock()

    from ansible.errors import AnsibleParserError

    with pytest.raises(AnsibleParserError, match="targets"):
        plugin.parse(inventory, loader, "/path/to/s3_tfstate_clusters.yml")


@patch("plugins.inventory.s3_tfstate_clusters.HAS_BOTO3", True)
@patch("plugins.inventory.s3_tfstate_clusters.boto3")
def test_parse_loads_clusters_from_s3(mock_boto3):
    with open(os.path.join(RESOURCES, "clusters_single.tfstate")) as f:
        tfstate_content = f.read()

    mock_body = MagicMock()
    mock_body.read.return_value = tfstate_content.encode("utf-8")
    mock_object = MagicMock()
    mock_object.get.return_value = {"Body": mock_body}
    mock_s3 = MagicMock()
    mock_s3.Object.return_value = mock_object
    mock_boto3.resource.return_value = mock_s3

    plugin = InventoryModule()
    plugin._read_config_data = MagicMock()

    options = {
        "bucket_name": "my-bucket",
        "targets": "terraform.tfstate",
        "aws_access_key_id": "key",
        "aws_secret_access_key": "secret",
        "aws_region": "us-east-1",
        "s3_endpoint_url": None,
        "clusters_output_key": "compute_clusters",
    }
    plugin.get_option = MagicMock(side_effect=lambda k: options.get(k))

    inventory = MagicMock()
    inventory.groups = {}
    loader = MagicMock()

    plugin.parse(inventory, loader, "/path/to/s3_tfstate_clusters.yml")

    inventory.add_host.assert_called_once_with("prod-cluster", group="k8s_clusters")
    inventory.set_variable.assert_any_call(
        "prod-cluster", "cluster_name", "prod-cluster"
    )


@patch("plugins.inventory.s3_tfstate_clusters.HAS_BOTO3", True)
@patch("plugins.inventory.s3_tfstate_clusters.boto3")
def test_parse_with_custom_endpoint(mock_boto3):
    with open(os.path.join(RESOURCES, "clusters_single.tfstate")) as f:
        tfstate_content = f.read()

    mock_body = MagicMock()
    mock_body.read.return_value = tfstate_content.encode("utf-8")
    mock_object = MagicMock()
    mock_object.get.return_value = {"Body": mock_body}
    mock_s3 = MagicMock()
    mock_s3.Object.return_value = mock_object
    mock_boto3.resource.return_value = mock_s3

    plugin = InventoryModule()
    plugin._read_config_data = MagicMock()

    options = {
        "bucket_name": "my-bucket",
        "targets": "terraform.tfstate",
        "aws_access_key_id": "key",
        "aws_secret_access_key": "secret",
        "aws_region": "gra",
        "s3_endpoint_url": "https://s3.gra.io.cloud.ovh.net",
        "clusters_output_key": "compute_clusters",
    }
    plugin.get_option = MagicMock(side_effect=lambda k: options.get(k))

    inventory = MagicMock()
    inventory.groups = {}
    loader = MagicMock()

    plugin.parse(inventory, loader, "/path/to/s3_tfstate_clusters.yml")

    mock_boto3.resource.assert_called_once_with(
        "s3",
        aws_access_key_id="key",
        aws_secret_access_key="secret",
        region_name="gra",
        endpoint_url="https://s3.gra.io.cloud.ovh.net",
    )
