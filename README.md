# Ansible Collection for Kubernetes - plopoyop.kubernetes

## Description

This Ansible collection provides a set of roles to install and configure various tools on a Kubernetes cluster using their helm charts. The goal is to simplify and automate the deployment of these tools using Ansible.

## Contents

This collection includes multiple Ansible roles designed to install and configure essential tools for a Kubernetes cluster. Each role is designed to be as configurable as possible while providing default settings tailored to my specific usage.

## Disclaimer

The roles provided in this collection are developed based on my usage of the tools and my specific needs. While configuration options are available to adjust their behavior, not all possible options are necessarily supported.

Before using this collection in production, ensure that the default configurations meet your needs and adjust them if necessary.

## Prerequisites

- Ansible >= 2.9
- A running Kubernetes cluster
- Administrator access to cluster nodes (if required for certain installations)

## Installation

To install this collection, use the following command:

```sh
ansible-galaxy collection install plopoyop.kubernetes
```

## Usage

You can call the roles from this collection in your Ansible playbooks as follows:

```yaml
- name: Install a tool on Kubernetes
  hosts: localhost
  roles:
    - role: plopoyop.kubernetes.role_name
      vars:
        config_option: value
```

## Collection content
### List of Roles and Helm Chart Versions

| Role Name       | Helm Chart Version | README Link                                 |
| ---------       | ------------------ | ------------------------------------        |
| ExternalDNS         | v1.20.0            | [View README](roles/external_dns/README.md)       |
| metallb         | v0.15.3            | [View README](roles/metallb/README.md)     |
| traefik         | v39.0.8            | [View README](roles/traefik/README.md)      |
| cert\_manager   | v0.17.1            | [View README](roles/cert_manager/README.md) |
| CrowdSec        | v0.23.0            | [View README](roles/crowdsec/README.md)     |
| mongodb community operator | v0.13.0            | [View README](roles/mongodb/README.md) |
| Rancher         | v2.14.1            | [View README](roles/rancher/README.md) |

## Customization

Each role exposes variables to adjust the configuration of the installed tools. Refer to each role's documentation for available variables.

## Plugins
This collection includes custom plugins to extend Ansible’s functionality.

### read_local_tfstate
**Description:** This plugin allows you to get variables from multiple local terraform tfstates with a `ansible_vars` output.

#### Configuration via Environment Variables
| Variable Name          | Description                            | Example Value |
|------------------------|----------------------------------------|--------------|
| `ANSIBLE_VARS_ENABLED`       | Ansible env var of which vars plugins are envabled | `host_group_vars,plopoyop.kubernetes.read_local_tfstate`  |
| `TF_STATES_PATHS`       | Local path for tfstate | `$PWD/terraform/terraform.tfstate,$PWD/terraform2/terraform.tfstate`  |

To set these variables, you can use:
```sh
export ANSIBLE_VARS_ENABLED="host_group_vars,plopoyop.kubernetes.read_local_tfstate"
export TF_STATES_PATHS="$PWD/terraform/terraform.tfstate"
```

### read_s3_tfstate
**Description:** This plugin allows you to get variables from multiple tfstates stored on S3 with a `ansible_vars` output.

#### Configuration via Environment Variables
| Variable Name          | Description                            | Example Value |
|------------------------|----------------------------------------|--------------|
| `TF_BACKEND_BUCKET_NAME`       | Name of the S3 bucket | `tfstates`  |
| `AWS_ENDPOINT_URL`       | S3 endpoint to use | `s3.amazonaws.com`  |
| `AWS_REGION`       | S3 region | `us-east-1`  |
| `AWS_ACCESS_KEY_ID`       | Access key Id | `your access key id`  |
| `AWS_SECRET_ACCESS_KEY`       | Secret Access Key | `your secret access key`  |
| `TF_TARGET`       | Path to tfstate files in the bucket | `prod/terraform.tfstate,dev/terraform.tfstate`  |


To set these variables, you can use:
```sh
TF_BACKEND_BUCKET_NAME="tfstates"
AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="accesskeyid"
AWS_SECRET_ACCESS_KEY="secretaccesskey"
TF_TARGET="prod/terraform.tfstate,dev/terraform.tfstate"
```

### local_tfstate_clusters
**Type:** Inventory plugin

**Description:** Generates a dynamic Ansible inventory from local Terraform state files. It reads the `compute_clusters` output and creates hosts with kubeconfig variables, grouped by tags.

#### Usage

Create an inventory file named `local_tfstate_clusters.yml`:
```yaml
plugin: plopoyop.kubernetes.local_tfstate_clusters
tfstate_paths: "./terraform/terraform.tfstate"
clusters_output_key: compute_clusters
```

#### Options
| Option                | Description                                         | Default            | Env Variable      |
|-----------------------|-----------------------------------------------------|--------------------|--------------------|
| `tfstate_paths`       | Comma-separated list of local tfstate file paths    | -                  | `TF_STATES_PATHS`  |
| `clusters_output_key` | Terraform output key containing cluster data        | `compute_clusters` | -                  |

#### Expected Terraform Output Format
```hcl
output "compute_clusters" {
  value = {
    "cluster-name" = {
      name       = "my-cluster"
      kubeconfig = "..."
      tags       = ["production", "eu-west"]
    }
  }
}
```

#### Generated Inventory
- Group `k8s_clusters`: all clusters
- Group `{tag}_clusters`: one group per tag (e.g., `production_clusters`, `eu_west_clusters`)
- Host variables: `ansible_connection`, `cluster_name`, `kubeconfig`

### s3_tfstate_clusters
**Type:** Inventory plugin

**Description:** Generates a dynamic Ansible inventory from Terraform state files stored in an S3-compatible bucket. Supports AWS S3, MinIO, and other S3-compatible providers.

#### Usage

Create an inventory file named `s3_tfstate_clusters.yml`:
```yaml
plugin: plopoyop.kubernetes.s3_tfstate_clusters
bucket_name: my-terraform-state
targets: "terraform.tfstate"
aws_region: eu-west-1
```

#### Options
| Option                  | Description                                           | Default       | Env Variable              |
|-------------------------|-------------------------------------------------------|---------------|----------------------------|
| `bucket_name`           | S3 bucket containing Terraform state files            | -             | `TF_BACKEND_BUCKET_NAME`   |
| `targets`               | Comma-separated list of state file keys in the bucket | -             | `TF_TARGET`                |
| `aws_access_key_id`     | AWS access key ID                                     | -             | `AWS_ACCESS_KEY_ID`        |
| `aws_secret_access_key` | AWS secret access key                                 | -             | `AWS_SECRET_ACCESS_KEY`    |
| `aws_region`            | AWS region                                            | `us-east-1`   | `AWS_REGION`               |
| `s3_endpoint_url`       | Custom S3 endpoint URL (MinIO, etc.)                  | -             | `AWS_S3_ENDPOINT`          |
| `clusters_output_key`   | Terraform output key containing cluster data          | `compute_clusters` | -                      |

#### Requirements
- `boto3` Python package

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve the roles and add new features.

## Tools
[Devbox](https://www.jetify.com/docs/devbox) is used to make reproducible development environments
[Task](https://taskfile.dev/) as a task runner
[Renovate](https://github.com/renovatebot/renovate) to update dependencies

## License

This collection is distributed under the Mozilla Public License Version 2.0 license.
