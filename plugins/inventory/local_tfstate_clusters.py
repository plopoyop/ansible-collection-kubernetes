from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin

DOCUMENTATION = """
    name: plopoyop.kubernetes.local_tfstate_clusters
    version_added: "7.1.0"
    short_description: Generate inventory from local Terraform state files
    description:
        - Reads local Terraform state files
        - Extracts compute_clusters from Terraform outputs
        - Creates groups based on cluster tags
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['plopoyop.kubernetes.local_tfstate_clusters']
        tfstate_paths:
            description: >
                Comma-separated list of local Terraform state file paths.
                Can also be set via TF_STATES_PATHS environment variable.
            type: str
            required: false
            env:
                - name: TF_STATES_PATHS
        clusters_output_key:
            description: Key of the Terraform output containing cluster data.
            type: str
            default: compute_clusters
            required: false
"""

EXAMPLES = """
# local_tfstate_clusters.yml
plugin: plopoyop.kubernetes.local_tfstate_clusters
tfstate_paths: "/path/to/terraform.tfstate,/path/to/other.tfstate"
clusters_output_key: compute_clusters
"""


def _extract_clusters(tfstate, clusters_output_key):
    """Extract clusters from a parsed Terraform state."""
    clusters = {}

    if not tfstate.get("outputs"):
        return clusters

    if clusters_output_key not in tfstate["outputs"]:
        return clusters

    compute_clusters = tfstate["outputs"][clusters_output_key]["value"]

    if not isinstance(compute_clusters, dict):
        return clusters

    for cluster_key, cluster_data in compute_clusters.items():
        cluster_name = cluster_data.get("name", cluster_key)

        tags = cluster_data.get("tags", [])
        if not isinstance(tags, list):
            tags = []

        kubeconfig = cluster_data.get("kubeconfig", "")
        if isinstance(kubeconfig, dict):
            kubeconfig = json.dumps(kubeconfig)
        elif not isinstance(kubeconfig, str):
            kubeconfig = ""

        clusters[cluster_name] = {
            "name": cluster_name,
            "kubeconfig": kubeconfig,
            "tags": tags,
        }

    return clusters


def _build_inventory(inventory, clusters):
    """Build Ansible inventory from clusters data."""
    inventory.add_group("k8s_clusters")
    inventory.add_group("all_clusters")

    for cluster_key, cluster_data in clusters.items():
        cluster_hostname = cluster_data.get("name", cluster_key)

        inventory.add_host(cluster_hostname, group="k8s_clusters")
        inventory.set_variable(cluster_hostname, "ansible_connection", "local")
        inventory.set_variable(
            cluster_hostname, "cluster_name", cluster_data.get("name", cluster_key)
        )
        inventory.set_variable(
            cluster_hostname, "kubeconfig", cluster_data.get("kubeconfig", "")
        )

        inventory.add_child("all_clusters", cluster_hostname)

        for tag in cluster_data.get("tags", []):
            if not tag:
                continue
            tag_sanitized = (
                str(tag).lower().replace(" ", "_").replace("-", "_").replace(".", "_")
            )
            tag_sanitized = "".join(c for c in tag_sanitized if c.isalnum() or c == "_")
            group_name = "{}_clusters".format(tag_sanitized)

            if group_name not in inventory.groups:
                inventory.add_group(group_name)

            inventory.add_child(group_name, cluster_hostname)


class InventoryModule(BaseInventoryPlugin):
    """Inventory plugin for Terraform clusters from local state files."""

    NAME = "plopoyop.kubernetes.local_tfstate_clusters"

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(
                ("local_tfstate_clusters.yml", "local_tfstate_clusters.yaml")
            ):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)

        tfstate_paths = self.get_option("tfstate_paths")
        if not tfstate_paths:
            tfstate_paths = os.getenv("TF_STATES_PATHS")

        clusters_output_key = self.get_option("clusters_output_key")

        if not tfstate_paths:
            raise AnsibleParserError(
                "tfstate_paths is required (set TF_STATES_PATHS env var or tfstate_paths option)"
            )

        all_clusters = {}

        for tf_path in tfstate_paths.split(","):
            tf_path = tf_path.strip()
            if not tf_path:
                continue

            tf_path = os.path.expanduser(tf_path)
            tf_path = os.path.expandvars(tf_path)

            if not os.path.exists(tf_path):
                self.display.warning(
                    "Terraform state file not found: {}".format(tf_path)
                )
                continue

            try:
                with open(tf_path, "r") as f:
                    tfstate = json.loads(f.read())

                clusters = _extract_clusters(tfstate, clusters_output_key)
                all_clusters.update(clusters)

            except Exception as e:
                raise AnsibleError(
                    "Failed to load Terraform state from {}: {}".format(tf_path, str(e))
                )

        _build_inventory(inventory, all_clusters)
