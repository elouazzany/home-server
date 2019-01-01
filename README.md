
# Server Provisioning

This project contains the playbook to provision my home servers.

It creates a Kubernetes cluster on self hosted bare metal hosts and deploy apps.

It also contains a Vagrant environment to test the playbooks and services.

TODO selfhosted

## Hosts

The underlying hardware is detailed on a [dedicated page](docs/Hardware_detail.md), but to keep it short : 

| Type      | Cores | CPU Model                                                                                                          |  RAM  | Storage   |
| --------- | :---: | ------------------------------------------------------------------------------------------------------------------ | :---: | --------- |
| Master    |  2/4  | [Intel i3 3217U](https://ark.intel.com/products/65697/Intel-Core-i3-3217U-Processor-3M-Cache-1-80-GHz-)            |  8G   | SSD 64G   |
| Node_1    |  2/4  | [Intel i5 6260U](https://ark.intel.com/products/91160/Intel-Core-i5-6260U-Processor-4M-Cache-up-to-2-90-GHz-)      |  32G  | SSD 500G  |
| Node_Home |  4/4  | [Intel Atom x5 Z8350](https://ark.intel.com/products/93361/Intel-Atom-x5-Z8350-Processor-2M-Cache-up-to-1-92-GHz-) |  2G   | Flash 32G |

## Vagrant

The Vagrantfile creates 3 *similar* guests : 

| Type      | Cores |  RAM  |
| --------- | :---: | :---: |
| Master    |   2   |  4G   |
| Node_1    |   4   |  8G   |
| Node_Home |   2   |  2G   |

These settings are configured in `Vagrantconfig.yaml`, feel free to change them or add mode nodes.

## Vagrant

To test the deployed services, you will have to add the following domains to your hosts file : 

```
192.168.100.10 k8stest.com 
192.168.100.10 infra.k8stest.com
192.168.100.10 home.k8stest.com
192.168.100.10 web.k8stest.com
192.168.100.10 dev.k8stest.com
192.168.100.10 streams.k8stest.com
192.168.100.10 plex.k8stest.com
192.168.100.10 dl.k8stest.com
```

### User

To avoid using `root` directly, a standard user is created. For the Vagrant environment, it's simply named `user`.

This `user` can 
  - `sudo` without password
  - SSH to other machines without password (using RSA keys)
  - use kubectl

### HTTPS

All HTTPS certificates are self-signed, so you'll need to accept a warning the first time you access a domain.

The playbook supports [Let's Encrypt](https://letsencrypt.org/) to generate valid certificates on a production environment.

### Credentials

Unless listed, all credentials are `user` / `Passw0rd`.

## Services

The folowing front-facing services are deployed : 

| Service                                                          | Test URL                                | Description                                   |
| ---------------------------------------------------------------- | --------------------------------------- | --------------------------------------------- |
| [Kubernetes dashboard](https://github.com/kubernetes/dashboard/) | https://infra.k8stest.com/kube          | Kubernetes dashboard                          |
| [Unifi Controller](https://unifi-sdn.ubnt.com/)                  | https://infra.k8stest.com/unifi         | Controller for Unifi devices                  |
| [HomeAssistant](https://www.home-assistant.io/)                  | https://home.k8stest.com/homeassistant/ | Home automation                               |
| [Node-RED](https://nodered.org/)                                 | https://home.k8stest.com/node-red/      | Flow-based programming for the IoT            |
| [TT-RSS](https://tt-rss.org/)                                    | https://web.k8stest.com/tt-rss/         | News feed (RSS/Atom) reader and aggregator    |
| [Gitlab](https://about.gitlab.com/)                              | https://dev.k8stest.com/gitlab/         | Source code management and CI/CD              |
| [Plex](https://www.plex.tv/)                                     | https://plex.k8stest.com/               | Video streaming                               |
| [Airsonic](https://airsonic.github.io/)                          | https://streams.k8stest.com/airsonic/   | Music streaming                               |
| [Sickchill](https://sickchill.github.io/)                        | https://dl.k8stest.com/sickchill/       | Automatic Video Library Manager for TV Shows. |
| [Deluge](https://deluge-torrent.org/)                            | https://dl.k8stest.com/deluge/          | Torrent client                                |
| [Pyload](https://pyload.net/)                                    | https://dl.k8stest.com/pyload/          | HTTP download manager                         |
| [SABnzbd](https://sabnzbd.org/)                                  | https://dl.k8stest.com/sabnzbd/         | Binary newsreader                             |


### Kubernetes dashboard

An `admin-user` service account is automatically created by the playbook.

To login, you need to fetch the associated token.

You can do so using a terminal (assuming you start at the project root) : 
```shell
[your_account@your_computer$] cd vagrant
[your_account@your_computer$] vagrant ssh master
[vagrant@master$] sudo su - user
[user@master$] kubectl --namespace=kube-system describe secrets $(kubectl --namespace=kube-system get secrets | awk '/admin-user-token/ { print $1 }')
```

### Unifi Controller

### HomeAssistant

### Node-RED

### TT-RSS

### Gitlab

### Plex

### Airsonic

### Sickchill

### Deluge

### Pyload

### SABnzbd

## Network

Master hosts an NGinx reverse proxy that handles SSL termination and basic authentication.
It then forwards the requests to the NGinx Ingress exposed as a NodePort on the Kubernetes cluster.
Ingresses then define the rules to hit the proper service. 