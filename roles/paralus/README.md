# paralus

Install paralus on kubernetes

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [paralus_additional_helm_values](#paralus_additional_helm_values)
  - [paralus_analytics_enabled](#paralus_analytics_enabled)
  - [paralus_audit_logs_storage](#paralus_audit_logs_storage)
  - [paralus_deploy_contour_enabled](#paralus_deploy_contour_enabled)
  - [paralus_deploy_elasticsearch_address](#paralus_deploy_elasticsearch_address)
  - [paralus_deploy_elasticsearch_enabled](#paralus_deploy_elasticsearch_enabled)
  - [paralus_deploy_filebeat_enabled](#paralus_deploy_filebeat_enabled)
  - [paralus_deploy_fluentbit_enabled](#paralus_deploy_fluentbit_enabled)
  - [paralus_deploy_kratos_admin_addr](#paralus_deploy_kratos_admin_addr)
  - [paralus_deploy_kratos_enabled](#paralus_deploy_kratos_enabled)
  - [paralus_deploy_kratos_public_addr](#paralus_deploy_kratos_public_addr)
  - [paralus_deploy_kratos_smtp_connection_uri](#paralus_deploy_kratos_smtp_connection_uri)
  - [paralus_deploy_postgresql_address](#paralus_deploy_postgresql_address)
  - [paralus_deploy_postgresql_database](#paralus_deploy_postgresql_database)
  - [paralus_deploy_postgresql_enabled](#paralus_deploy_postgresql_enabled)
  - [paralus_deploy_postgresql_password](#paralus_deploy_postgresql_password)
  - [paralus_deploy_postgresql_username](#paralus_deploy_postgresql_username)
  - [paralus_deployment_name](#paralus_deployment_name)
  - [paralus_enabled](#paralus_enabled)
  - [paralus_fqdn_core_connector_subdomain](#paralus_fqdn_core_connector_subdomain)
  - [paralus_fqdn_domain](#paralus_fqdn_domain)
  - [paralus_fqdn_hostname](#paralus_fqdn_hostname)
  - [paralus_fqdn_user_subdomain](#paralus_fqdn_user_subdomain)
  - [paralus_helm_chart_ref](#paralus_helm_chart_ref)
  - [paralus_helm_chart_version](#paralus_helm_chart_version)
  - [paralus_helm_repo_name](#paralus_helm_repo_name)
  - [paralus_helm_repo_url](#paralus_helm_repo_url)
  - [paralus_ingress_class_name](#paralus_ingress_class_name)
  - [paralus_ingress_tls](#paralus_ingress_tls)
  - [paralus_init_admin_email](#paralus_init_admin_email)
  - [paralus_init_admin_first_name](#paralus_init_admin_first_name)
  - [paralus_init_admin_last_name](#paralus_init_admin_last_name)
  - [paralus_init_org](#paralus_init_org)
  - [paralus_init_org_desc](#paralus_init_org_desc)
  - [paralus_init_partner](#paralus_init_partner)
  - [paralus_init_partner_desc](#paralus_init_partner_desc)
  - [paralus_init_partner_host](#paralus_init_partner_host)
  - [paralus_namespace](#paralus_namespace)
  - [paralus_wait_install](#paralus_wait_install)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### paralus_additional_helm_values

Additional helm values to be passed to the chart.
These values are merged with the generated values.

**_Type:_** dict<br />

#### Default value

```YAML
paralus_additional_helm_values: {}
```

### paralus_analytics_enabled

Enable analytics collection

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_analytics_enabled: true
```

### paralus_audit_logs_storage

Audit logs storage backend. Options: database, elasticsearch

**_Type:_** string<br />

#### Default value

```YAML
paralus_audit_logs_storage: database
```

### paralus_deploy_contour_enabled

Enable Contour ingress controller deployment.
Set to false if you already have an ingress controller
and configure ingress settings below.

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_deploy_contour_enabled: true
```

### paralus_deploy_elasticsearch_address

External Elasticsearch address. Used when bundled Elasticsearch is disabled.

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_elasticsearch_address: ''
```

### paralus_deploy_elasticsearch_enabled

Enable Elasticsearch deployment for audit logs

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_deploy_elasticsearch_enabled: false
```

### paralus_deploy_filebeat_enabled

Enable Filebeat for log forwarding

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_deploy_filebeat_enabled: false
```

### paralus_deploy_fluentbit_enabled

Enable Fluentbit for log forwarding

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_deploy_fluentbit_enabled: true
```

### paralus_deploy_kratos_admin_addr

External Kratos admin address. Required when bundled Kratos is disabled.

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_kratos_admin_addr: ''
```

### paralus_deploy_kratos_enabled

Enable bundled Kratos identity provider deployment.
Set to false to use an external Kratos instance.

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_deploy_kratos_enabled: true
```

### paralus_deploy_kratos_public_addr

External Kratos public address. Required when bundled Kratos is disabled.

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_kratos_public_addr: ''
```

### paralus_deploy_kratos_smtp_connection_uri

SMTP connection URI for Kratos email sending.
Format: smtps://user:pass@host:port/?skip_ssl_verify=true

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_kratos_smtp_connection_uri: ''
```

### paralus_deploy_postgresql_address

External PostgreSQL address. Required when bundled PostgreSQL is disabled.

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_postgresql_address: ''
```

### paralus_deploy_postgresql_database

External PostgreSQL database name. Required when bundled PostgreSQL is disabled.

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_postgresql_database: ''
```

### paralus_deploy_postgresql_enabled

Enable bundled PostgreSQL deployment.
Set to false to use an external PostgreSQL instance.

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_deploy_postgresql_enabled: true
```

### paralus_deploy_postgresql_password

External PostgreSQL password. Required when bundled PostgreSQL is disabled.

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_postgresql_password: ''
```

### paralus_deploy_postgresql_username

External PostgreSQL username. Required when bundled PostgreSQL is disabled.

**_Type:_** string<br />

#### Default value

```YAML
paralus_deploy_postgresql_username: ''
```

### paralus_deployment_name

Deployment name for paralus helm chart

**_Type:_** string<br />

#### Default value

```YAML
paralus_deployment_name: paralus
```

### paralus_enabled

Should paralus helm chart be installed

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_enabled: true
```

### paralus_fqdn_core_connector_subdomain

Subdomain for core connector relay

**_Type:_** string<br />

#### Default value

```YAML
paralus_fqdn_core_connector_subdomain: '*.core-connector'
```

### paralus_fqdn_domain

Domain for the Paralus console. This is required.

**_Type:_** string<br />

#### Default value

```YAML
paralus_fqdn_domain: paralus.local
```

#### Example usage

```YAML
  paralus_fqdn_domain: "example.com"
```

### paralus_fqdn_hostname

Hostname prefix for the Paralus console.
The console will be accessible at <hostname>.<domain>

**_Type:_** string<br />

#### Default value

```YAML
paralus_fqdn_hostname: console
```

### paralus_fqdn_user_subdomain

Subdomain for user-facing relay

**_Type:_** string<br />

#### Default value

```YAML
paralus_fqdn_user_subdomain: '*.user'
```

### paralus_helm_chart_ref

#### Default value

```YAML
paralus_helm_chart_ref: '{{ paralus_helm_repo_name }}/ztka'
```

### paralus_helm_chart_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
paralus_helm_chart_version: 0.3.1
```

### paralus_helm_repo_name

#### Default value

```YAML
paralus_helm_repo_name: paralus
```

### paralus_helm_repo_url

#### Default value

```YAML
paralus_helm_repo_url: https://paralus.github.io/helm-charts
```

### paralus_ingress_class_name

Ingress class name to use (e.g. traefik, nginx)

**_Type:_** string<br />

#### Default value

```YAML
paralus_ingress_class_name: ''
```

### paralus_ingress_tls

Enable TLS on the ingress (determines https vs http scheme)

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_ingress_tls: true
```

### paralus_init_admin_email

Admin email address for initial Paralus setup. This is required.

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_admin_email: admin@paralus.local
```

#### Example usage

```YAML
  paralus_init_admin_email: "admin@example.com"
```

### paralus_init_admin_first_name

Admin first name for initial Paralus setup

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_admin_first_name: Admin
```

### paralus_init_admin_last_name

Admin last name for initial Paralus setup

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_admin_last_name: User
```

### paralus_init_org

Organization name for initial Paralus setup

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_org: ParalusOrg
```

### paralus_init_org_desc

Organization description for initial Paralus setup

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_org_desc: Default Organization
```

### paralus_init_partner

Partner name for initial Paralus setup

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_partner: Paralus
```

### paralus_init_partner_desc

Partner description for initial Paralus setup

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_partner_desc: Default Partner
```

### paralus_init_partner_host

Partner host for initial Paralus setup.
Defaults to the FQDN domain if empty.

**_Type:_** string<br />

#### Default value

```YAML
paralus_init_partner_host: ''
```

### paralus_namespace

K8s namespace to install the paralus chart

**_Type:_** string<br />

#### Default value

```YAML
paralus_namespace: paralus
```

### paralus_wait_install

Wait for paralus helm chart installation

**_Type:_** boolean<br />

#### Default value

```YAML
paralus_wait_install: true
```

## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
