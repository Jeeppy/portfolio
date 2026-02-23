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

## Application staging dans Coolify

### Créer le projet et l'environnement

1. Coolify → **Projects** → **New Project** → nom : `portfolio`
2. Créer deux environnements : `staging` et `production`
3. Dans `staging` → **New Resource** → **Docker Image**

### Configuration du service

| Paramètre | Valeur |
|-----------|--------|
| Name | `portfolio-api-staging` |
| Docker Image | `ghcr.io/<user>/portfolio-api` |
| Docker Image Tag | `develop` |
| Ports Exposes | `8000` |
| Domains | `http://portfolio-api-staging.domaine.fr` |

> **Important :** utiliser `http://` et non `https://` dans le domaine Coolify —
> Cloudflare gère déjà le TLS. Sinon boucle de redirection.

### Variables d'environnement

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Générer avec `openssl rand -hex 32` |
| `ADMIN_EMAIL` | Email du compte admin |
| `ADMIN_PASSWORD` | Mot de passe admin |
| `ENVIRONMENT` | `staging` |

### Tunnel Cloudflare pour le staging

Dans `/etc/cloudflared/config.yml` :

```yaml
  - hostname: portfolio-api-staging.domaine.fr
    service: http://<ip-vm>:80
```

```bash
cloudflared tunnel route dns <tunnel-name> portfolio-api-staging.domaine.fr
sudo systemctl restart cloudflared
```

## CI/CD — GitHub Actions

### Workflow CD (`.github/workflows/ci.yml`)

Job `deploy-staging` déclenché sur push vers `develop` après succès des tests :

- Build de l'image Docker depuis `./backend`
- Push vers `ghcr.io/<user>/portfolio-api:develop`
- Déclenchement du webhook Coolify

### Secrets GitHub nécessaires

| Secret | Description |
|--------|-------------|
| `COOLIFY_STAGING_WEBHOOK_URL` | URL webhook Coolify staging |
| `COOLIFY_TOKEN` | Token API Coolify (write + deploy + read) |

> Le token `GITHUB_TOKEN` est automatique pour pousser sur ghcr.io.

### Rendre le package public

Après le premier push : **github.com/<user> → Packages → portfolio-api → Package settings → Change visibility → Public**

## Accès

- **Interface Coolify** : `http://<ip-vm>:8000` (local) ou `https://coolify.domaine.fr` (via tunnel)
- **API staging** : `https://portfolio-api-staging.domaine.fr/health`
- **SSH** : `ssh <user>@<ip-vm>`
