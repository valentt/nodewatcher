# Nodewatcher

**Nodewatcher** is an open-source network planning, deployment, monitoring, and maintenance platform designed for community wireless networks. Developed by [wlan slovenija](https://wlan-si.net), it provides comprehensive tools for managing mesh networks at scale.

> **Note**: This is the `development` branch containing version 3.0 (beta). For the stable 2.0 version, switch to the `master` branch.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Module System](#module-system)
- [Monitoring System](#monitoring-system)
- [Firmware Generation](#firmware-generation)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

## Features

- **Network Planning**: Design and plan wireless mesh network deployments
- **Node Management**: Register, configure, and manage network nodes
- **Real-time Monitoring**: Collect and visualize network telemetry data
- **Firmware Generation**: Automatically build custom firmware images for supported hardware
- **Geospatial Support**: Map-based visualization with PostGIS integration
- **REST API**: Comprehensive API (v1 and v2) for integration and automation
- **Extensible Architecture**: Plugin-based registry system for customization
- **Multi-platform Support**: OpenWRT and LEDE firmware platforms
- **Routing Protocol Support**: OLSR and Babel mesh routing protocols

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         NODEWATCHER v3                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐ │
│  │   Web UI    │    │  REST API   │    │   Firmware Generator    │ │
│  │  (Django)   │    │   v1/v2     │    │   (Celery Workers)      │ │
│  └──────┬──────┘    └──────┬──────┘    └───────────┬─────────────┘ │
│         │                  │                       │               │
│         └──────────────────┼───────────────────────┘               │
│                            │                                       │
│  ┌─────────────────────────▼─────────────────────────────────────┐ │
│  │                    DJANGO CORE                                 │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │ │
│  │  │ Registry │  │ Monitor  │  │Generator │  │   Events     │   │ │
│  │  │ System   │  │ System   │  │   CGM    │  │   System     │   │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                            │                                       │
│  ┌─────────────────────────▼─────────────────────────────────────┐ │
│  │                     DATA LAYER                                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐    │ │
│  │  │  PostgreSQL  │  │   InfluxDB   │  │      Redis        │    │ │
│  │  │   + PostGIS  │  │ (timeseries) │  │ (broker/cache)    │    │ │
│  │  └──────────────┘  └──────────────┘  └───────────────────┘    │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                  FIRMWARE BUILDERS (Docker)                    │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐   │ │
│  │  │  OpenWRT   │  │  OpenWRT   │  │      LEDE              │   │ │
│  │  │   AR71xx   │  │   Lantiq   │  │      AR71xx            │   │ │
│  │  └────────────┘  └────────────┘  └────────────────────────┘   │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Description |
|-----------|-------------|
| **Registry System** | Plugin-based architecture with polymorphic model inheritance |
| **Generator (CGM)** | Configuration Generation Module for building firmware images |
| **Monitor System** | Celery-based async monitoring with processor pipelines |
| **Datastream** | Time-series data abstraction layer with InfluxDB backend |
| **REST API** | v1 (Tastypie) and v2 (Django REST Framework) endpoints |

## Requirements

### Databases

| Database | Version | Purpose |
|----------|---------|---------|
| PostgreSQL | 9.5+ | Primary relational database |
| PostGIS | 2.1+ | Geospatial extension |
| InfluxDB | 3.0+ | Time-series monitoring data |
| Redis | 2.10+ | Message broker and caching |

### System Dependencies

```
postgresql-client-9.5
postgresql-server-dev-9.5
libxml2-dev
libxslt-dev
libpcre3-dev
libgeoip1
libgeos-c1v5
libgdal-dev
libgdal1i
fping
libffi-dev
eot-utils
python-fontforge
python-apt
libaprutil1-dev
liblzma-dev
```

### Python Dependencies

- Python 2.7
- Django 1.10.8
- Celery 3.1.20
- See `requirements.txt` for complete list

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/wlanslovenija/nodewatcher.git
   cd nodewatcher
   git checkout development
   ```

2. **Pull Docker images**
   ```bash
   docker-compose pull
   ```

3. **Build the development environment**
   ```bash
   docker-compose build
   ```

4. **Start all services**
   ```bash
   docker-compose up
   ```

5. **Initialize the database** (in a new terminal)
   ```bash
   docker-compose run web python manage.py migrate
   ```

6. **Compile stylesheets**
   ```bash
   docker-compose run web python manage.py collectstatic -l
   ```

7. **Create admin account**

   Visit http://localhost:8000/setup/ and follow the instructions.

8. **Access the application**
   - Web UI: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - API: http://localhost:8000/api/v3/

### Docker Services

| Service | Port | Description |
|---------|------|-------------|
| `web` | 8000 | Django development server |
| `db` | 5432 | PostgreSQL + PostGIS |
| `influxdb` | 8086 | InfluxDB time-series database |
| `redis` | 6379 | Redis message broker |
| `generator` | - | Celery worker for firmware generation |
| `monitorq` | - | Celery worker for monitoring |
| `builderar71xx` | - | OpenWRT AR71xx firmware builder |
| `builderlantiq` | - | OpenWRT Lantiq firmware builder |
| `builderar71xx_lede` | - | LEDE AR71xx firmware builder |

### Data Persistence

By default, database files are stored in `/tmp/nodewatcher-db` and `/tmp/nodewatcher-influxdb`. These locations are cleared on system restart. To persist data, modify the volume paths in `docker-compose.yml`:

```yaml
volumes:
  - /path/to/persistent/storage:/var/lib/postgresql/9.5/main
```

## Configuration

### Main Settings

Configuration is managed in `nodewatcher/settings.py`. Key settings include:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'nodewatcher',
        'USER': 'nodewatcher',
        'PASSWORD': 'nodewatcher',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Celery
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('generator', Exchange('generator'), routing_key='generator'),
    Queue('monitor', Exchange('monitor'), routing_key='monitor'),
)

# InfluxDB
DATASTREAM_BACKEND = 'datastream.backends.influxdb.Backend'
DATASTREAM_BACKEND_SETTINGS = {
    'database': 'nodewatcher',
    'host': 'influxdb',
    'port': 8086,
}
```

### Monitoring Configuration

```python
# OLSR monitor host
OLSRD_MONITOR_HOST = 'localhost'
OLSRD_MONITOR_PORT = 2006

# Monitor runs
MONITOR_RUNS = {
    'latency': {'workers': 10, 'interval': 600},
    'telemetry': {'workers': 15, 'interval': 300},
    'telemetry-push': {'workers': 5},
    'datastream': {'workers': 2, 'interval': 700},
    'topology': {'workers': 5, 'interval': 60},
}
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PYTHONUNBUFFERED` | Set to `1` for unbuffered output |
| `C_FORCE_ROOT` | Set to `true` to allow Celery to run as root |
| `BUILDER_PUBLIC_KEY` | SSH public key for firmware builder authentication |

## API Reference

### API v3 Endpoints

Base URL: `/api/v3/`

| Endpoint | Description |
|----------|-------------|
| `/node/` | Node data (configuration and monitoring) |
| `/pool/ip/` | IP address pools |
| `/link/` | Network links between nodes |
| `/project/` | Network projects |
| `/event/` | System events |
| `/warning/` | Node warnings |
| `/build_result/` | Firmware build results |
| `/statistics/device/` | Device statistics |
| `/statistics/project/` | Project statistics |
| `/statistics/status/` | Status statistics |
| `/unknown_node/` | Unregistered nodes |
| `/user_authentication_key/` | User authentication keys |

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `format` | Response format | `?format=json` |
| `limit` | Results per page | `?limit=10` |
| `offset` | Pagination offset | `?offset=20` |
| `fields` | Select specific fields | `?fields=config:core.general` |
| `filters` | Filter results | `?filters=config:core.general__name="test"` |

### Field Groups

**Configuration Fields (`config:`):**
- `core.general` - Node name and general info
- `core.type` - Node type
- `core.project` - Associated project
- `core.location` - Geographic location
- `core.routerid` - Router identifiers
- `core.interfaces` - Network interfaces
- `core.authentication` - Authentication settings

**Monitoring Fields (`monitoring:`):**
- `core.general` - General monitoring data
- `core.interfaces` - Interface statistics
- `system.status` - System status
- `system.resources.general` - CPU, memory, disk usage
- `network.routing.topology` - Routing topology
- `network.clients` - Connected clients

### Example Queries

```bash
# Get all nodes in JSON format
curl "http://localhost:8000/api/v3/node/?format=json"

# Get node with specific fields
curl "http://localhost:8000/api/v3/node/?fields=config:core.general&fields=monitoring:system.status"

# Filter nodes by name
curl "http://localhost:8000/api/v3/node/?filters=config:core.general__name__contains=\"test\""

# Get nodes seen after a specific time
curl "http://localhost:8000/api/v3/node/?filters=monitoring:core.general__last_seen__gt=\"2024-01-01T00:00:00Z\""
```

## Module System

Nodewatcher uses a modular architecture with 57+ Django apps organized into categories:

### Core Modules (`nodewatcher/core/`)

| Module | Description |
|--------|-------------|
| `allocation` | IP address pool management |
| `api` | REST API infrastructure |
| `events` | Event system |
| `frontend` | Web UI components |
| `generator` | Firmware generation |
| `generator.cgm` | Configuration Generation Module |
| `monitor` | Monitoring infrastructure |
| `registry` | Plugin registry system |

### Feature Modules (`nodewatcher/modules/`)

| Category | Modules |
|----------|---------|
| **Administration** | `projects`, `location`, `description`, `roles`, `status`, `banner` |
| **Analysis** | `channel_allocation`, `rogue_nodes` |
| **Authentication** | `public_key`, `oauth` |
| **Devices** | Hardware device definitions |
| **Frontend** | `map`, `list`, `topology`, `statistics`, `editor`, `mynodes`, `setup`, `display` |
| **Identity** | `base`, `public_key`, `hmac` |
| **Monitor** | `sources.http`, `datastream`, `topology`, `validation_*` |
| **Platforms** | `openwrt`, `lede` |
| **Routing** | `olsr`, `babel` |
| **Services** | `dns`, `dhcp`, `nodeupgrade`, `watchdog` |
| **VPN** | `tunneldigger` |

### Extra Modules (`nodewatcher/extra/`)

| Module | Description |
|--------|-------------|
| `accounts` | User account management |
| `wlansi` | wlan slovenija specific defaults |
| `irnas` | IRNAS project specifics (Koruza) |

## Monitoring System

### Running the Monitor

```bash
# Run all monitor runs
docker-compose run web python manage.py monitord

# Run specific monitor
docker-compose run web python manage.py monitord --run=telemetry

# Limit cycles
docker-compose run web python manage.py monitord --cycles=10

# Process single node
docker-compose run web python manage.py monitord --process-only-node=<uuid>
```

### Monitor Runs

| Run | Workers | Interval | Description |
|-----|---------|----------|-------------|
| `telemetry` | 15 | 300s | Main telemetry collection |
| `latency` | 10 | 600s | RTT measurements |
| `telemetry-push` | 5 | on-demand | HTTP push handling |
| `datastream` | 2 | 700s | Data downsampling |
| `topology` | 5 | 60s | Network topology |

### Telemetry Pipeline

The monitoring system processes data through a pipeline of processors:

1. Validators (reboot, version, interfaces)
2. HTTP telemetry collection
3. System status (CPU, memory, disk)
4. Interface metrics
5. Client information
6. Survey data
7. Topology (OLSR, Babel)
8. Generic sensors
9. VPN/tunneling
10. Node status determination

## Firmware Generation

### Setting Up Builders

1. **Create a build channel** in the admin interface (`/admin/`)

2. **Add builders** with the following configuration:
   - Host: `builderar71xx`, `builderlantiq`, or `builderar71xx_lede`
   - Use the development private key from `docker-compose.yml`

3. **Generate firmware** through the web UI or API

### Supported Platforms

| Platform | Architecture | Image |
|----------|--------------|-------|
| OpenWRT Chaos Calmer | AR71xx | `wlanslovenija/openwrt-builder:v15acdee_cc_ar71xx` |
| OpenWRT Chaos Calmer | Lantiq | `wlanslovenija/openwrt-builder:v15acdee_cc_lantiq` |
| LEDE 17.01.1 | AR71xx | `wlanslovenija/lede-builder:v3ee8a65_17_01_1_ar71xx` |

### Custom Builder Keys

For production, generate new SSH keys:

```bash
ssh-keygen -f builder.key -C "builder@host"
```

Set the public key via the `BUILDER_PUBLIC_KEY` environment variable on the builder container.

## Development

### Running Tests

```bash
docker-compose run web python manage.py test --keepdb
```

### Code Style

```bash
# PEP8 compliance
pep8 nodewatcher/

# Linting
pylint nodewatcher/
```

### Management Commands

```bash
# Database migrations
docker-compose run web python manage.py migrate

# Create superuser
docker-compose run web python manage.py createsuperuser

# Collect static files
docker-compose run web python manage.py collectstatic -l

# Import from nodewatcher v2
docker-compose run web python manage.py import_nw2 dump.json

# Run development server
docker-compose run web python manage.py runserver 0.0.0.0:8000
```

### Project Structure

```
nodewatcher/
├── nodewatcher/               # Django project
│   ├── core/                  # Core framework modules
│   ├── modules/               # Feature modules
│   ├── extra/                 # Extra/specialized features
│   ├── settings.py            # Django configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI application
│   └── celery.py              # Celery configuration
├── docs/                      # Sphinx documentation
├── docker/                    # Production Docker images
├── scripts/                   # Utility scripts
├── manage.py                  # Django management
├── docker-compose.yml         # Development environment
├── Dockerfile                 # Base Docker image
├── requirements.txt           # Python dependencies
└── packages.txt               # System dependencies
```

## Documentation

- **Online Documentation**: http://docs.nodewatcher.net
- **Development Wiki**: https://dev.wlan-si.net/wiki/Nodewatcher
- **Paper**: https://github.com/wlanslovenija/nodewatcher-paper

### Local Documentation

Documentation is built with Sphinx:

```bash
cd docs/
make html
```

## Resources

- **GitHub**: https://github.com/wlanslovenija/nodewatcher
- **Issue Tracker**: https://dev.wlan-si.net/report/14
- **Mailing List**: https://wlan-si.net/lists/info/nodewatcher
- **wlan slovenija**: https://wlan-si.net

## License

Nodewatcher is released under the **GNU Affero General Public License v3 (AGPLv3)**.

---

**Note**: This is version 3.0 (development). The codebase uses Python 2.7 and Django 1.10.8, which are no longer maintained. Consider this when planning production deployments.
