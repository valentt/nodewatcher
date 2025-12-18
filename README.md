# nodewatcher

**Open-source network planning, deployment, monitoring, and maintenance platform for community wireless networks.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

---

## What is nodewatcher?

nodewatcher is a comprehensive platform for managing community mesh networks. It helps network operators and communities to:

- **Plan** wireless network deployments with geographic visualization
- **Deploy** nodes with automatically generated custom firmware
- **Monitor** network health, performance, and connectivity in real-time
- **Maintain** large-scale mesh networks with minimal manual intervention

### Who is it for?

- **Community networks** - Open wireless mesh networks like Freifunk, Guifi, etc.
- **Network operators** - Managing fleets of OpenWrt-based routers
- **Researchers** - Studying mesh network behavior and performance
- **ISPs** - Running wireless last-mile infrastructure

> **Note:** This project was abandoned from 2018-2025 and has been revived. See [Project History](#project-history) for details.

---

## Features

- **Network Planning** - Design and coordinate mesh network deployments
- **Node Management** - Register, configure, and manage network nodes
- **Real-time Monitoring** - Collect and visualize network telemetry data
- **Firmware Generation** - Automatically build custom OpenWrt firmware images
- **Geospatial Support** - Map-based visualization with PostGIS
- **REST API** - Comprehensive API (v1 and v2) for integration
- **Multi-platform Support** - OpenWrt and LEDE firmware platforms
- **Routing Protocols** - OLSR and Babel mesh routing support

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.10+, Django 4.2 LTS |
| **Database** | PostgreSQL 13+ with PostGIS |
| **Time-series** | InfluxDB 1.8 |
| **Cache/Broker** | Redis 7 |
| **Task Queue** | Celery 5.2 |
| **Frontend** | Django Templates, JavaScript |
| **Container** | Docker, Docker Compose |

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/valentt/nodewatcher.git
cd nodewatcher

# Start all services
docker compose up -d

# Run database migrations
docker compose exec web python manage.py migrate

# Create admin user (or visit http://localhost:8000/setup/)
docker compose exec web python manage.py createsuperuser

# Access the application
open http://localhost:8000
```

### Docker Services

| Service | Port | Description |
|---------|------|-------------|
| `web` | 8000 | Django application server |
| `db` | 5432 | PostgreSQL + PostGIS |
| `influxdb` | 8086 | InfluxDB time-series database |
| `redis` | 6379 | Redis message broker |
| `builderar71xx` | - | OpenWrt AR71xx firmware builder |
| `builderlantiq` | - | OpenWrt Lantiq firmware builder |
| `builderar71xx_lede` | - | LEDE AR71xx firmware builder |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         NODEWATCHER v3.1                            │
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
└─────────────────────────────────────────────────────────────────────┘
```

---

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
| `/statistics/` | Network statistics |

### Example

```bash
# Get all nodes
curl "http://localhost:8000/api/v3/node/?format=json"

# Get node with specific fields
curl "http://localhost:8000/api/v3/node/?fields=config:core.general&fields=monitoring:system.status"
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [PYTHON3_MIGRATION.md](PYTHON3_MIGRATION.md) | Python 3 / Django 4.2 migration guide |
| [docs/](docs/) | Technical documentation and feature specs |

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

GNU Affero General Public License v3.0 - see [LICENSE](LICENSE) file.

---

## Contact & Support

- **Maintainer:** [Valent Turković](https://github.com/valentt)
- **Repository:** https://github.com/valentt/nodewatcher
- **Issues:** https://github.com/valentt/nodewatcher/issues

---

## Project History

### Origins: wlan slovenija (2009-2018)

nodewatcher was originally created by **[wlan slovenija](https://en.wikipedia.org/wiki/Wlan_slovenija)** - a pioneering open wireless community network in Slovenia.

| Year | Milestone |
|------|-----------|
| **2009** | Project founded in Ljubljana with 10 initial nodes |
| **2009-2017** | Network grew to 400+ active nodes, 1.6M+ connections |
| **2012-2017** | Multiple Google Summer of Code participations |
| **2015** | International collaboration with FunkFeuer (Austria) and Otvorena mreža (Croatia) |
| **October 2018** | Last upstream commit - project became dormant |

The original wlan slovenija infrastructure (wlan-si.net, dev.wlan-si.net, docs.nodewatcher.net) is no longer operational.

### Revival: Otvorena mreža (2025)

In December 2025, the project was revived by **[Valent Turković](https://github.com/valentt)** from **Otvorena mreža** (Croatia), a partner network since 2015.

**v3.1.0 updates:**
- Migration from Python 2.7 to Python 3.10+
- Upgrade from Django 1.x to Django 4.2 LTS
- 70+ dependencies updated
- 200+ compatibility fixes

### Version History

| Version | Date | Maintainer | Notes |
|---------|------|------------|-------|
| **v3.1.0** | Dec 2025 | Otvorena mreža | Python 3 / Django 4.2 migration |
| v3.0.x | 2017-2018 | wlan slovenija | Last original releases |
| v2.0 | 2015-2017 | wlan slovenija | Stable production version |
| v1.0 | 2009-2014 | wlan slovenija | Initial releases |

### Historical References

- [nodewatcher paper](https://github.com/wlanslovenija/nodewatcher-paper) - Academic paper (2015)
- [Wikipedia: wlan slovenija](https://en.wikipedia.org/wiki/Wlan_slovenija) - Project history

### Acknowledgments

- **wlan slovenija team** - Original developers (Jernej Kos, Mitar Milutinović, and contributors)
- **Google Summer of Code** - Student contributor funding (2012-2017)
- **European Commission** - Project co-funding
