# rancher

Install rancher

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [rancher_additional_helm_values](#rancher_additional_helm_values)
  - [rancher_additional_trusted_cas](#rancher_additional_trusted_cas)
  - [rancher_anti_affinity](#rancher_anti_affinity)
  - [rancher_audit_log_destination](#rancher_audit_log_destination)
  - [rancher_audit_log_enabled](#rancher_audit_log_enabled)
  - [rancher_audit_log_level](#rancher_audit_log_level)
  - [rancher_bootstrap_password](#rancher_bootstrap_password)
  - [rancher_debug](#rancher_debug)
  - [rancher_deployment_name](#rancher_deployment_name)
  - [rancher_enabled](#rancher_enabled)
  - [rancher_helm_chart_ref](#rancher_helm_chart_ref)
  - [rancher_helm_chart_version](#rancher_helm_chart_version)
  - [rancher_helm_repo_name](#rancher_helm_repo_name)
  - [rancher_helm_repo_url](#rancher_helm_repo_url)
  - [rancher_hostname](#rancher_hostname)
  - [rancher_ingress_class_name](#rancher_ingress_class_name)
  - [rancher_ingress_enabled](#rancher_ingress_enabled)
  - [rancher_ingress_tls_source](#rancher_ingress_tls_source)
  - [rancher_lets_encrypt_email](#rancher_lets_encrypt_email)
  - [rancher_lets_encrypt_ingress_class](#rancher_lets_encrypt_ingress_class)
  - [rancher_namespace](#rancher_namespace)
  - [rancher_private_ca](#rancher_private_ca)
  - [rancher_replicas](#rancher_replicas)
  - [rancher_resources](#rancher_resources)
  - [rancher_system_default_registry](#rancher_system_default_registry)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### rancher_additional_helm_values

Additional helm values to be passed to the chart.
These values are merged with the generated values.

**_Type:_** dict<br />

#### Default value

```YAML
rancher_additional_helm_values: {}
```

### rancher_additional_trusted_cas

Set to true to add additional CA certificates via the
tls-ca-additional secret in the cattle-system namespace.

**_Type:_** boolean<br />

#### Default value

```YAML
rancher_additional_trusted_cas: false
```

### rancher_anti_affinity

Pod anti-affinity rule. Options: preferred, required

**_Type:_** string<br />

#### Default value

```YAML
rancher_anti_affinity: preferred
```

### rancher_audit_log_destination

Audit log destination. Options: sidecar, hostpath

**_Type:_** string<br />

#### Default value

```YAML
rancher_audit_log_destination: sidecar
```

### rancher_audit_log_enabled

Enable audit logging

**_Type:_** boolean<br />

#### Default value

```YAML
rancher_audit_log_enabled: false
```

### rancher_audit_log_level

Audit log level (0-3). 0=metadata only, 3=request+response bodies

**_Type:_** integer<br />

#### Default value

```YAML
rancher_audit_log_level: 0
```

### rancher_bootstrap_password

Bootstrap password for the first admin user.
If empty, a random password is generated.

**_Type:_** string<br />

#### Default value

```YAML
rancher_bootstrap_password: ''
```

### rancher_debug

Enable debug mode

**_Type:_** boolean<br />

#### Default value

```YAML
rancher_debug: false
```

### rancher_deployment_name

Deployment name for rancher helm chart

**_Type:_** string<br />

#### Default value

```YAML
rancher_deployment_name: rancher
```

### rancher_enabled

Should rancher helm chart be installed

**_Type:_** boolean<br />

#### Default value

```YAML
rancher_enabled: true
```

### rancher_helm_chart_ref

#### Default value

```YAML
rancher_helm_chart_ref: rancher-stable/rancher
```

### rancher_helm_chart_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
rancher_helm_chart_version: 2.13.3
```

### rancher_helm_repo_name

#### Default value

```YAML
rancher_helm_repo_name: rancher-stable
```

### rancher_helm_repo_url

#### Default value

```YAML
rancher_helm_repo_url: https://releases.rancher.com/server-charts/stable
```

### rancher_hostname

FQDN for the Rancher server. This is required.

**_Type:_** string<br />

#### Default value

```YAML
rancher_hostname: ''
```

#### Example usage

```YAML
  rancher_hostname: "rancher.example.com"
```

### rancher_ingress_class_name

Ingress class name

**_Type:_** string<br />

#### Default value

```YAML
rancher_ingress_class_name: ''
```

### rancher_ingress_enabled

Enable ingress for Rancher

**_Type:_** boolean<br />

#### Default value

```YAML
rancher_ingress_enabled: false
```

### rancher_ingress_tls_source

TLS certificate source for ingress.
Options: rancher (self-signed, requires cert-manager),
letsEncrypt (requires cert-manager),
secret (bring your own certificate)

**_Type:_** string<br />

#### Default value

```YAML
rancher_ingress_tls_source: rancher
```

### rancher_lets_encrypt_email

Email address for Let's Encrypt certificate registration.
Required when rancher_ingress_tls_source is letsEncrypt.

**_Type:_** string<br />

#### Default value

```YAML
rancher_lets_encrypt_email: ''
```

### rancher_lets_encrypt_ingress_class

Ingress class for the Let's Encrypt HTTP01 solver

**_Type:_** string<br />

#### Default value

```YAML
rancher_lets_encrypt_ingress_class: ''
```

### rancher_namespace

K8s namespace to install the rancher chart.
Rancher requires cattle-system namespace.

**_Type:_** string<br />

#### Default value

```YAML
rancher_namespace: cattle-system
```

### rancher_private_ca

Set to true if using certificates signed by a private CA.
Rancher will add the CA certificate to the trust store.

**_Type:_** boolean<br />

#### Default value

```YAML
rancher_private_ca: false
```

### rancher_replicas

Number of Rancher server replicas

**_Type:_** integer<br />

#### Default value

```YAML
rancher_replicas: 3
```

### rancher_resources

Resource requests and limits for Rancher pods

**_Type:_** dict<br />

#### Default value

```YAML
rancher_resources: {}
```

#### Example usage

```YAML
  rancher_resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 1
      memory: 1Gi
```

### rancher_system_default_registry

Private registry for air-gapped installations.
All system images will be pulled from this registry.

**_Type:_** string<br />

#### Default value

```YAML
rancher_system_default_registry: ''
```

## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
