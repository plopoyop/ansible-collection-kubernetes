# traefik

Install traefik ingress controller on kubernetes

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [traefik_deployments](#traefik_deployments)
  - [traefik_helm_version](#traefik_helm_version)
  - [traefik_ingress_enabled](#traefik_ingress_enabled)
  - [traefik_namespace](#traefik_namespace)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`


## Default Variables

### traefik_deployments

List of ingress controlers to deploy

#### Default value

```YAML
traefik_deployments:
  - name: traefik
    state: present
    helm_values:
      deployment_kind: DaemonSet
      service_type: LoadBalancer
      traefik_entrypoint_port: 9000
      traefik_entrypoint_expose: 'false'
      websecure_entrypoint_port: 8443
      websecure_entrypoint_exposed_port: 443
      websecure_entrypoint_expose: 'true'
      web_entrypoint_port: 8000
      web_entrypoint_exposed_port: 80
      web_entrypoint_expose: 'true'
      traefik_additionnal_entrypoint: []
      traefik_ingress_enabled: 'true'
      traefik_gateway_enabled: 'false'
      dashboard_enabled: false
      additionnal_values: {}
```

#### Example usage

```YAML
 traefik_deployments:
   - name: traefik
     state: present
     helm_values:
       deployment_kind: "DaemonSet"
       service_type: "LoadBalancer"
       traefik_entrypoint_port: 9000
       traefik_entrypoint_expose: "false"
       websecure_entrypoint_port: 8443
       websecure_entrypoint_exposed_port: 443
       websecure_entrypoint_expose: "true"
       web_entrypoint_port: 8000
       web_entrypoint_exposed_port: 80
       web_entrypoint_expose: "true"
       traefik_additionnal_entrypoint:
         - name: "example"
           port: 8001
           exposed_port: 81
           expose: true
       traefik_ingress_enabled: "true"
       traefik_gateway_enabled: "false"
       dashboard_enabled: false
       additionnal_values:
         healthcheck:
           enabled: "true"
```

### traefik_helm_version

Helm chart version to install

#### Default value

```YAML
traefik_helm_version: v35.3.0
```

### traefik_ingress_enabled

Should traefik helm chart be installed

#### Default value

```YAML
traefik_ingress_enabled: true
```

### traefik_namespace

K8s namespace to install the traefik ingress chart

#### Default value

```YAML
traefik_namespace: ingress-traefik-controller
```



## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
