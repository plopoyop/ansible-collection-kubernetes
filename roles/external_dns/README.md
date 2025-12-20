# external_dns

Install and configure External-DNS on kubernetes

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [external_dns_additional_helm_values](#external_dns_additional_helm_values)
  - [external_dns_deployment_name](#external_dns_deployment_name)
  - [external_dns_domain_filters](#external_dns_domain_filters)
  - [external_dns_enabled](#external_dns_enabled)
  - [external_dns_env](#external_dns_env)
  - [external_dns_exclude_domains](#external_dns_exclude_domains)
  - [external_dns_extra_args](#external_dns_extra_args)
  - [external_dns_helm_chart_ref](#external_dns_helm_chart_ref)
  - [external_dns_helm_chart_version](#external_dns_helm_chart_version)
  - [external_dns_helm_repo_name](#external_dns_helm_repo_name)
  - [external_dns_helm_repo_url](#external_dns_helm_repo_url)
  - [external_dns_helm_values](#external_dns_helm_values)
  - [external_dns_namespace](#external_dns_namespace)
  - [external_dns_policy](#external_dns_policy)
  - [external_dns_provider_name](#external_dns_provider_name)
  - [external_dns_rbac_create](#external_dns_rbac_create)
  - [external_dns_registry](#external_dns_registry)
  - [external_dns_resources](#external_dns_resources)
  - [external_dns_service_account_create](#external_dns_service_account_create)
  - [external_dns_service_account_name](#external_dns_service_account_name)
  - [external_dns_sources](#external_dns_sources)
  - [external_dns_txt_owner_id](#external_dns_txt_owner_id)
  - [external_dns_txt_prefix](#external_dns_txt_prefix)
  - [external_dns_txt_suffix](#external_dns_txt_suffix)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### external_dns_additional_helm_values

#### Default value

```YAML
external_dns_additional_helm_values: {}
```

### external_dns_deployment_name

Deployment name for external-dns helm chart

**_Type:_** string<br />

#### Default value

```YAML
external_dns_deployment_name: external-dns
```

### external_dns_domain_filters

Limit possible target zones by domain suffixes

**_Type:_** list<br />

#### Default value

```YAML
external_dns_domain_filters: []
```

### external_dns_enabled

Should external-dns helm chart be installed

**_Type:_** boolean<br />

#### Default value

```YAML
external_dns_enabled: true
```

### external_dns_env

Environment variables for the external-dns helm chart

**_Type:_** dict<br />

#### Default value

```YAML
external_dns_env: {}
```

### external_dns_exclude_domains

Intentionally exclude domains from being managed

**_Type:_** list<br />

#### Default value

```YAML
external_dns_exclude_domains: []
```

### external_dns_extra_args

Extra arguments to provide to ExternalDNS

**_Type:_** dict<br />

#### Default value

```YAML
external_dns_extra_args: {}
```

### external_dns_helm_chart_ref

#### Default value

```YAML
external_dns_helm_chart_ref: '{{ external_dns_helm_repo_name }}/external-dns'
```

### external_dns_helm_chart_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
external_dns_helm_chart_version: 1.19.0
```

### external_dns_helm_repo_name

#### Default value

```YAML
external_dns_helm_repo_name: external-dns
```

### external_dns_helm_repo_url

#### Default value

```YAML
external_dns_helm_repo_url: https://kubernetes-sigs.github.io/external-dns/
```

### external_dns_helm_values

Additional helm values to override defaults

**_Type:_** dict<br />

### external_dns_namespace

K8s namespace to install the external-dns chart

**_Type:_** string<br />

#### Default value

```YAML
external_dns_namespace: external-dns
```

### external_dns_policy

Policy for the external-dns helm chart

**_Type:_** string<br />

#### Default value

```YAML
external_dns_policy: upsert-only
```

### external_dns_provider_name

Provider name (e.g., aws, cloudflare, azure, etc.)

**_Type:_** string<br />

#### Default value

```YAML
external_dns_provider_name: ''
```

### external_dns_rbac_create

If true, create a ClusterRole & ClusterRoleBinding with access to the Kubernetes API

**_Type:_** boolean<br />

#### Default value

```YAML
external_dns_rbac_create: true
```

### external_dns_registry

Specify the registry for storing ownership and labels (txt, aws-sd, dynamodb, noop)

**_Type:_** string<br />

#### Default value

```YAML
external_dns_registry: txt
```

### external_dns_resources

Resources for the external-dns container

**_Type:_** dict<br />

#### Default value

```YAML
external_dns_resources: {}
```

### external_dns_service_account_create

If true, create a new ServiceAccount

**_Type:_** boolean<br />

#### Default value

```YAML
external_dns_service_account_create: true
```

### external_dns_service_account_name

ServiceAccount name

**_Type:_** string<br />

#### Default value

```YAML
external_dns_service_account_name: ''
```

### external_dns_sources

Kubernetes resources to monitor for DNS entries

**_Type:_** list<br />

#### Default value

```YAML
external_dns_sources:
  - service
  - ingress
```

### external_dns_txt_owner_id

Specify an identifier for this instance of ExternalDNS when using a registry other than noop

**_Type:_** string<br />

#### Default value

```YAML
external_dns_txt_owner_id: ''
```

### external_dns_txt_prefix

Specify a prefix for the domain names of TXT records created for the txt registry

**_Type:_** string<br />

#### Default value

```YAML
external_dns_txt_prefix: ''
```

### external_dns_txt_suffix

Specify a suffix for the domain names of TXT records created for the txt registry

**_Type:_** string<br />

#### Default value

```YAML
external_dns_txt_suffix: ''
```

## Dependencies

None.

## License

MPL2

## Author

Clément Hubert
