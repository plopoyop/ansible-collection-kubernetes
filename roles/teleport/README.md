# teleport

Install teleport-cluster

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [teleport_acme_enabled](#teleport_acme_enabled)
  - [teleport_additional_helm_values](#teleport_additional_helm_values)
  - [teleport_authentication_second_factors](#teleport_authentication_second_factors)
  - [teleport_authentication_type](#teleport_authentication_type)
  - [teleport_chart_mode](#teleport_chart_mode)
  - [teleport_cluster_name](#teleport_cluster_name)
  - [teleport_deployment_name](#teleport_deployment_name)
  - [teleport_enabled](#teleport_enabled)
  - [teleport_enterprise](#teleport_enterprise)
  - [teleport_helm_chart_ref](#teleport_helm_chart_ref)
  - [teleport_helm_chart_version](#teleport_helm_chart_version)
  - [teleport_helm_repo_name](#teleport_helm_repo_name)
  - [teleport_helm_repo_url](#teleport_helm_repo_url)
  - [teleport_high_availability_cert_manager_enabled](#teleport_high_availability_cert_manager_enabled)
  - [teleport_high_availability_cert_manager_issuer_kind](#teleport_high_availability_cert_manager_issuer_kind)
  - [teleport_high_availability_cert_manager_issuer_name](#teleport_high_availability_cert_manager_issuer_name)
  - [teleport_high_availability_enabled](#teleport_high_availability_enabled)
  - [teleport_high_availability_replica_count](#teleport_high_availability_replica_count)
  - [teleport_log_format](#teleport_log_format)
  - [teleport_log_level](#teleport_log_level)
  - [teleport_log_output](#teleport_log_output)
  - [teleport_namespace](#teleport_namespace)
  - [teleport_persistence_enabled](#teleport_persistence_enabled)
  - [teleport_persistence_volume_size](#teleport_persistence_volume_size)
  - [teleport_pod_security_policy_enabled](#teleport_pod_security_policy_enabled)
  - [teleport_proxy_listener_mode](#teleport_proxy_listener_mode)
  - [teleport_proxy_service_type](#teleport_proxy_service_type)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### teleport_acme_enabled

Enable ACME (Let's Encrypt) automatic certificate provisioning.
Only works in single-instance (non-HA) mode.

**_Type:_** boolean<br />

#### Default value

```YAML
teleport_acme_enabled: false
```

### teleport_additional_helm_values

Additional Helm values to pass to the teleport-cluster chart.
These values are merged with the generated values, with overrides taking precedence.

**_Type:_** dict<br />

#### Default value

```YAML
teleport_additional_helm_values: {}
```

#### Example usage

```YAML
  teleport_additional_helm_values:
    resources:
      requests:
        cpu: "1"
        memory: "2Gi"
    annotations:
      service:
        external-dns.alpha.kubernetes.io/hostname: "teleport.example.com"
```

### teleport_authentication_second_factors

List of second factor methods to enable.
Options: otp, sso, webauthn

**_Type:_** list<br />

#### Default value

```YAML
teleport_authentication_second_factors:
  - webauthn
  - otp
```

### teleport_authentication_type

Authentication type. Options: local, github (OSS), oidc, saml (Enterprise)

**_Type:_** string<br />

#### Default value

```YAML
teleport_authentication_type: local
```

### teleport_chart_mode

Deployment mode for the Teleport chart.
Supported values: standalone, aws, gcp, azure, scratch

**_Type:_** string<br />

#### Default value

```YAML
teleport_chart_mode: standalone
```

### teleport_cluster_name

The externally-facing public domain name of the Teleport cluster.
This value cannot be changed after cluster deployment.

**_Type:_** string<br />

#### Default value

```YAML
teleport_cluster_name: ''
```

#### Example usage

```YAML
  teleport_cluster_name: "teleport.example.com"
```

### teleport_deployment_name

Deployment name for teleport-cluster helm chart

**_Type:_** string<br />

#### Default value

```YAML
teleport_deployment_name: teleport
```

### teleport_enabled

Should teleport-cluster helm chart be installed

**_Type:_** boolean<br />

#### Default value

```YAML
teleport_enabled: true
```

### teleport_enterprise

Enable Teleport Enterprise mode. Requires a license secret.

**_Type:_** boolean<br />

#### Default value

```YAML
teleport_enterprise: false
```

### teleport_helm_chart_ref

#### Default value

```YAML
teleport_helm_chart_ref: teleport/teleport-cluster
```

### teleport_helm_chart_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
teleport_helm_chart_version: 18.7.1
```

### teleport_helm_repo_name

#### Default value

```YAML
teleport_helm_repo_name: teleport
```

### teleport_helm_repo_url

#### Default value

```YAML
teleport_helm_repo_url: https://charts.releases.teleport.dev
```

### teleport_high_availability_cert_manager_enabled

Use cert-manager for TLS certificates in HA mode

**_Type:_** boolean<br />

#### Default value

```YAML
teleport_high_availability_cert_manager_enabled: false
```

### teleport_high_availability_cert_manager_issuer_kind

Kind of the cert-manager issuer (ClusterIssuer or Issuer)

**_Type:_** string<br />

#### Default value

```YAML
teleport_high_availability_cert_manager_issuer_kind: ClusterIssuer
```

### teleport_high_availability_cert_manager_issuer_name

Name of the cert-manager ClusterIssuer to use

**_Type:_** string<br />

#### Default value

```YAML
teleport_high_availability_cert_manager_issuer_name: letsencrypt-prod
```

### teleport_high_availability_enabled

Enable high availability with multiple replicas

**_Type:_** boolean<br />

#### Default value

```YAML
teleport_high_availability_enabled: false
```

### teleport_high_availability_replica_count

Number of replicas for high availability mode

**_Type:_** integer<br />

#### Default value

```YAML
teleport_high_availability_replica_count: 2
```

### teleport_log_format

Log format. Options: json, text

**_Type:_** string<br />

#### Default value

```YAML
teleport_log_format: json
```

### teleport_log_level

Log level for Teleport. Options: DEBUG, INFO, WARNING, ERROR

**_Type:_** string<br />

#### Default value

```YAML
teleport_log_level: INFO
```

### teleport_log_output

Log output destination. Options: stderr, stdout

**_Type:_** string<br />

#### Default value

```YAML
teleport_log_output: stderr
```

### teleport_namespace

K8s namespace to install the teleport-cluster chart

**_Type:_** string<br />

#### Default value

```YAML
teleport_namespace: teleport
```

### teleport_persistence_enabled

Enable PersistentVolumeClaim for Teleport data storage

**_Type:_** boolean<br />

#### Default value

```YAML
teleport_persistence_enabled: true
```

### teleport_persistence_volume_size

Size of the PersistentVolumeClaim for Teleport data

**_Type:_** string<br />

#### Default value

```YAML
teleport_persistence_volume_size: 10Gi
```

### teleport_pod_security_policy_enabled

Enable PodSecurityPolicy resources. Must be set to false for Kubernetes >= 1.25
as PSP API has been removed.

**_Type:_** boolean<br />

#### Default value

```YAML
teleport_pod_security_policy_enabled: false
```

### teleport_proxy_listener_mode

Proxy listener mode. Use 'multiplex' for TLS routing (single port)
or 'separate' for separate ports per protocol.

**_Type:_** string<br />

#### Default value

```YAML
teleport_proxy_listener_mode: separate
```

### teleport_proxy_service_type

Kubernetes Service type for the Proxy. Options: LoadBalancer, ClusterIP, NodePort

**_Type:_** string<br />

#### Default value

```YAML
teleport_proxy_service_type: LoadBalancer
```

## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
