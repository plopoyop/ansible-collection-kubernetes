import json
import os
from unittest.mock import MagicMock
from plugins.inventory.local_tfstate_clusters import (
    InventoryModule,
    _extract_clusters,
    _build_inventory,
)

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")


# --- Tests for _extract_clusters ---


def test_extract_clusters_single():
    with open(os.path.join(RESOURCES, "clusters_single.tfstate")) as f:
        tfstate = json.load(f)
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert len(clusters) == 1
    assert "prod-cluster" in clusters
    assert clusters["prod-cluster"]["name"] == "prod-cluster"
    assert clusters["prod-cluster"]["tags"] == ["production", "eu-west"]


def test_extract_clusters_multiple():
    with open(os.path.join(RESOURCES, "clusters_multiple.tfstate")) as f:
        tfstate = json.load(f)
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert len(clusters) == 3
    assert "gitops-e2e-tooling" in clusters
    assert "gitops-e2e-prod" in clusters
    assert "gitops-e2e-staging" in clusters


def test_extract_clusters_no_output():
    with open(os.path.join(RESOURCES, "clusters_no_output.tfstate")) as f:
        tfstate = json.load(f)
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert clusters == {}


def test_extract_clusters_empty_outputs():
    tfstate = {"outputs": {}}
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert clusters == {}


def test_extract_clusters_no_outputs_key():
    tfstate = {}
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert clusters == {}


def test_extract_clusters_no_tags():
    with open(os.path.join(RESOURCES, "clusters_no_tags.tfstate")) as f:
        tfstate = json.load(f)
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert len(clusters) == 1
    assert clusters["simple-cluster"]["tags"] == []


def test_extract_clusters_kubeconfig_dict():
    with open(os.path.join(RESOURCES, "clusters_kubeconfig_dict.tfstate")) as f:
        tfstate = json.load(f)
    clusters = _extract_clusters(tfstate, "compute_clusters")
    kubeconfig = clusters["dict-cluster"]["kubeconfig"]
    parsed = json.loads(kubeconfig)
    assert parsed["apiVersion"] == "v1"
    assert parsed["kind"] == "Config"


def test_extract_clusters_custom_output_key():
    tfstate = {
        "outputs": {
            "my_clusters": {"value": {"c1": {"name": "custom-cluster", "tags": []}}}
        }
    }
    clusters = _extract_clusters(tfstate, "my_clusters")
    assert "custom-cluster" in clusters


def test_extract_clusters_uses_key_as_fallback_name():
    tfstate = {
        "outputs": {
            "compute_clusters": {"value": {"my-key": {"kubeconfig": "", "tags": []}}}
        }
    }
    clusters = _extract_clusters(tfstate, "compute_clusters")
    assert "my-key" in clusters
    assert clusters["my-key"]["name"] == "my-key"


# --- Tests for _build_inventory ---


def test_build_inventory_creates_groups():
    inventory = MagicMock()
    inventory.groups = {}
    clusters = {
        "cluster-a": {"name": "cluster-a", "kubeconfig": "", "tags": ["prod"]},
    }
    _build_inventory(inventory, clusters)
    inventory.add_group.assert_any_call("k8s_clusters")
    inventory.add_group.assert_any_call("all_clusters")
    inventory.add_group.assert_any_call("prod_clusters")


def test_build_inventory_adds_hosts():
    inventory = MagicMock()
    inventory.groups = {}
    clusters = {
        "my-cluster": {"name": "my-cluster", "kubeconfig": "cfg", "tags": []},
    }
    _build_inventory(inventory, clusters)
    inventory.add_host.assert_called_once_with("my-cluster", group="k8s_clusters")
    inventory.set_variable.assert_any_call("my-cluster", "ansible_connection", "local")
    inventory.set_variable.assert_any_call("my-cluster", "cluster_name", "my-cluster")
    inventory.set_variable.assert_any_call("my-cluster", "kubeconfig", "cfg")


def test_build_inventory_multiple_tags():
    inventory = MagicMock()
    inventory.groups = {}
    clusters = {
        "c1": {"name": "c1", "kubeconfig": "", "tags": ["prod", "eu-west", "apps"]},
    }
    _build_inventory(inventory, clusters)
    inventory.add_group.assert_any_call("prod_clusters")
    inventory.add_group.assert_any_call("eu_west_clusters")
    inventory.add_group.assert_any_call("apps_clusters")
    inventory.add_child.assert_any_call("prod_clusters", "c1")
    inventory.add_child.assert_any_call("eu_west_clusters", "c1")
    inventory.add_child.assert_any_call("apps_clusters", "c1")


def test_build_inventory_sanitizes_tags():
    inventory = MagicMock()
    inventory.groups = {}
    clusters = {
        "c1": {"name": "c1", "kubeconfig": "", "tags": ["My Tag.v2"]},
    }
    _build_inventory(inventory, clusters)
    inventory.add_group.assert_any_call("my_tag_v2_clusters")


def test_build_inventory_empty_clusters():
    inventory = MagicMock()
    inventory.groups = {}
    _build_inventory(inventory, {})
    inventory.add_group.assert_any_call("k8s_clusters")
    inventory.add_group.assert_any_call("all_clusters")
    inventory.add_host.assert_not_called()


# --- Tests for InventoryModule ---


def test_verify_file_valid(tmp_path):
    plugin = InventoryModule()
    yml_file = tmp_path / "local_tfstate_clusters.yml"
    yml_file.write_text("plugin: plopoyop.kubernetes.local_tfstate_clusters")
    yaml_file = tmp_path / "local_tfstate_clusters.yaml"
    yaml_file.write_text("plugin: plopoyop.kubernetes.local_tfstate_clusters")
    assert plugin.verify_file(str(yml_file)) is True
    assert plugin.verify_file(str(yaml_file)) is True


def test_verify_file_invalid(tmp_path):
    plugin = InventoryModule()
    other = tmp_path / "other.yml"
    other.write_text("")
    old_name = tmp_path / "terraform_local.yml"
    old_name.write_text("")
    assert plugin.verify_file(str(other)) is False
    assert plugin.verify_file(str(old_name)) is False
