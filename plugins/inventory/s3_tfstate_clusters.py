from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin

try:
    import boto3

    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

DOCUMENTATION = """
    name: plopoyop.kubernetes.s3_tfstate_clusters
    version_added: "7.1.0"
    short_description: Generate inventory from Terraform state stored on S3
    description:
        - Reads Terraform state files from an S3-compatible bucket
        - Extracts compute_clusters from Terraform outputs
        - Creates groups based on cluster tags
    requirements:
        - boto3
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['plopoyop.kubernetes.s3_tfstate_clusters']
        bucket_name:
            description: S3 bucket containing Terraform state files.
            type: str
            required: false
            env:
                - name: TF_BACKEND_BUCKET_NAME
        targets:
            description: Comma-separated list of Terraform state file keys in the S3 bucket.
            type: str
            required: false
            env:
                - name: TF_TARGET
        aws_access_key_id:
            description: AWS access key ID for S3 authentication.
            type: str
            required: false
            env:
                - name: AWS_ACCESS_KEY_ID
        aws_secret_access_key:
            description: AWS secret access key for S3 authentication.
            type: str
            required: false
            secret: true
            env:
                - name: AWS_SECRET_ACCESS_KEY
        aws_region:
            description: AWS region for the S3 bucket.
            type: str
            default: us-east-1
            required: false
            env:
                - name: AWS_REGION
        s3_endpoint_url:
            description: Custom S3 endpoint URL (for S3-compatible providers like OVH, MinIO).
            type: str
            required: false
            env:
                - name: AWS_S3_ENDPOINT
        clusters_output_key:
            description: Key of the Terraform output containing cluster data.
            type: str
            default: compute_clusters
            required: false
"""

EXAMPLES = """
# s3_tfstate_clusters.yml
plugin: plopoyop.kubernetes.s3_tfstate_clusters
bucket_name: my-terraform-state
targets: "env/prod/terraform.tfstate,env/staging/terraform.tfstate"
aws_region: eu-west-1
clusters_output_key: compute_clusters

# With OVH S3-compatible storage
# s3_tfstate_clusters.yml
plugin: plopoyop.kubernetes.s3_tfstate_clusters
bucket_name: my-terraform-state
targets: "terraform.tfstate"
s3_endpoint_url: "https://s3.gra.io.cloud.ovh.net"
aws_region: gra
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
    """Inventory plugin for Terraform clusters from S3 state files."""

    NAME = "plopoyop.kubernetes.s3_tfstate_clusters"

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(("s3_tfstate_clusters.yml", "s3_tfstate_clusters.yaml")):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)

        if not HAS_BOTO3:
            raise AnsibleParserError("boto3 is required for this inventory plugin")

        bucket_name = self.get_option("bucket_name")
        targets = self.get_option("targets")
        aws_access_key_id = self.get_option("aws_access_key_id")
        aws_secret_access_key = self.get_option("aws_secret_access_key")
        aws_region = self.get_option("aws_region")
        s3_endpoint_url = self.get_option("s3_endpoint_url")
        clusters_output_key = self.get_option("clusters_output_key")

        if not bucket_name:
            raise AnsibleParserError(
                "bucket_name is required (set TF_BACKEND_BUCKET_NAME env var or bucket_name option)"
            )
        if not targets:
            raise AnsibleParserError(
                "targets is required (set TF_TARGET env var or targets option)"
            )

        s3_kwargs = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "region_name": aws_region,
        }
        if s3_endpoint_url:
            s3_kwargs["endpoint_url"] = s3_endpoint_url

        try:
            s3 = boto3.resource("s3", **s3_kwargs)
        except Exception as e:
            raise AnsibleError("Failed to connect to S3: {}".format(str(e)))

        all_clusters = {}

        for target in targets.split(","):
            target = target.strip()
            if not target:
                continue

            try:
                content_object = s3.Object(bucket_name, target)
                tfstate_content = content_object.get()["Body"].read().decode("utf-8")
                tfstate = json.loads(tfstate_content)

                clusters = _extract_clusters(tfstate, clusters_output_key)
                all_clusters.update(clusters)

            except Exception as e:
                self.display.warning(
                    "Failed to load state from {}: {}".format(target, str(e))
                )
                continue

        _build_inventory(inventory, all_clusters)
