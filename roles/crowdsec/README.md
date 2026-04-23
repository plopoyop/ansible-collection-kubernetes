# crowdsec

Install CrowdSec on kubernetes

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [crowdsec_additional_helm_values](#crowdsec_additional_helm_values)
  - [crowdsec_agent_acquisition](#crowdsec_agent_acquisition)
  - [crowdsec_agent_additional_acquisition](#crowdsec_agent_additional_acquisition)
  - [crowdsec_agent_collections](#crowdsec_agent_collections)
  - [crowdsec_agent_enabled](#crowdsec_agent_enabled)
  - [crowdsec_agent_env](#crowdsec_agent_env)
  - [crowdsec_agent_host_var_log](#crowdsec_agent_host_var_log)
  - [crowdsec_agent_is_deployment](#crowdsec_agent_is_deployment)
  - [crowdsec_agent_resources](#crowdsec_agent_resources)
  - [crowdsec_appsec_acquisitions](#crowdsec_appsec_acquisitions)
  - [crowdsec_appsec_collections](#crowdsec_appsec_collections)
  - [crowdsec_appsec_configs](#crowdsec_appsec_configs)
  - [crowdsec_appsec_enabled](#crowdsec_appsec_enabled)
  - [crowdsec_appsec_env](#crowdsec_appsec_env)
  - [crowdsec_appsec_replicas](#crowdsec_appsec_replicas)
  - [crowdsec_appsec_resources](#crowdsec_appsec_resources)
  - [crowdsec_appsec_service_type](#crowdsec_appsec_service_type)
  - [crowdsec_bouncers](#crowdsec_bouncers)
  - [crowdsec_container_runtime](#crowdsec_container_runtime)
  - [crowdsec_deployment_name](#crowdsec_deployment_name)
  - [crowdsec_enabled](#crowdsec_enabled)
  - [crowdsec_helm_chart_version](#crowdsec_helm_chart_version)
  - [crowdsec_lapi_cs_lapi_secret](#crowdsec_lapi_cs_lapi_secret)
  - [crowdsec_lapi_enabled](#crowdsec_lapi_enabled)
  - [crowdsec_lapi_env](#crowdsec_lapi_env)
  - [crowdsec_lapi_ingress_annotations](#crowdsec_lapi_ingress_annotations)
  - [crowdsec_lapi_ingress_class_name](#crowdsec_lapi_ingress_class_name)
  - [crowdsec_lapi_ingress_enabled](#crowdsec_lapi_ingress_enabled)
  - [crowdsec_lapi_ingress_host](#crowdsec_lapi_ingress_host)
  - [crowdsec_lapi_persistence_config_enabled](#crowdsec_lapi_persistence_config_enabled)
  - [crowdsec_lapi_persistence_config_size](#crowdsec_lapi_persistence_config_size)
  - [crowdsec_lapi_persistence_config_storage_class](#crowdsec_lapi_persistence_config_storage_class)
  - [crowdsec_lapi_persistence_data_enabled](#crowdsec_lapi_persistence_data_enabled)
  - [crowdsec_lapi_persistence_data_size](#crowdsec_lapi_persistence_data_size)
  - [crowdsec_lapi_persistence_data_storage_class](#crowdsec_lapi_persistence_data_storage_class)
  - [crowdsec_lapi_registration_token](#crowdsec_lapi_registration_token)
  - [crowdsec_lapi_replicas](#crowdsec_lapi_replicas)
  - [crowdsec_lapi_resources](#crowdsec_lapi_resources)
  - [crowdsec_lapi_service_type](#crowdsec_lapi_service_type)
  - [crowdsec_metrics_enabled](#crowdsec_metrics_enabled)
  - [crowdsec_metrics_service_monitor_enabled](#crowdsec_metrics_service_monitor_enabled)
  - [crowdsec_namespace](#crowdsec_namespace)
  - [crowdsec_secrets_password](#crowdsec_secrets_password)
  - [crowdsec_secrets_username](#crowdsec_secrets_username)
  - [crowdsec_tls_cert_manager_enabled](#crowdsec_tls_cert_manager_enabled)
  - [crowdsec_tls_enabled](#crowdsec_tls_enabled)
  - [crowdsec_wait_install](#crowdsec_wait_install)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### crowdsec_additional_helm_values

Additional helm values to merge with the rendered values (escape hatch for fine-grained tuning)

**_Type:_** dict<br />

#### Default value

```YAML
crowdsec_additional_helm_values: {}
```

### crowdsec_agent_acquisition

Pod log acquisition definitions (namespace, podName, program, etc.).
See https://docs.crowdsec.net/docs/next/data_sources/intro

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_agent_acquisition: []
```

#### Example usage

```YAML
  crowdsec_agent_acquisition:
    - namespace: "ingress-traefik-controller"
      podName: "traefik-*"
      program: "traefik"
```

### crowdsec_agent_additional_acquisition

Extra log acquisition sources (non-pod datasources such as syslog, kinesis, etc.)

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_agent_additional_acquisition: []
```

### crowdsec_agent_collections

CrowdSec hub collections installed in the agent pod via the
COLLECTIONS env var. The Docker image already ships with
`crowdsecurity/linux`, `crowdsecurity/sshd` and
`crowdsecurity/whitelist-good-actors`; list here only the extra
collections matching your agent acquisitions (e.g.
`crowdsecurity/traefik` when scraping Traefik pod logs).

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_agent_collections: []
```

#### Example usage

```YAML
  crowdsec_agent_collections:
    - "crowdsecurity/traefik"
```

### crowdsec_agent_enabled

Enable the CrowdSec agent (DaemonSet by default)

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_agent_enabled: true
```

### crowdsec_agent_env

Extra environment variables injected into the agent container.
The COLLECTIONS var built from crowdsec_agent_collections is
appended automatically.

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_agent_env: []
```

### crowdsec_agent_host_var_log

Mount host /var/log into the agent pod

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_agent_host_var_log: true
```

### crowdsec_agent_is_deployment

Deploy agent as a Deployment instead of a DaemonSet

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_agent_is_deployment: false
```

### crowdsec_agent_resources

Resource requests and limits for the agent container. Empty dict
lets the chart use its own defaults. When the agent runs as a
DaemonSet this request applies to every node, so keep it low.

**_Type:_** dict<br />

#### Default value

```YAML
crowdsec_agent_resources: {}
```

#### Example usage

```YAML
  crowdsec_agent_resources:
    requests:
      cpu: "50m"
      memory: "64Mi"
    limits:
      cpu: "200m"
      memory: "128Mi"
```

### crowdsec_appsec_acquisitions

AppSec acquisitions (datasource listeners, typically on :7422).
When empty and AppSec is enabled, a default listener on 0.0.0.0:7422
referencing `crowdsecurity/appsec-default` is created.

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_appsec_acquisitions: []
```

#### Example usage

```YAML
  crowdsec_appsec_acquisitions:
    - source: "appsec"
      listen_addr: "0.0.0.0:7422"
      path: "/"
      appsec_config: "crowdsecurity/appsec-default"
      labels:
        type: "appsec"
```

### crowdsec_appsec_collections

CrowdSec hub collections installed in the AppSec pod via the COLLECTIONS
env var. Typical values are `crowdsecurity/appsec-virtual-patching` and
`crowdsecurity/appsec-generic-rules`.

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_appsec_collections: []
```

#### Example usage

```YAML
  crowdsec_appsec_collections:
    - "crowdsecurity/appsec-virtual-patching"
    - "crowdsecurity/appsec-generic-rules"
```

### crowdsec_appsec_configs

AppSec configuration files (key = filename, value = file content).
When empty and AppSec is enabled, a default `appsec-default.yaml`
referencing virtual-patching + generic-rules is created.

**_Type:_** dict<br />

#### Default value

```YAML
crowdsec_appsec_configs: {}
```

#### Example usage

```YAML
  crowdsec_appsec_configs:
    appsec-default.yaml: |
      name: crowdsecurity/appsec-default
      default_remediation: ban
      inband_rules:
        - crowdsecurity/base-config
        - crowdsecurity/vpatch-*
        - crowdsecurity/generic-*
```

### crowdsec_appsec_enabled

Enable the AppSec (WAF) component. Requires a registration token set
via `crowdsec_lapi_registration_token` so the AppSec pod can register
itself against LAPI.

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_appsec_enabled: false
```

### crowdsec_appsec_env

Extra environment variables injected into the AppSec container.
The COLLECTIONS var built from crowdsec_appsec_collections is appended
automatically.

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_appsec_env: []
```

### crowdsec_appsec_replicas

Number of replicas for the AppSec Deployment

**_Type:_** integer<br />

#### Default value

```YAML
crowdsec_appsec_replicas: 1
```

### crowdsec_appsec_resources

Resource requests and limits for the AppSec container. Empty dict
lets the chart use its own defaults (500m CPU / 250Mi RAM request,
which is oversized for most dev clusters).

**_Type:_** dict<br />

#### Default value

```YAML
crowdsec_appsec_resources: {}
```

#### Example usage

```YAML
  crowdsec_appsec_resources:
    requests:
      cpu: "50m"
      memory: "128Mi"
    limits:
      cpu: "500m"
      memory: "256Mi"
```

### crowdsec_appsec_service_type

Kubernetes Service type for the AppSec listener

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_appsec_service_type: ClusterIP
```

### crowdsec_bouncers

Bouncers to pre-register on LAPI first boot (name + API key pairs).

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_bouncers: []
```

#### Example usage

```YAML
  crowdsec_bouncers:
    - name: "traefik"
      key: "{{ crowdsec_traefik_bouncer_key }}"
```

### crowdsec_container_runtime

Container runtime used by the cluster for raw logs format (docker or containerd)

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_container_runtime: containerd
```

### crowdsec_deployment_name

Deployment name for CrowdSec helm chart

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_deployment_name: crowdsec
```

### crowdsec_enabled

Should CrowdSec helm chart be installed

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_enabled: true
```

### crowdsec_helm_chart_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_helm_chart_version: 0.23.0
```

### crowdsec_lapi_cs_lapi_secret

Shared LAPI secret (must be >64 chars). Randomly generated if empty; provide a stable value for idempotent upgrades.

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_cs_lapi_secret: ''
```

### crowdsec_lapi_enabled

Enable the CrowdSec Local API deployment

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_lapi_enabled: true
```

### crowdsec_lapi_env

Extra environment variables injected into the LAPI container.
Bouncer env vars from crowdsec_bouncers are appended automatically.

**_Type:_** list<br />

#### Default value

```YAML
crowdsec_lapi_env: []
```

### crowdsec_lapi_ingress_annotations

Annotations for the LAPI ingress

**_Type:_** dict<br />

#### Default value

```YAML
crowdsec_lapi_ingress_annotations: {}
```

### crowdsec_lapi_ingress_class_name

Ingress class name for the LAPI ingress

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_ingress_class_name: ''
```

### crowdsec_lapi_ingress_enabled

Enable ingress for the LAPI service

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_lapi_ingress_enabled: false
```

### crowdsec_lapi_ingress_host

Hostname for the LAPI ingress

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_ingress_host: ''
```

### crowdsec_lapi_persistence_config_enabled

Enable persistent volume for LAPI config folder (stores API credentials)

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_lapi_persistence_config_enabled: true
```

### crowdsec_lapi_persistence_config_size

Requested size for the LAPI config PVC

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_persistence_config_size: 100Mi
```

### crowdsec_lapi_persistence_config_storage_class

StorageClass name for the LAPI config PVC (empty uses the cluster default)

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_persistence_config_storage_class: ''
```

### crowdsec_lapi_persistence_data_enabled

Enable persistent volume for LAPI data folder (stores registered bouncer API keys)

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_lapi_persistence_data_enabled: true
```

### crowdsec_lapi_persistence_data_size

Requested size for the LAPI data PVC

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_persistence_data_size: 1Gi
```

### crowdsec_lapi_persistence_data_storage_class

StorageClass name for the LAPI data PVC (empty uses the cluster default)

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_persistence_data_storage_class: ''
```

### crowdsec_lapi_registration_token

Registration token for AppSec (must be >48 chars). Randomly generated if empty; provide a stable value for idempotent upgrades.

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_registration_token: ''
```

### crowdsec_lapi_replicas

Number of replicas for the Local API deployment

**_Type:_** integer<br />

#### Default value

```YAML
crowdsec_lapi_replicas: 1
```

### crowdsec_lapi_resources

Resource requests and limits for the LAPI container. Empty dict
lets the chart use its own defaults.

**_Type:_** dict<br />

#### Default value

```YAML
crowdsec_lapi_resources: {}
```

#### Example usage

```YAML
  crowdsec_lapi_resources:
    requests:
      cpu: "50m"
      memory: "128Mi"
    limits:
      cpu: "500m"
      memory: "256Mi"
```

### crowdsec_lapi_service_type

Kubernetes Service type for LAPI

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_lapi_service_type: ClusterIP
```

### crowdsec_metrics_enabled

Expose Prometheus metrics on port 6060 for LAPI and agent

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_metrics_enabled: true
```

### crowdsec_metrics_service_monitor_enabled

Create ServiceMonitor resources for Prometheus Operator (LAPI + agent)

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_metrics_service_monitor_enabled: false
```

### crowdsec_namespace

K8s namespace to install the CrowdSec chart

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_namespace: crowdsec
```

### crowdsec_secrets_password

Shared agent password (randomly generated if empty). Provide a stable value via Ansible Vault for idempotent upgrades.

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_secrets_password: ''
```

### crowdsec_secrets_username

Shared agent username (randomly generated if empty). Provide a stable value via Ansible Vault for idempotent upgrades.

**_Type:_** string<br />

#### Default value

```YAML
crowdsec_secrets_username: ''
```

### crowdsec_tls_cert_manager_enabled

Use cluster cert-manager to issue CrowdSec TLS certificates

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_tls_cert_manager_enabled: true
```

### crowdsec_tls_enabled

Enable mTLS between agent/appsec and LAPI. Requires cert-manager when certManager integration is used.

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_tls_enabled: false
```

### crowdsec_wait_install

Wait for helm install to finish

**_Type:_** boolean<br />

#### Default value

```YAML
crowdsec_wait_install: true
```

## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
