# traefik

Install traefik ingress controller on kubernetes

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [traefik_deployments](#traefik_deployments)
  - [traefik_helm_chart_ref](#traefik_helm_chart_ref)
  - [traefik_helm_repo_name](#traefik_helm_repo_name)
  - [traefik_helm_repo_url](#traefik_helm_repo_url)
  - [traefik_helm_version](#traefik_helm_version)
  - [traefik_ingress_enabled](#traefik_ingress_enabled)
  - [traefik_middlewares](#traefik_middlewares)
  - [traefik_middlewares_tcp](#traefik_middlewares_tcp)
  - [traefik_namespace](#traefik_namespace)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### traefik_deployments

List of ingress controllers to deploy

**_Type:_** list of dict<br />

#### Default value

```YAML
traefik_deployments:
  - name: traefik
    state: present
    helm_values:
      deployment_kind: DaemonSet
      service_type: LoadBalancer
      traefik_entrypoint_port: 9000
      traefik_entrypoint_expose: false
      websecure_entrypoint_port: 8443
      websecure_entrypoint_exposed_port: 443
      websecure_entrypoint_expose: true
      web_entrypoint_port: 8000
      web_entrypoint_exposed_port: 80
      web_entrypoint_expose: true
      traefik_additional_entrypoint: []
      traefik_ingress_enabled: true
      traefik_gateway_enabled: false
      dashboard_enabled: false
      additional_values: {}
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
       traefik_entrypoint_expose: false
       websecure_entrypoint_port: 8443
       websecure_entrypoint_exposed_port: 443
       websecure_entrypoint_expose: true
       web_entrypoint_port: 8000
       web_entrypoint_exposed_port: 80
       web_entrypoint_expose: true
       traefik_additional_entrypoint:
         - name: "example"
           port: 8001
           exposed_port: 81
           expose: true
       traefik_ingress_enabled: true
       traefik_gateway_enabled: false
       dashboard_enabled: false
       additional_values:
         healthcheck:
           enabled: true
```

### traefik_helm_chart_ref

#### Default value

```YAML
traefik_helm_chart_ref: traefik/traefik
```

### traefik_helm_repo_name

#### Default value

```YAML
traefik_helm_repo_name: traefik
```

### traefik_helm_repo_url

#### Default value

```YAML
traefik_helm_repo_url: https://traefik.github.io/charts
```

### traefik_helm_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
traefik_helm_version: v38.0.1
```

### traefik_ingress_enabled

Should traefik helm chart be installed

**_Type:_** boolean<br />

#### Default value

```YAML
traefik_ingress_enabled: true
```

### traefik_middlewares

List of traefik middlewares to create

**_Type:_** list of dict<br />

#### Default value

```YAML
traefik_middlewares: []
```

#### Example usage

```YAML
 traefik_middlewares:
 - name: redirect-to-https
   spec:
     redirectRegex:
       regex: "^http://(.*)"
       replacement: "https://$1"
       permanent: true
 - name: older-middleware
   state: absent
```

### traefik_middlewares_tcp

List of traefik TCP middlewares to create

**_Type:_** list of dict<br />

#### Default value

```YAML
traefik_middlewares_tcp: []
```

#### Example usage

```YAML
 traefik_middlewares_tcp:
 - name: test-inflightconn
   spec:
     inFlightConn:
       amount: 10
 - name: older-middleware
   state: absent
```

### traefik_namespace

K8s namespace to install the traefik ingress chart

**_Type:_** string<br />

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
