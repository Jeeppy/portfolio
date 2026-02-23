# Installation Coolify sur Proxmox

## Infrastructure

- **Cluster Proxmox** : 3 nœuds
- **VM Coolify** : hébergée sur le nœud avec le plus de RAM disponible
- **IP fixe** : à définir selon ton réseau local
- **OS** : Debian 13 (Trixie)

## Specs VM

| Ressource | Valeur |
|-----------|--------|
| RAM | 8 Go |
| vCPU | 4 |
| Disque | 50 Go |
| OS | Debian 13 |

## Création de la VM

1. Proxmox → nœud cible → **Create VM**
2. ISO : `debian-13.0-amd64-netinst.iso`
3. Specs ci-dessus, disque VirtIO, réseau VirtIO sur `vmbr0`
4. Installation Debian : uniquement `SSH server` + `standard system utilities`

## Configuration réseau (IP fixe)

Fichier `/etc/network/interfaces` :

```
auto <interface>      # vérifier avec : ip a
iface <interface> inet static
    address <ip>/24
    gateway <gateway>
    dns-nameservers 1.1.1.1 8.8.8.8
```

> Si le DNS ne résout pas après reboot : `echo "nameserver 1.1.1.1" > /etc/resolv.conf`

## Installation de sudo et curl

```bash
su -
apt update && apt upgrade -y
apt install -y sudo curl
usermod -aG sudo <user>
# Déconnecter/reconnecter SSH pour activer sudo
```

## Installation Coolify

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | sudo bash
```

## Problèmes rencontrés

### 1. Partition `/var` trop petite

Si Debian crée une partition `/var` séparée trop petite lors de l'installation,
Docker et containerd la remplissent rapidement → erreur `No space left on device`.

**Solution : déplacer Docker vers une partition avec plus d'espace (ex: `/srv`)**

```bash
sudo systemctl stop docker.socket docker.service

sudo mkdir -p /srv/docker
sudo mv /var/lib/docker /srv/docker/lib
```

Fichier `/etc/docker/daemon.json` :

```json
{
  "data-root": "/srv/docker/lib"
}
```

**Déplacer containerd également**

```bash
sudo systemctl stop containerd

sudo mkdir -p /srv/containerd
sudo mv /var/lib/containerd /srv/containerd/lib

sudo containerd config default | sudo tee /etc/containerd/config.toml > /dev/null
```

Dans `/etc/containerd/config.toml`, modifier :

```
root = "/srv/containerd/lib"
```

Puis relancer :

```bash
sudo systemctl start containerd
sudo systemctl start docker
sudo docker start coolify
```

## État final

Tous les containers Coolify healthy :

| Container | Image | Rôle |
|-----------|-------|------|
| coolify | coollabsio/coolify | Application principale |
| coolify-db | postgres:15-alpine | Base de données |
| coolify-redis | redis:7-alpine | Cache |
| coolify-realtime | coollabsio/coolify-realtime | WebSockets |
| coolify-proxy | traefik:v3.x | Reverse proxy |
| coolify-sentinel | coollabsio/sentinel | Monitoring |

## Tunnel Cloudflare

Ajouter la règle dans `/etc/cloudflared/config.yml` sur le LXC cloudflared :

```yaml
  - hostname: coolify.domaine.fr
    service: http://<ip-vm>:8000
```

Créer l'entrée DNS via CLI :

```bash
cloudflared tunnel route dns <tunnel-name> coolify.domaine.fr
```

Redémarrer cloudflared :

```bash
sudo systemctl restart cloudflared
```

> **Note :** Le wildcard `*.preview.domaine.fr` pour les review environments nécessite
> un certificat Cloudflare Advanced (payant) ou une configuration TLS alternative.
> À traiter lors de l'issue #66 (review environments).

## Accès

- **Interface Coolify** : `http://<ip-vm>:8000` (local) ou `https://coolify.domaine.fr` (via tunnel)
- **SSH** : `ssh <user>@<ip-vm>`
