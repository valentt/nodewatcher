# Firmware Core

**Firmware Builders for Nodewatcher** - Docker-based OpenWrt firmware build system for community wireless networks.

Developed by [wlan slovenija](https://wlan-si.net), this repository provides pre-built OpenWrt firmware builders as Docker images, enabling rapid custom firmware generation for mesh network nodes monitored by [nodewatcher](https://github.com/wlanslovenija/nodewatcher).

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Nodewatcher Agent](#nodewatcher-agent)
- [Custom Packages](#custom-packages)
- [Building Firmware Images](#building-firmware-images)
- [Modifying Builders](#modifying-builders)
- [Docker Images](#docker-images)
- [Cloud Builder API](#cloud-builder-api)
- [Integration with Nodewatcher](#integration-with-nodewatcher)
- [Development](#development)
- [License](#license)

## Overview

This build system provides:

- **Pre-built Docker Images**: Ready-to-use firmware builders on Docker Hub
- **Rapid Image Generation**: Build custom firmware without full OpenWrt compilation
- **Nodewatcher Integration**: All monitoring packages pre-installed
- **Multi-Platform Support**: Multiple OpenWrt releases, targets, and architectures
- **Remote Building**: SSH and HTTP API for automated builds

### Pre-built Images on Docker Hub

| Image | Description |
|-------|-------------|
| [wlanslovenija/firmware-base](https://hub.docker.com/r/wlanslovenija/firmware-base) | Base image for all builders |
| [wlanslovenija/openwrt-builder](https://hub.docker.com/r/wlanslovenija/openwrt-builder) | Production OpenWrt builders |

Image tags follow the format: `<OpenWrt_Release>_<Target>_<SubTarget>`

Examples:
- `wlanslovenija/openwrt-builder:18.06.0_ar71xx_generic`
- `wlanslovenija/openwrt-builder:19.07.0_ath79_generic`

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FIRMWARE-CORE BUILD SYSTEM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    wlanslovenija/firmware-base                       │   │
│  │              (Ubuntu Bionic + Build Dependencies)                    │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                           │
│            ┌────────────────────┴────────────────────┐                     │
│            │                                         │                     │
│  ┌─────────▼─────────────────────┐     ┌────────────▼────────────────┐    │
│  │  openwrt-buildsystem          │     │  firmware-runtime           │    │
│  │  (OpenWrt Source + Feeds)     │     │  (SSH + Nginx + runit)      │    │
│  └─────────┬─────────────────────┘     └────────────┬────────────────┘    │
│            │                                         │                     │
│  ┌─────────▼─────────────────────┐                  │                     │
│  │  openwrt-imagebuilder-base    │                  │                     │
│  │  (SDK + Compiled Packages)    │                  │                     │
│  │  [NOT PUBLISHED - too large]  │                  │                     │
│  └─────────┬─────────────────────┘                  │                     │
│            │                                         │                     │
│            └────────────────────┬────────────────────┘                     │
│                                 │                                           │
│                    ┌────────────▼────────────────────┐                     │
│                    │    wlanslovenija/openwrt-builder │                     │
│                    │    (Final Builder - Published)   │                     │
│                    │    SSH:22 | HTTP:80              │                     │
│                    └─────────────────────────────────┘                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Build Flow

```
1. generate-dockerfiles     Creates version-specific Dockerfiles
         │
         ▼
2. Build firmware-base      Base Ubuntu image with build tools
         │
         ▼
3. Build buildsystem        OpenWrt source + feeds + patches
         │
         ▼
4. Build imagebuilder-base  Compiles SDK and all packages
         │
         ▼
5. docker-build-builders    Extracts imagebuilder to runtime
         │
         ▼
6. openwrt-builder          Final production image (published)
```

## Quick Start

### Running a Pre-built Builder

```bash
# Pull and run the builder
docker run --detach=true \
  --name builder-openwrt \
  --env "BUILDER_PUBLIC_KEY=ssh-rsa AAAA...your-key... builder@host" \
  wlanslovenija/openwrt-builder:18.06.0_ar71xx_generic
```

### Connect to the Builder

**Via Docker exec:**
```bash
docker exec -it builder-openwrt bash
```

**Via SSH:**
```bash
ssh builder@<container-ip>
```

### Build a Firmware Image

```bash
cd /builder/imagebuilder
su builder

make image PROFILE="TLWR1043" PACKAGES="wireless-tools wpad-mini \
  nodewatcher-agent nodewatcher-agent-mod-general \
  nodewatcher-agent-mod-resources nodewatcher-agent-mod-interfaces \
  nodewatcher-agent-mod-wireless nodewatcher-agent-mod-keys_ssh \
  nodewatcher-agent-mod-clients uhttpd ip-full"
```

### Retrieve the Built Image

**Via Docker cp:**
```bash
docker cp builder-openwrt:/builder/imagebuilder/bin/ar71xx/generic/openwrt-ar71xx-generic-tl-wr1043nd-v1-squashfs-factory.bin .
```

**Via SCP:**
```bash
scp builder@<container-ip>:/builder/imagebuilder/bin/ar71xx/generic/*.bin .
```

## Nodewatcher Agent

The **nodewatcher-agent** is a modular monitoring daemon that runs on network nodes and reports telemetry data back to the nodewatcher server.

### Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NODEWATCHER-AGENT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Core      │  │   Modules   │  │   Transport             │ │
│  │   Agent     │──│   (mod-*)   │──│   (HTTP Push/Poll)      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Nodewatcher Server │
                    │  /push/http/<uuid>/ │
                    └─────────────────────┘
```

### Agent Modules

| Module | Package | Description |
|--------|---------|-------------|
| **Core** | `nodewatcher-agent` | Base agent daemon |
| **General** | `nodewatcher-agent-mod-general` | System info (hostname, uptime, firmware) |
| **Resources** | `nodewatcher-agent-mod-resources` | CPU, memory, disk usage |
| **Interfaces** | `nodewatcher-agent-mod-interfaces` | Network interface statistics |
| **Wireless** | `nodewatcher-agent-mod-wireless` | WiFi signal, channel, AP info |
| **SSH Keys** | `nodewatcher-agent-mod-keys_ssh` | SSH public key management |
| **Clients** | `nodewatcher-agent-mod-clients` | Connected client information |
| **HTTP Push** | `nodewatcher-agent-mod-http_push` | Push telemetry to server |
| **Babel** | `nodewatcher-agent-mod-routing_babel` | Babel routing protocol data |

### Data Collection Flow

1. Agent modules collect system information
2. Data is serialized (JSON format)
3. Two transport modes available:
   - **Poll Mode**: Server fetches from node's HTTP endpoint (`/nodewatcher/feed`)
   - **Push Mode**: Node POSTs to server's endpoint (`/push/http/<uuid>/`)
4. Server processes and stores data in InfluxDB

## Custom Packages

All custom packages included in the builder (from `openwrt/packages`):

### Monitoring Packages

| Package | Description |
|---------|-------------|
| `nodewatcher-agent` | Core monitoring agent |
| `nodewatcher-agent-mod-*` | Agent modules (8 modules) |
| `nodewatcher-watchdog` | Node health monitoring |
| `nodeupgrade` | Firmware update management |

### Routing Packages

| Package | Description |
|---------|-------------|
| `babeld` | Babel mesh routing protocol |
| `olsrd` | OLSR mesh routing daemon |
| `olsrd-mod-txtinfo` | OLSR text info plugin |
| `olsrd-mod-jsoninfo` | OLSR JSON info plugin |

### VPN & Tunneling

| Package | Description |
|---------|-------------|
| `tunneldigger` | VPN tunnel client |
| `tunneldigger-broker` | VPN tunnel broker |
| `l2tp` | Layer 2 Tunneling Protocol |

### Security

| Package | Description |
|---------|-------------|
| `identity-pubkey` | Public key infrastructure |

### Complete Package List

```
babeld
l2tp
tunneldigger
tunneldigger-broker
nodewatcher-agent
nodewatcher-agent-mod-general
nodewatcher-agent-mod-resources
nodewatcher-agent-mod-interfaces
nodewatcher-agent-mod-wireless
nodewatcher-agent-mod-keys_ssh
nodewatcher-agent-mod-clients
nodewatcher-agent-mod-http_push
nodewatcher-agent-mod-routing_babel
nodewatcher-watchdog
nodeupgrade
olsrd
olsrd-mod-txtinfo
olsrd-mod-jsoninfo
identity-pubkey
```

Package source code: https://github.com/wlanslovenija/firmware-packages-opkg

## Building Firmware Images

### Prerequisites

- Docker installed and running
- Sufficient disk space (2-3GB+ per build)
- Internet connectivity

### Using Pre-built Builders

```bash
# 1. Run the builder container
docker run --detach=true \
  --name my-builder \
  --env "BUILDER_PUBLIC_KEY=ssh-rsa AAAA..." \
  wlanslovenija/openwrt-builder:18.06.0_ar71xx_generic

# 2. Enter the container
docker exec -it my-builder bash

# 3. Switch to builder user and directory
cd /builder/imagebuilder
su builder

# 4. Build firmware
make image PROFILE="<DEVICE_PROFILE>" PACKAGES="<package-list>"

# 5. Find output
ls -la bin/<target>/<subtarget>/
```

### Available Device Profiles

List available profiles:
```bash
make info
```

Common profiles include:
- `TLWR1043` - TP-Link WR1043ND
- `TLWR841` - TP-Link WR841N/ND
- `UBNT` - Ubiquiti devices
- Many more depending on target/subtarget

### Example Build Commands

**TP-Link WR1043ND with full monitoring:**
```bash
make image PROFILE="TLWR1043" PACKAGES="wireless-tools wpad-mini \
  kmod-netem kmod-pktgen ntpclient qos-scripts iperf horst \
  wireless-info cronscripts iwinfo \
  nodewatcher-agent nodewatcher-agent-mod-general \
  nodewatcher-agent-mod-resources nodewatcher-agent-mod-interfaces \
  nodewatcher-agent-mod-wireless nodewatcher-agent-mod-keys_ssh \
  nodewatcher-agent-mod-clients nodewatcher-agent-mod-http_push \
  uhttpd ip-full"
```

**Minimal build with just monitoring:**
```bash
make image PROFILE="TLWR841" PACKAGES="nodewatcher-agent \
  nodewatcher-agent-mod-general nodewatcher-agent-mod-interfaces \
  uhttpd"
```

## Modifying Builders

### When to Modify

- Adding new packages not in the default list
- Supporting new hardware/devices
- Changing default configurations
- Updating to new OpenWrt releases

### Build Your Own Builder

```bash
# Clone the repository
git clone https://github.com/wlanslovenija/firmware-core.git
cd firmware-core

# Add packages to openwrt/packages file (if needed)
echo "my-custom-package" >> openwrt/packages

# Build the builder image
sudo ./openwrt/scripts/build <version> <target> <subtarget>

# Example: Build for OpenWrt 18.06.0, ar71xx target, generic subtarget
sudo ./openwrt/scripts/build 18.06.0 ar71xx generic
```

### Build Script Workflow

The `./openwrt/scripts/build` script:

1. **generate-dockerfiles**: Creates Dockerfiles for the specified version
2. **Build firmware-base**: Base image with build dependencies
3. **Build openwrt-buildsystem**: OpenWrt source with feeds
4. **Build openwrt-imagebuilder-base**: Compiles all packages
5. **docker-build-builders**: Creates final runtime image

### Adding New Packages

1. Add package to `firmware-packages-opkg` repository
2. Add package name to `openwrt/packages` file
3. Rebuild the builder image

### Directory Structure After Build

```
firmware-core/
├── docker/
│   ├── openwrt/                    # Generated Dockerfiles
│   │   ├── buildsystem/
│   │   │   └── <version>/
│   │   │       └── Dockerfile
│   │   └── imagebuilder_base/
│   │       └── <version>/<target>/<subtarget>/
│   │           └── Dockerfile
│   └── runtime/                    # Runtime base image
│       ├── Dockerfile
│       └── etc/
│           ├── nginx/
│           └── service/
├── openwrt/
│   ├── packages                    # Package list
│   ├── scripts/
│   │   ├── build                   # Main build script
│   │   ├── docker-build            # Package compilation
│   │   ├── docker-build-builders   # Final image creation
│   │   └── generate-dockerfiles    # Dockerfile generation
│   └── tools/
│       └── packages2json.py        # Metadata generator
└── Dockerfile                      # firmware-base image
```

## Docker Images

### Image Hierarchy

```
tozd/base:ubuntu-bionic
        │
        ▼
firmware-base (Dockerfile)
    │       │
    │       ▼
    │   openwrt-buildsystem (generated)
    │       │
    │       ▼
    │   openwrt-imagebuilder-base (generated, not published)
    │       │
    ▼       │
firmware-runtime (docker/runtime/Dockerfile)
        │
        ▼
openwrt-builder (final, published)
```

### Image Details

#### firmware-base
- **Base**: `tozd/base:ubuntu-bionic`
- **Purpose**: Build environment with all dependencies
- **Contents**: gcc, make, git, python, ncurses, ssl, etc.
- **User**: `builder` (non-root)

#### firmware-runtime
- **Base**: `tozd/runit:ubuntu-bionic`
- **Purpose**: Runtime environment for builders
- **Ports**: 22 (SSH), 80 (HTTP)
- **Services**: sshd, nginx
- **Contents**: Minimal runtime + package serving

#### openwrt-builder
- **Base**: firmware-runtime
- **Purpose**: Production firmware builder
- **Contents**: OpenWrt imagebuilder + pre-compiled packages
- **Published**: Yes (Docker Hub)

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BUILDER_PUBLIC_KEY` | SSH public key for authentication |

## Cloud Builder API

The Cloud Builder API 0.1 standard for remote firmware building:

### Filesystem Layout

| Path | Description |
|------|-------------|
| `/builder/imagebuilder/` | OpenWrt image builder |
| `/builder/packages/` | Pre-built opkg packages |

### HTTP Endpoints

| Endpoint | Description |
|----------|-------------|
| `/packages/` | Package repository (autoindex) |
| `/metadata` | Builder metadata (JSON) |

### Metadata Format

```json
{
  "platform": "openwrt",
  "architecture": "ar71xx_generic",
  "version": "18.06.0",
  "packages": {
    "nodewatcher-agent": {
      "name": "nodewatcher-agent",
      "version": "1.0.0",
      "dependencies": ["libuci", "libubox"],
      "source": "firmware-packages-opkg",
      "size": 12345,
      "size_installed": 45678,
      "checksum_md5": "abc123...",
      "checksum_sha256": "def456...",
      "description": "Nodewatcher monitoring agent"
    }
  }
}
```

### SSH Access

- **User**: `builder`
- **Authentication**: Public key (via `BUILDER_PUBLIC_KEY`)
- **Working Directory**: `/builder/imagebuilder`

## Integration with Nodewatcher

### How Nodewatcher Uses Builders

```
┌─────────────────────┐         ┌─────────────────────────────┐
│  Nodewatcher Server │         │     Builder Container       │
│                     │         │                             │
│  1. User requests   │         │                             │
│     firmware        │         │                             │
│         │           │  SSH    │                             │
│  2. Connect to ─────┼────────►│  3. Run make image          │
│     builder         │         │     PROFILE=... PACKAGES=.. │
│         │           │         │         │                   │
│  4. Download ◄──────┼─────────┼─────────┘                   │
│     .bin file       │   SCP   │                             │
│         │           │         │                             │
│  5. Store/serve     │         │                             │
│     to user         │         │                             │
└─────────────────────┘         └─────────────────────────────┘
```

### Configuration in Nodewatcher

1. **Add Builder** in admin interface:
   - Host: Container hostname/IP
   - Private Key: Matching key for `BUILDER_PUBLIC_KEY`

2. **Add Device Descriptor** for supported hardware:
   - Profile name
   - Default packages
   - Architecture mapping

### Generated Firmware Features

Firmware built through nodewatcher automatically includes:
- Node-specific network configuration
- Mesh routing parameters (OLSR/Babel)
- VPN/tunnel settings
- Nodewatcher agent with server URL
- SSH keys for management

## Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/wlanslovenija/firmware-core.git
cd firmware-core

# Build for specific target
sudo ./openwrt/scripts/build 18.06.0 ar71xx generic

# The resulting image will be tagged as:
# wlanslovenija/openwrt-builder:18.06.0_ar71xx_generic
```

### Testing a Builder

```bash
# Run locally built builder
docker run --detach=true \
  --name test-builder \
  --env "BUILDER_PUBLIC_KEY=$(cat ~/.ssh/id_rsa.pub)" \
  wlanslovenija/openwrt-builder:18.06.0_ar71xx_generic

# Test SSH access
ssh builder@$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-builder)

# Test HTTP access
curl http://$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-builder)/packages/
```

### Script Reference

| Script | Purpose |
|--------|---------|
| `openwrt/scripts/build` | Main build entry point |
| `openwrt/scripts/generate-dockerfiles` | Create version-specific Dockerfiles |
| `openwrt/scripts/docker-build` | Compile packages inside container |
| `openwrt/scripts/docker-build-builders` | Create final builder image |
| `openwrt/tools/packages2json.py` | Generate metadata JSON |

### Requirements for Building

**System:**
- Linux host (or Docker Desktop)
- 4GB+ RAM recommended
- 10GB+ free disk space
- Internet connectivity

**Software:**
- Docker Engine
- Git
- Bash

## Resources

- **GitHub**: https://github.com/wlanslovenija/firmware-core
- **Package Repository**: https://github.com/wlanslovenija/firmware-packages-opkg
- **Nodewatcher**: https://github.com/wlanslovenija/nodewatcher
- **Docker Hub**: https://hub.docker.com/u/wlanslovenija
- **Issue Tracker**: https://dev.wlan-si.net/report
- **Mailing List**: https://wlan-si.net/lists/info/development
- **OpenWrt Wiki**: https://openwrt.org/docs/guide-developer/start

## License

- **Code**: GNU Affero General Public License v3 or later
- **Content**: Creative Commons Attribution-ShareAlike 3.0

See [LICENSE](LICENSE) and [COPYING](COPYING) for details.

---

**Note**: This firmware builder is designed for community wireless networks. For production use, ensure you understand the security implications and customize the `BUILDER_PUBLIC_KEY` for your deployment.
