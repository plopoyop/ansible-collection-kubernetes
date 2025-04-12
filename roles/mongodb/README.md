# mongodb

Role to install mongodb on kubernetes cluster.
It install community operator via its helm chart and deploy mongodb replicatset.

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [mongodb_crd_helm_version](#mongodb_crd_helm_version)
  - [mongodb_default_instance](#mongodb_default_instance)
  - [mongodb_instance_members](#mongodb_instance_members)
  - [mongodb_instance_name](#mongodb_instance_name)
  - [mongodb_instance_namespace](#mongodb_instance_namespace)
  - [mongodb_instance_values_override](#mongodb_instance_values_override)
  - [mongodb_instance_version](#mongodb_instance_version)
  - [mongodb_operator_cpu_limit](#mongodb_operator_cpu_limit)
  - [mongodb_operator_cpu_request](#mongodb_operator_cpu_request)
  - [mongodb_operator_deployment_name](#mongodb_operator_deployment_name)
  - [mongodb_operator_extra_envs](#mongodb_operator_extra_envs)
  - [mongodb_operator_helm_version](#mongodb_operator_helm_version)
  - [mongodb_operator_memory_limit](#mongodb_operator_memory_limit)
  - [mongodb_operator_memory_request](#mongodb_operator_memory_request)
  - [mongodb_operator_namespace](#mongodb_operator_namespace)
  - [mongodb_operator_pod_security_context](#mongodb_operator_pod_security_context)
  - [mongodb_operator_priority_class](#mongodb_operator_priority_class)
  - [mongodb_operator_replicas](#mongodb_operator_replicas)
  - [mongodb_operator_security_context](#mongodb_operator_security_context)
  - [mongodb_operator_watch_namespace](#mongodb_operator_watch_namespace)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`


## Default Variables

### mongodb_crd_helm_version

mongodb instance helm chart version

#### Default value

```YAML
mongodb_crd_helm_version: 0.1.0
```

### mongodb_default_instance

Overrides for default values

#### Default value

```YAML
mongodb_default_instance:
  name: '{{ mongodb_instance_name }}'
  namespace: '{{ mongodb_instance_namespace }}'
  version: '{{ mongodb_instance_version }}'
  feature_compatibility_version: "{{ (mongodb_instance_version | ansible.builtin.split('.'))[0]
    }}.{{ (mongodb_instance_version | ansible.builtin.split('.'))[1] }}"
  members: '{{ mongodb_instance_members }}'
  persistent: true
  create_service_account: false
  admin_password: '{{ mongodb_instance_admin_password }}'
  additional_connection_string_config: {}
  additional_mongod_config: {}
  container_additional_config: {}
  backup_enabled: false
  backup_cronjob_schedule: '*/20 * * * *'
  backup_cronjob_timezone: Europe/Paris
  backup_cronjob_command: []
  backup_cronjob_container_env: []
  backup_cronjob_container_secret_env: []
  backup_cronjob_image: {}
  backup_cronjob_image_pull_secret: {}
  backup_additionnal_config: {}
  metrics_enabled: false
  metrics_username: prometheus
  metrics_password: ''
```

### mongodb_instance_members

number of replicatset members

#### Default value

```YAML
mongodb_instance_members: 3
```

### mongodb_instance_name

mongodb instance name

#### Default value

```YAML
mongodb_instance_name: mongodb-database
```

### mongodb_instance_namespace

K8s namespace to install deploy mongodb instance

#### Default value

```YAML
mongodb_instance_namespace: mongodb
```

### mongodb_instance_values_override

#### Default value

```YAML
mongodb_instance_values_override: {}
```

#### Example usage

```YAML
 mongodb_instance_values_override:
   create_service_account: true
   additional_connection_string_config:
     authenticationMechanism: "scram-sha256"
     authSource: "admin"
   metrics_enabled: true
   metrics_username: "monitoring"
   metrics_password: "metricspassword"
```

### mongodb_instance_version

mongodb version

#### Default value

```YAML
mongodb_instance_version: 8.0.6
```

### mongodb_operator_cpu_limit

CPU limit for operator pod

#### Default value

```YAML
mongodb_operator_cpu_limit: 1100m
```

### mongodb_operator_cpu_request

CPU request for operator pod

#### Default value

```YAML
mongodb_operator_cpu_request: 500m
```

### mongodb_operator_deployment_name

Deployment name for mongodb community operator chart

#### Default value

```YAML
mongodb_operator_deployment_name: mongodb-operator
```

### mongodb_operator_extra_envs

Additional environment variables

#### Default value

```YAML
mongodb_operator_extra_envs: []
```

#### Example usage

```YAML
 mongodb_operator_extra_envs:
  - name: CLUSTER_DOMAIN
    value: my-cluster.domain
```

### mongodb_operator_helm_version

Helm chart version to install

#### Default value

```YAML
mongodb_operator_helm_version: 0.13.0
```

### mongodb_operator_memory_limit

Memory limit for operator pod

#### Default value

```YAML
mongodb_operator_memory_limit: 1Gi
```

### mongodb_operator_memory_request

Memory request for operator pod

#### Default value

```YAML
mongodb_operator_memory_request: 200Mi
```

### mongodb_operator_namespace

K8s namespace to install the mongodb community operator chart

#### Default value

```YAML
mongodb_operator_namespace: mongodb
```

### mongodb_operator_pod_security_context

security context for operator pod

#### Default value

```YAML
mongodb_operator_pod_security_context:
  runAsNonRoot: true
  runAsUser: 2000
```

### mongodb_operator_priority_class

PriorityClass configuration for operator
ref: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#priorityclass

#### Default value

```YAML
mongodb_operator_priority_class: ''
```

### mongodb_operator_replicas

Number of replicat for mongodb operator

#### Default value

```YAML
mongodb_operator_replicas: 1
```

### mongodb_operator_security_context

security context for operator

#### Default value

```YAML
mongodb_operator_security_context: {}
```

### mongodb_operator_watch_namespace

To configure the Operator to watch resources in another namespace

#### Default value

```YAML
mongodb_operator_watch_namespace: "{{ (mongodb_instance_namespace == mongodb_operator_namespace)
  | ternary(mongodb_instance_namespace, '*') }}"
```

#### Example usage

```YAML
 mongodb_operator_watch_namespace: "*"
```



## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
