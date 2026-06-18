# traefik

Install traefik ingress controller on kubernetes

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [traefik_crds_upgrade_enabled](#traefik_crds_upgrade_enabled)
  - [traefik_deployments](#traefik_deployments)
  - [traefik_gateway_api_channel](#traefik_gateway_api_channel)
  - [traefik_gateway_api_crds_install](#traefik_gateway_api_crds_install)
  - [traefik_gateway_api_version](#traefik_gateway_api_version)
  - [traefik_helm_version](#traefik_helm_version)
  - [traefik_ingress_enabled](#traefik_ingress_enabled)
  - [traefik_middlewares](#traefik_middlewares)
  - [traefik_middlewares_tcp](#traefik_middlewares_tcp)
  - [traefik_namespace](#traefik_namespace)
- [Discovered Tags](#discovered-tags)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.17`

## Default Variables

### traefik_crds_upgrade_enabled

Apply Traefik CRDs (server-side, force conflicts) before helm upgrade.
Helm does not update CRDs automatically (HIP-0011), so we render the
target chart with `helm_template --include-crds` and apply only the
CustomResourceDefinition resources. Skipped on first install since
`helm install` already applies CRDs from the chart's `crds/` directory,
and skipped when the installed chart version already matches the target.

**_Type:_** boolean<br />

#### Default value

```YAML
traefik_crds_upgrade_enabled: true
```

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
      gateway_experimental_channel: false
      gateway_namespaces: []
      gateway_cross_provider_namespaces: []
      gateway_label_selector: ''
      gateway: {}
      gateway_class: {}
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
       traefik_gateway_enabled: true
       gateway_experimental_channel: false
       gateway_namespaces: []
       gateway_cross_provider_namespaces: []
       gateway_label_selector: ""
       gateway:
         enabled: true
         name: "traefik-gateway"
         namespace: ""
         annotations: {}
         infrastructure: {}
         defaultScope: ""
         listeners:
           web:
             port: 8000
             protocol: "HTTP"
             namespacePolicy:
               from: "All"
       gateway_class:
         enabled: true
         name: "traefik"
         labels: {}
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

### traefik_gateway_api_channel

Release channel of the Gateway API CRDs to install: `standard` (GA
resources only) or `experimental` (adds `TCPRoute`/`TLSRoute`, required
when a deployment sets `gateway_experimental_channel: true`).

**_Type:_** string<br />

#### Default value

```YAML
traefik_gateway_api_channel: standard
```

### traefik_gateway_api_crds_install

Install the upstream Kubernetes Gateway API CRDs (`gateway.networking.k8s.io`)
before deploying Traefik. The Traefik helm chart deploys the `Gateway` and
`GatewayClass` resources but does NOT bundle the Gateway API CRDs themselves,
so they must already exist in the cluster when `providers.kubernetesGateway`
is enabled on a deployment. Leave this disabled when the CRDs are managed
elsewhere (another controller, a GitOps pipeline, etc.).

**_Type:_** boolean<br />

#### Default value

```YAML
traefik_gateway_api_crds_install: false
```

### traefik_gateway_api_version

Version (git tag) of the Kubernetes Gateway API CRDs to install when
`traefik_gateway_api_crds_install` is enabled.

**_Type:_** string<br />

#### Default value

```YAML
traefik_gateway_api_version: v1.5.1
```

### traefik_helm_version

Helm chart version to install

**_Type:_** string<br />

#### Default value

```YAML
traefik_helm_version: v41.0.0
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

## Discovered Tags

**_crds_**

**_helm_chart_**

**_helm_repository_**

**_install_**

**_manifest_**

**_namespace_**

**_traefik_**

**_uninstall_**

## Dependencies

None.

## License

MPL-2.0

## Author

Clément Hubert
