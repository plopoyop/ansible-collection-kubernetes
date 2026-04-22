# traefik

Install traefik ingress controller on kubernetes

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [traefik_deployments](#traefik_deployments)
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
      access_logs: {}
      plugins: []
      service_annotations: {}
      service_labels: {}
      service_spec: {}
      proxy_protocol_trusted_ips: []
      forwarded_headers_trusted_ips: []
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
       access_logs:
         enabled: true
         format: "json"
       plugins:
         - name: "bouncer"
           moduleName: "github.com/maxlerebourg/crowdsec-bouncer-traefik-plugin"
           version: "v1.4.3"
       service_annotations:
         service.beta.kubernetes.io/ovh-loadbalancer-proxy-protocol: "v2"
       service_labels: {}
       service_spec:
         externalTrafficPolicy: "Local"
         loadBalancerIP: "1.2.3.4"
       # Trust PROXY protocol v1/v2 on the web+websecure entrypoints.
       # Required when the upstream LB forwards the client IP via the
       # PROXY header. List the LB egress IPs / CIDRs.
       proxy_protocol_trusted_ips:
         - "10.20.0.0./24"
       # Trust forwarded HTTP headers (X-Forwarded-*) on the same
       # entrypoints. Useful when behind an L7 proxy or CDN.
       forwarded_headers_trusted_ips: []
       additional_values:
         commonLabels:
           team: "platform"
```

### traefik_helm_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
traefik_helm_version: v39.0.8
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
