# cert_manager

Install cert-manager

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [cert_manager_acme_production_contact_email](#cert_manager_acme_production_contact_email)
  - [cert_manager_acme_production_enabled](#cert_manager_acme_production_enabled)
  - [cert_manager_acme_production_ingress_class](#cert_manager_acme_production_ingress_class)
  - [cert_manager_acme_production_private_key_ref](#cert_manager_acme_production_private_key_ref)
  - [cert_manager_acme_production_solver](#cert_manager_acme_production_solver)
  - [cert_manager_acme_production_url](#cert_manager_acme_production_url)
  - [cert_manager_acme_staging_contact_email](#cert_manager_acme_staging_contact_email)
  - [cert_manager_acme_staging_enabled](#cert_manager_acme_staging_enabled)
  - [cert_manager_acme_staging_ingress_class](#cert_manager_acme_staging_ingress_class)
  - [cert_manager_acme_staging_private_key_ref](#cert_manager_acme_staging_private_key_ref)
  - [cert_manager_acme_staging_solver](#cert_manager_acme_staging_solver)
  - [cert_manager_acme_staging_url](#cert_manager_acme_staging_url)
  - [cert_manager_deployment_name](#cert_manager_deployment_name)
  - [cert_manager_enabled](#cert_manager_enabled)
  - [cert_manager_helm_chart_version](#cert_manager_helm_chart_version)
  - [cert_manager_namespace](#cert_manager_namespace)
  - [cert_manager_self_signed_enabled](#cert_manager_self_signed_enabled)
  - [cert_manager_trust_manager_deployment_name](#cert_manager_trust_manager_deployment_name)
  - [cert_manager_trust_manager_enabled](#cert_manager_trust_manager_enabled)
  - [cert_manager_trust_manager_helm_chart_ref](#cert_manager_trust_manager_helm_chart_ref)
- [Open Tasks](#open-tasks)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`


## Default Variables

### cert_manager_acme_production_contact_email

Contact Email for ACME production account

#### Default value

```YAML
cert_manager_acme_production_contact_email: ''
```

### cert_manager_acme_production_enabled

#### Default value

```YAML
cert_manager_acme_production_enabled: true
```

### cert_manager_acme_production_ingress_class

Ingress Class for ACME Production HTTP solver

#### Default value

```YAML
cert_manager_acme_production_ingress_class: traefik
```

### cert_manager_acme_production_private_key_ref

Private key secret ref for ACME Production

#### Default value

```YAML
cert_manager_acme_production_private_key_ref: letsencrypt-prod
```

### cert_manager_acme_production_solver

Solver for ACME Production

#### Default value

```YAML
cert_manager_acme_production_solver:
  - selector: {}
    http01:
      ingress:
        ingressClassName: '{{ cert_manager_acme_production_ingress_class }}'
```

### cert_manager_acme_production_url

ACME Staging url

#### Default value

```YAML
cert_manager_acme_production_url: https://acme-v02.api.letsencrypt.org/directory
```

### cert_manager_acme_staging_contact_email

#### Default value

```YAML
cert_manager_acme_staging_contact_email: ''
```

### cert_manager_acme_staging_enabled

Should ACME staging ClusterIssuer be enabled

#### Default value

```YAML
cert_manager_acme_staging_enabled: true
```

### cert_manager_acme_staging_ingress_class

Ingress Class for ACME Staging HTTP solver

#### Default value

```YAML
cert_manager_acme_staging_ingress_class: traefik
```

### cert_manager_acme_staging_private_key_ref

Private key secret ref for ACME Staging

#### Default value

```YAML
cert_manager_acme_staging_private_key_ref: letsencrypt-staging
```

### cert_manager_acme_staging_solver

Solver for ACME Staging

#### Default value

```YAML
cert_manager_acme_staging_solver:
  - selector: {}
    http01:
      ingress:
        ingressClassName: '{{ cert_manager_acme_staging_ingress_class }}'
```

### cert_manager_acme_staging_url

#### Default value

```YAML
cert_manager_acme_staging_url: https://acme-staging-v02.api.letsencrypt.org/directory
```

### cert_manager_deployment_name

Deployment name for cert-manager helm chart

#### Default value

```YAML
cert_manager_deployment_name: cert-manager
```

### cert_manager_enabled

Should cert-manager helm chart be installed

#### Default value

```YAML
cert_manager_enabled: true
```

### cert_manager_helm_chart_version

Helm chart version to install

#### Default value

```YAML
cert_manager_helm_chart_version: 1.17.1
```

### cert_manager_namespace

K8s namespace to install the cert-manager chart

#### Default value

```YAML
cert_manager_namespace: cert-manager
```

### cert_manager_self_signed_enabled

Should ACME production ClusterIssuer be enabled

#### Default value

```YAML
cert_manager_self_signed_enabled: true
```

### cert_manager_trust_manager_deployment_name

Deployment name for cert-manager trust manager helm chart

#### Default value

```YAML
cert_manager_trust_manager_deployment_name: cert-manager-trust
```

### cert_manager_trust_manager_enabled

Should cert-manager trust manager helm chart be installed

#### Default value

```YAML
cert_manager_trust_manager_enabled: false
```

### cert_manager_trust_manager_helm_chart_ref

Trust manager Helm chart version to install

#### Default value

```YAML
cert_manager_trust_manager_helm_chart_ref: 0.16.0
```


## Open Tasks

- (improvement): Allow multiple times deployment of the same ClusterIssuer with differents names and solvers

## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
