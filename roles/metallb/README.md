# metallb

Install Metal LB controller on kubernetes

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [metallb_create_additionnal_values](#metallb_create_additionnal_values)
  - [metallb_enabled](#metallb_enabled)
  - [metallb_helm_version](#metallb_helm_version)
  - [metallb_ip_pools](#metallb_ip_pools)
  - [metallb_namespace](#metallb_namespace)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`


## Default Variables

### metallb_create_additionnal_values

additionnal values to pass to helm chart. Will be rendered as is

#### Default value

```YAML
metallb_create_additionnal_values: {}
```

#### Example usage

```YAML
metallb_create_additionnal_values:
  prometheus:
    scrapeAnnotations: true
```

### metallb_enabled

Should metallb helm chart be installed

#### Default value

```YAML
metallb_enabled: true
```

### metallb_helm_version

Helm chart version to install

#### Default value

```YAML
metallb_helm_version: 0.15.2
```

### metallb_ip_pools

IP pool to create

#### Default value

```YAML
metallb_ip_pools: {}
```

#### Example usage

```YAML
 metallb_ip_pools:
 - name: "default-ip-pool"
   protocol: "layer2"
   addresses: "192.168.50.8-192.168.50.12"
   state: "present"
   pool_options:
     avoidBuggyIPs: true
     serviceAllocation:
     priority: 50
   interfaces: ["eth0", "eth1"]
 - name: "bgp-ip-pool"
   protocol: "bgp"
   addresses: "198.51.100.10/24"
   bgp_peer_options:
     myASN: 64500
     peerASN: 64501
     peerAddress: "10.0.0.1"
     peerPort: 180
   bfd_profile_options:
     receiveInterval: 380
     transmitInterval: 270
   frr_configuration_options:
       bgp:
         routers:
         - asn: 64512
           neighbors:
             - address: 172.30.0.3
               asn: 64512
               toReceive:
                 allowed:
                 mode: all
   community_configuration_options:
     communities:
       - name: "vpn-only"
         value: 74041
       - name: "NO_ADVERTISE"
         value: "65535:65282"
```

### metallb_namespace

K8s namespace to install the metallb chart

#### Default value

```YAML
metallb_namespace: metallb-system
```



## Dependencies

None.

## License

MLP2

## Author

Clément Hubert
