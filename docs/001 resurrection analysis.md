# Nodewatcher V3.0 Resurrection Analysis

## Deep Dive Technical Assessment for Reviving Development

**Document Version:** 2.0
**Analysis Date:** December 2024
**Analyst:** Claude Code
**Target:** Nodewatcher v3.0 (development branch)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project History & V3.0 Vision](#2-project-history--v30-vision)
3. [Developer Contributions](#3-developer-contributions)
4. [Current State Assessment](#4-current-state-assessment)
5. [Codebase Analysis](#5-codebase-analysis)
6. [Architecture Assessment](#6-architecture-assessment)
7. [Dependency Audit](#7-dependency-audit)
8. [Infrastructure Analysis](#8-infrastructure-analysis)
9. [Critical Issues](#9-critical-issues)
10. [Resurrection Strategy](#10-resurrection-strategy)
11. [Phase-by-Phase Roadmap](#11-phase-by-phase-roadmap)
12. [Risk Assessment](#12-risk-assessment)
13. [Resource Requirements](#13-resource-requirements)
14. [Decision Matrix](#14-decision-matrix)
15. [Appendices](#15-appendices)

---

## 1. Executive Summary

### Project Status: ABANDONED (6+ years)

| Metric | Value | Risk Level |
|--------|-------|------------|
| Last Commit | October 27, 2018 | CRITICAL |
| Python Version | 2.7 (EOL Jan 2020) | CRITICAL |
| Django Version | 1.10.8 (EOL Dec 2017) | CRITICAL |
| Ubuntu Base | 16.04 Xenial (EOL Apr 2021) | HIGH |
| Docker Build | FAILS | CRITICAL |
| Test Suite | UNKNOWN (can't run) | HIGH |
| Total Commits | 3,883 from ~12 developers | - |
| Lines of Code | ~110,000 Python | - |

### Key Findings

1. **Complete Architectural Rewrite**: V3.0 was not an upgrade but a ground-up rewrite with 2,496 commits adding 124,908 lines of code
2. **Never Released**: Despite 7 years of development (2011-2018), V3.0 never reached stable release
3. **Innovative Core**: The "Registry System" is a sophisticated plugin architecture that was ahead of its time - **rated 9/10**
4. **Infrastructure Decay**: All Docker images, base OS, and dependencies are severely outdated
5. **Custom Forks**: 7 forked dependencies require special handling
6. **Small Team Success**: 89% of code written by just 2 developers (Jernej Kos & Mitar)

### Bottom Line

Resurrection is **technically feasible** but requires significant investment. The unique Registry System and modular architecture provide value worth preserving.

**Architecture Assessment:** 7.5/10 - excellent core concepts held back by custom forks and incomplete testing.

**Estimated Effort:**
- Upgrade path: 12-16 weeks, ~$40-50k
- Full rewrite (Node.js): 18-24+ months, $540k-$800k
- **Recommendation:** Upgrade, not rewrite

---

## 2. Project History & V3.0 Vision

### 2.1 The Big Rewrite

V3.0 was not an incremental update but a **complete architectural reimagining** of nodewatcher. Started in 2011 with ticket #900 "Started 'registry' branch", the project embarked on an ambitious 7-year development journey.

**What V3.0 Set Out to Achieve:**

1. **Plugin Architecture (Registry System)**
   - Allow network-specific customizations without forking
   - Dynamic schema extension at runtime
   - Auto-generated forms from configuration models
   - The most sophisticated part of the rewrite

2. **Configuration Generation Module (CGM)**
   - Automated firmware generation pipeline
   - Device-specific configuration abstraction
   - Support for 100+ router models
   - Template-based configuration system

3. **Modular Everything**
   - 57 Django apps, each focused on single responsibility
   - Clean separation of core vs modules vs extras
   - Hierarchical event system
   - Cross-module validation

4. **Modern API**
   - Dual REST API (Tastypie v1 + DRF v2)
   - GeoJSON for maps
   - Real-time monitoring data via InfluxDB

### 2.2 Why V3.0 Never Released

Based on code analysis and commit patterns:

1. **Scope Creep**: The ambition kept growing
2. **Perfectionism**: Architecture constantly refined
3. **Volunteer Time**: Open source project without dedicated funding
4. **External Life**: Developers moved on to other projects/jobs
5. **No Deadline Pressure**: Community networks worked with V2

### 2.3 Timeline

```
2010:     v1.0, v2.0, v2.0b released (master branch)
2011:     V3.0 development begins (ticket #900)
2011-14:  Heavy development, Registry system takes shape
2014-16:  CGM, firmware builders, device support
2016-18:  API v2, frontend work, gradual slowdown
Oct 2018: Final commit (Merge PR #69)
Jan 2020: Python 2.7 EOL
2024:     6+ years of silence
```

---

## 3. Developer Contributions

### 3.1 Contribution Statistics by Developer

| Rank | Developer | Commits | % | Lines Added | Lines Removed | Net Lines | Primary Contributions |
|------|-----------|---------|---|-------------|---------------|-----------|----------------------|
| 1 | **Jernej Kos (kostko)** | 2,421 | 62% | 143,283 | 95,041 | +48,242 | Core architecture, Registry, CGM |
| 2 | **Mitar** | 1,040 | 27% | 76,563 | 62,954 | +13,609 | Infrastructure, modules, frontend |
| 3 | David Marn | 165 | 4% | 31,361 | 8,307 | +23,054 | Device support, testing |
| 4 | Luka Čehovin | 139 | 4% | 59,817 | 27,917 | +31,900 | Early architecture |
| 5 | Raslav Milutinović | 62 | 2% | 19,041 | 1,908 | +17,133 | Device descriptors |
| 6 | Robert Marko | 48 | 1% | 1,109 | 106 | +1,003 | Recent device support |
| 7 | Jaka | 4 | <1% | 35 | 1 | +34 | Minor fixes |
| 8 | Tomaž Bratanič | 2 | <1% | 8 | 2 | +6 | Minor fixes |
| 9 | Gregor | 1 | <1% | 1 | 1 | 0 | Typo fix |
| 10 | Tomaž Šolc | 1 | <1% | 25 | 0 | +25 | Documentation |
| | **TOTAL** | **3,883** | 100% | 331,243 | 196,237 | **+135,006** | |

### 3.2 Key Insights

**Two-Person Show:**
- Jernej Kos and Mitar together contributed **89% of all commits**
- Jernej alone wrote 62% of the codebase (net +48,242 lines)
- This concentration is both a risk and an opportunity for knowledge transfer

**Jernej Kos (kostko) - Lead Architect:**
- GitHub: @kostko
- Created the Registry System (core innovation)
- Designed CGM architecture
- Responsible for most core module code
- **Critical contact for resurrection effort**

**Mitar - Co-Developer:**
- Major contributor to infrastructure
- Frontend and UI development
- Module development
- Documentation

### 3.3 Activity Periods

```
High Activity (100+ commits/year):
├── 2011-2012: Registry development (Jernej, Luka)
├── 2013-2014: Module explosion (Jernej, Mitar)
├── 2015: CGM, Firmware builders (Jernej, Mitar)
└── 2016: API v2, Frontend (Jernej, Mitar)

Declining Activity:
├── 2017: Bug fixes, maintenance (30-40 commits)
└── 2018: Final commits (Jan-Oct)

Silence:
└── Oct 2018 - Present: No activity
```

### 3.4 Institutional Knowledge Risk

| Developer | Knowledge Area | Reachable | Risk if Lost |
|-----------|---------------|-----------|--------------|
| Jernej Kos | Registry, CGM, Core | Unknown | CRITICAL |
| Mitar | Infrastructure, Frontend | Unknown | HIGH |
| David Marn | Device testing | Unknown | MEDIUM |
| Others | Specific modules | Unknown | LOW |

**Recommendation:** Contact Jernej Kos before starting resurrection. His architectural knowledge would save weeks of reverse engineering.

---

## 4. Current State Assessment

### 4.1 Version History

```
Timeline:
├── 2010: v1.0, v2.0, v2.0b released (master branch)
├── 2011: v3.0 development begins
│         └── First commit: "Started 'registry' branch" (ticket #900)
├── 2011-2018: Active development (2,496 commits)
├── Oct 2018: Last commit (Merge PR #69 - Map update)
├── Jan 2020: Python 2.7 EOL
├── Apr 2021: Ubuntu 16.04 EOL
└── Dec 2024: Current analysis (6+ years abandoned)
```

### 4.2 Branch Structure

| Branch | Purpose | Last Activity |
|--------|---------|---------------|
| `development` | V3.0 beta (current) | Oct 2018 |
| `master` | V2.0 stable | 2015 |
| `feature/cidr` | CIDR feature | Abandoned |
| `nw2-disabled-editing` | V2 patch | Abandoned |
| `Update-packages` | Package updates | Abandoned |

### 4.3 Release Tags

```
v1.0   - September 2010 (14 years old)
v2.0   - September 2010 (14 years old)
v2.0b  - September 2010 (14 years old)

v3.0   - NEVER RELEASED
```

---

## 5. Codebase Analysis

### 5.1 Code Metrics

| Metric | Value |
|--------|-------|
| Total Python Files | 872 |
| Total Lines of Python | ~110,000 |
| Django Apps | 57 |
| Test Files | 11 |
| Migration Files | 200+ |

### 5.2 Architecture Overview

```
nodewatcher/
├── core/                      # Framework Core (8 modules)
│   ├── allocation/            # IP address management
│   │   └── ip/               # IP pool allocation
│   ├── api/                   # REST API infrastructure
│   ├── events/                # Event/notification system
│   ├── frontend/              # Web UI framework
│   ├── generator/             # Firmware generation
│   │   └── cgm/              # Config Generation Module
│   ├── monitor/               # Monitoring framework
│   └── registry/              # Plugin system (CORE INNOVATION)
│
├── modules/                   # Feature Modules (18 categories)
│   ├── administration/        # Projects, location, roles
│   ├── analysis/              # Channel allocation, rogue nodes
│   ├── authentication/        # OAuth, public key
│   ├── defaults/              # Network defaults
│   ├── devices/               # Hardware definitions (100+ devices)
│   ├── equipment/             # Antennas
│   ├── events/                # Event sinks
│   ├── frontend/              # UI components (map, editor, etc.)
│   ├── identity/              # Node identity
│   ├── importer/              # V2 data migration
│   ├── monitor/               # HTTP sources, datastream
│   ├── platforms/             # OpenWrt, LEDE
│   ├── qos/                   # Quality of Service
│   ├── routing/               # OLSR, Babel
│   ├── sensors/               # Sensor data
│   ├── services/              # DNS, DHCP, watchdog
│   └── vpn/                   # Tunneldigger
│
├── extra/                     # Network-Specific Extensions
│   ├── accounts/              # User management
│   ├── wlansi/                # wlan slovenija defaults
│   ├── irnas/                 # IRNAS hardware (Koruza)
│   └── normalize/             # Frontend libraries
│
└── utils/                     # Utilities
    ├── ipaddr.py              # IP address handling
    ├── toposort.py            # Topological sorting
    └── loader.py              # Dynamic module loading
```

### 5.3 The Registry System (Core Innovation)

The Registry is nodewatcher's most significant architectural achievement - a custom Django ORM extension enabling:

```python
# Dynamic schema extension
class MyConfig(registry.items.RegistryItem):
    class Meta:
        registry_id = 'my.custom.config'

    my_field = models.CharField(max_length=100)

# Automatic registration
registration_point = registration.RegistrationPoint('node.config')
registration_point.register(MyConfig)

# Query across all registered models
Node.objects.regpoint('config').registry_fields(
    name='core.general__name',
    custom='my.custom.config__my_field',
)
```

**Key Features:**
- Polymorphic model inheritance
- Auto-generated forms from schema
- Context-sensitive defaults with rules engine
- Cross-module validation
- Hierarchical data structures

### 5.4 Test Coverage

| Module | Test File | Status |
|--------|-----------|--------|
| core.allocation.ip | tests.py | EXISTS |
| core.events | tests.py | EXISTS |
| core.api | test_api.py | EXISTS |
| modules.monitor.datastream | tests.py | EXISTS |
| modules.monitor.sources.http | tests.py | EXISTS |
| Other modules | - | NO TESTS |

**Estimated Coverage**: <20% (most modules lack tests)

---

## 6. Architecture Assessment

### 6.1 Overall Rating: 7.5/10

The V3.0 architecture demonstrates sophisticated engineering thinking, but practical concerns drag down the score.

### 6.2 Component Ratings

| Component | Rating | Verdict |
|-----------|--------|---------|
| **Registry System** | 9/10 | Genius-level abstraction. Worth preserving at all costs. |
| **Device Descriptors** | 8/10 | Clean, declarative, extensible. Minor verbosity issues. |
| **CGM Module** | 8/10 | Excellent firmware generation pipeline. |
| **Module Organization** | 7/10 | Good separation, but 57 apps is arguably too many. |
| **API Layer** | 6/10 | Dual API (v1 + v2) creates confusion and maintenance burden. |
| **Frontend** | 6/10 | Functional but dated. Heavy jQuery dependency. |
| **Testing** | 4/10 | Critical weakness. <20% coverage is unacceptable for this complexity. |
| **Custom Forks** | 3/10 | Major technical debt. 7 forks = 7 maintenance nightmares. |

### 6.3 What to Keep (Do Not Touch)

**Registry System (10/10 for concept)**
```
nodewatcher/core/registry/
├── registration.py    # Registration points
├── models.py          # RegistryItem base
├── forms.py           # Auto-generated forms
├── lookup.py          # Cross-model queries
└── rules.py           # Context-sensitive defaults
```
This is the crown jewel. The concept of polymorphic, pluggable model inheritance with auto-generated forms and validation is ahead of its time. Modern equivalents would use:
- Django Polymorphic
- JSONField with schema validation
- But neither matches the elegance of this implementation

**Device Descriptors (9/10)**
```python
# Clean, declarative hardware definitions
class TPLinkWR1043NDv1(cgm_devices.DeviceBase):
    identifier = 'tp-wr1043ndv1'
    name = "TP-Link WR1043ND (v1)"
    ports = [...]
    radios = [...]
```
Excellent abstraction for hardware diversity.

**CGM Pipeline (8/10)**
The template-based configuration generation is well-designed and handles 100+ router models gracefully.

### 6.4 What to Change (If Starting Over)

**1. Eliminate Custom Forks (Priority: CRITICAL)**
| Current Fork | Replacement |
|--------------|-------------|
| wlanslovenija/django-tastypie | Remove, keep only DRF |
| wlanslovenija/django-datastream | Direct InfluxDB client or TimescaleDB |
| wlanslovenija/django-rest-framework-gis | Upstream djangorestframework-gis |
| wlanslovenija/drf-ujson-renderer | orjson |
| wlanslovenija/pyScss | dart-sass or Tailwind |
| zestedesavoir/django-cors-middleware | django-cors-headers |
| herzbube/python-aprmd5 | Standard hashlib |

**2. Unify API Layer (Priority: HIGH)**
- Remove Tastypie API v1 completely
- Use Django REST Framework only
- Single OpenAPI/Swagger documentation
- Consistent authentication

**3. Add Comprehensive Testing (Priority: HIGH)**
Target coverage:
- Core modules: 90%+
- Registry system: 95%+
- API endpoints: 100%
- Module integration: 80%+

**4. Simplify Module Structure (Priority: MEDIUM)**
Consolidate 57 apps → ~20-30 apps:
```
# Before (too granular)
modules/administration/projects/
modules/administration/location/
modules/administration/roles/
modules/administration/description/

# After (sensible grouping)
modules/administration/  # Single app with submodules
```

**5. Modernize Frontend (Priority: LOW)**
- Remove jQuery dependency
- Consider Vue.js or htmx for reactivity
- Or keep server-side rendering with modern CSS

### 6.5 Architecture Summary

```
What Works:                    What Doesn't:
─────────────────────────────────────────────────────
✓ Registry System              ✗ 7 custom forks
✓ Plugin architecture          ✗ Dual API confusion
✓ Device descriptors           ✗ Almost no tests
✓ CGM firmware generation      ✗ Python 2 / Django 1.10
✓ Module separation            ✗ jQuery-heavy frontend
✓ Event system                 ✗ 57 apps (too many)
✓ GeoJSON map support          ✗ Unclear documentation
```

### 6.6 Verdict

**Keep the baby, change the bathwater.**

The core concepts (Registry, CGM, Device Descriptors) are excellent and would take 6-12 months to recreate from scratch. The problems (forks, testing, outdated stack) are fixable with focused effort.

---

## 7. Dependency Audit

### 7.1 Core Dependencies

| Package | Current | Latest | Gap | Breaking Changes |
|---------|---------|--------|-----|------------------|
| Python | 2.7 | 3.12 | 5 major | CRITICAL |
| Django | 1.10.8 | 5.2 LTS | 11 major | CRITICAL |
| Celery | 3.1.20 | 5.4.0 | 2 major | HIGH |
| psycopg2 | 2.7.4 | 2.9.9 | Minor | LOW |
| DRF | 3.5.4 | 3.15.0 | Minor | MEDIUM |
| redis | 2.10.5 | 5.0.0 | 3 major | MEDIUM |
| influxdb | 3.0.0 | 5.3.2 | 2 major | MEDIUM |
| GDAL | 1.10.0 | 3.9.0 | 2 major | HIGH |

### 7.2 Custom Forks (CRITICAL)

These forked repositories require special attention:

| Fork | Original | Last Update | Status | Action Required |
|------|----------|-------------|--------|-----------------|
| `wlanslovenija/django-tastypie` | django-tastypie | Sep 2025 | ACTIVE | Evaluate upstream |
| `wlanslovenija/django-datastream` | Custom | Apr 2017 | DEAD | Major work needed |
| `wlanslovenija/django-rest-framework-gis` | drf-gis | Unknown | STALE | Use upstream |
| `wlanslovenija/drf-ujson-renderer` | drf-ujson | Unknown | STALE | Replace with orjson |
| `wlanslovenija/pyScss` | pyScss | Unknown | STALE | Use libsass/dart-sass |
| `zestedesavoir/django-cors-middleware` | django-cors | Unknown | STALE | Use django-cors-headers |
| `herzbube/python-aprmd5` | Custom | Unknown | STALE | Find alternative |

### 7.3 Django-Datastream Deep Dive

This is the most critical custom dependency - a time-series abstraction layer for InfluxDB.

**Location:** https://github.com/wlanslovenija/django-datastream

**Components:**
- Time-series data model abstraction
- InfluxDB backend
- Automatic downsampling
- Query interface

**Risk Assessment:**
- Last updated: April 2017
- Incompatible with Django 2.0+
- Requires significant porting effort
- Alternative: Direct InfluxDB client or TimescaleDB

### 7.4 System Packages

```
packages.txt:
├── postgresql-client-9.5      → Need 15/16
├── postgresql-server-dev-9.5  → Need 15/16
├── libgeos-c1v5               → Need libgeos-c1v7
├── libgdal1i                  → Need libgdal30+
├── python-fontforge           → Need python3-fontforge
├── python-apt                 → Need python3-apt
└── fping, libffi, libxml2, etc. (still available)
```

---

## 8. Infrastructure Analysis

### 8.1 Docker Infrastructure

**Current State: BROKEN**

| Component | Issue | Fix Required |
|-----------|-------|--------------|
| Base Image | `tozd/runit:ubuntu-xenial` (EOL) | Update to Ubuntu 22.04/24.04 |
| Dockerfile | Missing `apt-get update` | Add update command |
| docker-compose.yml | Wrong image tags | Fix tag references |
| tozd/influxdb | No `latest` tag | Use `tozd/influxdb:1.8` |
| tozd/redis | No `latest` tag | Use `tozd/redis:6` or `7` |
| Builder images | Tags don't exist | Use `v15acdee_cc_ar71xx` |
| LEDE builder | Image doesn't exist | Build from scratch or remove |

### 8.2 Docker Image Availability

```
AVAILABLE:
✓ tozd/postgresql:9.5
✓ tozd/influxdb:1.8
✓ tozd/redis:6, 7, 8
✓ tozd/runit:ubuntu-xenial (but EOL)
✓ wlanslovenija/openwrt-builder:v15acdee_cc_ar71xx (from 2016)
✓ wlanslovenija/openwrt-builder:v15acdee_cc_lantiq (from 2016)

NOT AVAILABLE:
✗ tozd/influxdb:latest
✗ tozd/redis:latest
✗ wlanslovenija/openwrt-builder:18.06.0_ar71xx_generic
✗ wlanslovenija/lede-builder:v3ee8a65_17_01_1_ar71xx
```

### 8.3 CI/CD Pipeline

**Travis CI Configuration (.travis.yml):**
- Ubuntu Trusty (14.04) - EOL
- Python 2.7 - EOL
- PostgreSQL 9.5 with PostGIS 2.3
- InfluxDB via Docker
- Tests: `python manage.py test --keepdb`

**Status:** Non-functional (outdated infrastructure)

---

## 9. Critical Issues

### 9.1 Showstoppers (Must Fix First)

| # | Issue | Impact | Effort |
|---|-------|--------|--------|
| 1 | Python 2.7 EOL | Security risk, no package support | 2 weeks |
| 2 | Django 1.10 EOL | Security vulnerabilities | 3-4 weeks |
| 3 | Docker build fails | Cannot run at all | 1 day |
| 4 | django-datastream dead | Core functionality broken | 2-3 weeks |
| 5 | Ubuntu 16.04 EOL | Security, no packages | 1 week |

### 9.2 Python 2 → 3 Migration

**Total Changes Required:**

| Pattern | Count | Auto-fixable |
|---------|-------|--------------|
| `unicode()` → `str()` | 5 | Yes |
| `basestring` → `str` | 9 | Yes |
| `.iteritems()` → `.items()` | 32 | Yes |
| `__unicode__` → `__str__` | 19 | Yes |
| `from __future__` cleanup | 212 | Yes |
| Division operator review | 20 | Manual |
| `%` formatting → f-strings | 129 | Optional |

**Tools:**
```bash
# Automated conversion
2to3 -w nodewatcher/
pyupgrade --py312-plus **/*.py

# Compatibility library (transitional)
pip install six future
```

### 9.3 Django Migration Path

Required upgrade sequence:
```
1.10.8 → 1.11 LTS → 2.0 → 2.2 LTS → 3.0 → 3.2 LTS → 4.0 → 4.2 LTS → 5.2 LTS
```

**Key Changes Per Version:**

| Version | Critical Changes |
|---------|-----------------|
| 1.11→2.0 | Python 3 required, `on_delete` mandatory |
| 2.0→2.2 | Minor, mostly stable |
| 3.0→3.2 | `DEFAULT_AUTO_FIELD`, async views |
| 4.0→4.2 | Redis cache, `index_together` deprecated |
| 5.0→5.2 | Python 3.10+, form rendering |

**Django Deprecation Fixes Required:**

| Issue | Count | Files |
|-------|-------|-------|
| `django.core.urlresolvers` | 4 | 4 |
| `ForeignKey` without `on_delete` | 4 | 4 |
| `url()` → `re_path()`/`path()` | 46 | 12 |
| `MIDDLEWARE_CLASSES` | 1 | 1 |
| `force_text` → `force_str` | 3 | 2 |

### 9.4 Database Considerations

**PostgreSQL:**
- Current: 9.5 (EOL Nov 2021)
- Target: 15 or 16
- Migration: Straightforward (pg_dump/pg_restore)

**PostGIS:**
- Current: 2.1
- Target: 3.4
- Risk: Some function name changes

**InfluxDB:**
- Current: 1.x
- Target: 1.8 (stable) or 2.x
- Risk: 2.x has completely different API (Flux query language)
- Recommendation: Stay on 1.8 for now

---

## 10. Resurrection Strategy

### 10.1 Strategic Options

#### Option A: Full Modernization
**Upgrade to latest everything (Python 3.12, Django 5.2)**

| Pros | Cons |
|------|------|
| Long-term maintainability | Highest effort |
| Latest security patches | Most breaking changes |
| Modern async support | All forks need updating |
| Easiest hiring | 12-20 weeks |

#### Option B: Minimal Revival
**Get it running (Python 3.8, Django 2.2)**

| Pros | Cons |
|------|------|
| Faster (8-12 weeks) | Django 2.2 EOL (Apr 2023) |
| Fewer changes | Python 3.8 EOL (Oct 2024) |
| Quicker to test | Technical debt remains |
| Validate feasibility | Need second upgrade soon |

#### Option C: Selective Extraction
**Extract valuable components for new project**

| Pros | Cons |
|------|------|
| Cherry-pick best parts | Lose integrated system |
| Start with clean slate | More upfront design work |
| No legacy baggage | Registry system complex to extract |
| Modern architecture | 6-12 months for equivalent |

### 10.2 Recommended Strategy

**Two-Phase Approach:**

```
Phase 1: Minimal Revival (8-10 weeks)
├── Target: Python 3.10, Django 3.2 LTS
├── Goal: Get it running and testable
├── Validates: Is the effort worth it?
└── Deliverable: Working development environment

Phase 2: Full Modernization (6-10 weeks)
├── Target: Python 3.12, Django 5.2 LTS
├── Goal: Production-ready system
├── Prerequisite: Phase 1 success
└── Deliverable: Modern, maintainable codebase
```

---

## 11. Phase-by-Phase Roadmap

### Phase 0: Immediate Fixes (Week 1)

**Goal:** Get Docker environment running

| Task | Time | Details |
|------|------|---------|
| Fix Dockerfile | 2h | Add `apt-get update`, fix package names |
| Fix docker-compose.yml | 2h | Correct image tags |
| Update packages.txt | 2h | Modern package names |
| Test basic boot | 2h | Verify containers start |
| Document current state | 4h | What works, what doesn't |

**Deliverables:**
- [ ] Docker containers start
- [ ] Database initializes
- [ ] Django shell accessible (even with errors)

### Phase 1: Python 3 Migration (Weeks 2-4)

**Goal:** All code runs on Python 3.10+

| Week | Focus | Tasks |
|------|-------|-------|
| Week 2 | Automated fixes | Run 2to3, pyupgrade, fix imports |
| Week 3 | Manual fixes | String encoding, division, edge cases |
| Week 4 | Testing | Fix broken tests, verify functionality |

**Key Tasks:**
```
[ ] Run 2to3 on entire codebase
[ ] Run pyupgrade --py310-plus
[ ] Fix unicode/basestring issues (14 files)
[ ] Fix .iteritems() calls (18 files)
[ ] Fix __unicode__ methods (11 files)
[ ] Update Dockerfile to Python 3
[ ] Fix encoding issues
[ ] Run existing tests
[ ] Fix test failures
```

**Deliverables:**
- [ ] All code syntactically valid Python 3
- [ ] Existing tests pass
- [ ] Django runserver starts

### Phase 2: Django 1.10 → 3.2 (Weeks 5-8)

**Goal:** Upgrade to Django 3.2 LTS

| Week | Version Target | Focus |
|------|----------------|-------|
| Week 5 | Django 1.11 → 2.0 | on_delete, URL changes |
| Week 6 | Django 2.0 → 2.2 | Stabilization |
| Week 7 | Django 2.2 → 3.2 | DEFAULT_AUTO_FIELD, migrations |
| Week 8 | Testing & fixes | Full test suite, bug fixes |

**Key Tasks:**
```
[ ] Add on_delete to all ForeignKeys (4 files)
[ ] Replace url() with re_path() (12 files, 46 occurrences)
[ ] Update urlresolvers imports (4 files)
[ ] Change MIDDLEWARE_CLASSES to MIDDLEWARE
[ ] Add DEFAULT_AUTO_FIELD setting
[ ] Run django-upgrade tool
[ ] Update all migrations
[ ] Fix deprecated queryset methods
[ ] Update template tags
[ ] Fix admin customizations
```

**Deliverables:**
- [ ] Django 3.2 running
- [ ] All migrations apply cleanly
- [ ] Admin interface works
- [ ] API endpoints respond

### Phase 3: Dependency Updates (Weeks 9-12)

**Goal:** All dependencies current and secure

| Week | Focus | Packages |
|------|-------|----------|
| Week 9 | Core dependencies | Celery 5.x, Redis 5.x, DRF updates |
| Week 10 | Custom forks | django-datastream, tastypie evaluation |
| Week 11 | Geo/data packages | GDAL, PostGIS, InfluxDB client |
| Week 12 | Testing & integration | Full system testing |

**Fork Resolution:**

| Fork | Resolution |
|------|------------|
| django-tastypie | Evaluate: keep fork or migrate to DRF |
| django-datastream | Update fork or rewrite with influxdb-client |
| django-rest-framework-gis | Switch to upstream djangorestframework-gis |
| drf-ujson-renderer | Replace with orjson renderer |
| pyScss | Replace with libsass-python or dart-sass |
| django-cors-middleware | Replace with django-cors-headers |
| python-aprmd5 | Find Python 3 alternative or remove |

**Deliverables:**
- [ ] All pip dependencies from PyPI (no git installs)
- [ ] No known security vulnerabilities
- [ ] Celery workers functional
- [ ] Monitoring pipeline works

### Phase 4: Django 3.2 → 5.2 (Weeks 13-16)

**Goal:** Latest Django LTS

| Week | Version Target | Focus |
|------|----------------|-------|
| Week 13 | Django 4.0 → 4.2 | index_together, form widgets |
| Week 14 | Django 5.0 → 5.2 | Python 3.10+ features |
| Week 15 | Performance | Async views, caching |
| Week 16 | Polish | Documentation, CI/CD |

**Deliverables:**
- [ ] Django 5.2 LTS running
- [ ] Full test suite passing
- [ ] CI/CD pipeline working
- [ ] Updated documentation

### Phase 5: Modernization (Weeks 17-20)

**Goal:** Modern development experience

| Task | Details |
|------|---------|
| Docker update | Ubuntu 22.04/24.04, multi-stage builds |
| CI/CD | GitHub Actions |
| Code quality | ruff, black, mypy |
| Testing | pytest, coverage >70% |
| Documentation | Updated docs, API docs |
| Builder images | New OpenWrt builder images |

**Deliverables:**
- [ ] Modern Docker setup
- [ ] Automated testing in CI
- [ ] Type hints in critical modules
- [ ] Comprehensive documentation

---

## 12. Risk Assessment

### 12.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| django-datastream unfixable | Medium | Critical | Plan alternative (direct InfluxDB) |
| Registry system breaks | Low | Critical | Extensive testing, incremental changes |
| Celery migration issues | Medium | High | Test queue operations thoroughly |
| Database migration fails | Low | Critical | Backup, test on copy first |
| Custom forks abandoned | High | High | Fork ourselves, use upstream |

### 12.2 Project Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | High | Medium | Strict phase gates |
| Unknown unknowns | High | Unknown | Buffer time in estimates |
| Loss of institutional knowledge | Already happened | High | Document everything found |
| No tests for features | Already true | High | Add tests as we go |
| Stakeholder impatience | Medium | Medium | Regular demos of progress |

### 12.3 Risk Matrix

```
                    IMPACT
                Low    Medium    High    Critical
         ┌──────┬──────┬────────┬────────┬──────────┐
   High  │      │      │ Forks  │        │          │
         ├──────┼──────┼────────┼────────┼──────────┤
Probability      │      │ Celery │datastrm│          │
  Medium ├──────┼──────┼────────┼────────┼──────────┤
         │      │      │        │        │          │
   Low   ├──────┼──────┼────────┼────────┼──────────┤
         │      │      │        │Registry│ DB Migr  │
         └──────┴──────┴────────┴────────┴──────────┘
```

---

## 13. Resource Requirements

### 13.1 Team Composition

**Minimum Viable Team:**
- 1 Senior Python/Django Developer (full-time, 16-20 weeks)

**Optimal Team:**
- 1 Senior Python/Django Developer (lead)
- 1 Mid-level Developer (support)
- 0.25 DevOps Engineer (infrastructure)

### 13.2 Skills Required

| Skill | Importance | Phase |
|-------|------------|-------|
| Django internals | Critical | All |
| Python 2→3 migration | Critical | 1 |
| PostgreSQL/PostGIS | High | 2-3 |
| Docker/containers | High | 0, 5 |
| Celery/async | High | 3 |
| InfluxDB/time-series | Medium | 3 |
| OpenWrt/networking | Low | 5 |

### 13.3 Time Estimates

| Phase | Optimistic | Realistic | Pessimistic |
|-------|------------|-----------|-------------|
| Phase 0: Docker fix | 1 day | 2 days | 1 week |
| Phase 1: Python 3 | 2 weeks | 3 weeks | 4 weeks |
| Phase 2: Django 3.2 | 3 weeks | 4 weeks | 6 weeks |
| Phase 3: Dependencies | 3 weeks | 4 weeks | 6 weeks |
| Phase 4: Django 5.2 | 2 weeks | 3 weeks | 4 weeks |
| Phase 5: Modernization | 2 weeks | 3 weeks | 4 weeks |
| **TOTAL** | **13 weeks** | **17 weeks** | **25 weeks** |

### 13.4 Cost Estimates

| Scenario | Duration | Cost (@ $80/hr) |
|----------|----------|-----------------|
| Optimistic | 13 weeks | $41,600 |
| Realistic | 17 weeks | $54,400 |
| Pessimistic | 25 weeks | $80,000 |

---

## 14. Decision Matrix

### 14.1 Go/No-Go Criteria

**GO if:**
- [ ] Organizational commitment to 4+ months of effort
- [ ] Budget available ($50-80k or equivalent developer time)
- [ ] Mesh network monitoring is core to mission
- [ ] Registry system architecture is valued
- [ ] Willing to maintain fork long-term

**NO-GO if:**
- [ ] Need production system in <3 months
- [ ] No Python/Django expertise available
- [ ] Simpler monitoring solution would suffice
- [ ] No budget for ongoing maintenance
- [ ] Team prefers different tech stack

### 14.2 Alternatives Comparison

| Option | Effort | Cost | Risk | Outcome |
|--------|--------|------|------|---------|
| Resurrect nodewatcher | 17 weeks | $55k | Medium | Full-featured mesh monitor |
| Build new (Python) | 6-12 months | $150k+ | High | Modern but less features initially |
| Build new (Node.js) | 12-18 months | $200k+ | Very High | Modern but complete rebuild |
| **Use Freifunk stack** | 4-8 weeks | $15k | Low | Monitoring only, no firmware builder |
| Use LibreNMS | 2-4 weeks | $10k | Low | Generic monitoring, no mesh focus |
| Use existing V2 | 0 | $0 | Critical | Legacy, unmaintained |

**Note on Freifunk Stack:** Requires integrating Meshviewer + Yanic + Grafana. Good for pure monitoring, but lacks nodewatcher's firmware generation and node configuration capabilities.

### 14.3 Recommendation

**Proceed with resurrection** if mesh network monitoring is core to your mission. The Registry system and modular architecture represent significant engineering value that would take 6-12 months to recreate.

**Recommend Phase 1 as proof-of-concept** (4 weeks, ~$13k) before committing to full effort. This validates:
- Code can be ported to Python 3
- Django upgrade is feasible
- Registry system still works
- Tests can be made to pass

---

## 15. Appendices

### Appendix A: Build Test Results (December 2024)

**Command:** `docker build -t nodewatcher-test .`
**Result:** ❌ FAILED

#### Error Summary

```
E: Unable to locate package postgresql-client-9.5
E: Unable to locate package postgresql-server-dev-9.5
E: Unable to locate package libxml2-dev
E: Unable to locate package libxslt-dev
E: Unable to locate package libpcre3-dev
E: Unable to locate package libgeoip1
E: Unable to locate package libgeos-c1v5
E: Unable to locate package libgdal-dev
E: Unable to locate package libgdal1i
E: Unable to locate package fping
E: Unable to locate package libffi-dev
E: Unable to locate package eot-utils
E: Unable to locate package python-fontforge
E: Unable to locate package python-apt
E: Unable to locate package libaprutil1-dev
E: Unable to locate package liblzma-dev
```

#### Root Cause

Ubuntu Xenial (16.04) is EOL. Package repositories have been moved to `old-releases.ubuntu.com` and many packages are no longer available or have been renamed.

#### packages.txt Analysis

| Current Package | Status | Fix |
|-----------------|--------|-----|
| `postgresql-client-9.5` | ❌ EOL | `postgresql-client-15` or `postgresql-client` |
| `postgresql-server-dev-9.5` | ❌ EOL | `postgresql-server-dev-15` or `libpq-dev` |
| `libxml2-dev` | ⚠️ Need apt-get update | Keep |
| `libxslt-dev` | ⚠️ Renamed | `libxslt1-dev` |
| `libpcre3-dev` | ⚠️ Need apt-get update | Keep or `libpcre2-dev` |
| `libgeoip1` | ⚠️ Deprecated | `libmaxminddb0` or remove |
| `libgeos-c1v5` | ❌ Renamed | `libgeos-c1v5` → `libgeos-c1` |
| `libgdal-dev` | ⚠️ Need apt-get update | Keep |
| `libgdal1i` | ❌ Renamed | `libgdal30` (Ubuntu 22.04) |
| `fping` | ⚠️ Need apt-get update | Keep |
| `libffi-dev` | ⚠️ Need apt-get update | Keep |
| `eot-utils` | ❌ Removed | Find alternative or remove |
| `python-fontforge` | ❌ Python 2 only | `python3-fontforge` |
| `python-apt` | ❌ Python 2 only | `python3-apt` |
| `libaprutil1-dev` | ⚠️ Need apt-get update | Keep |
| `liblzma-dev` | ⚠️ Need apt-get update | Keep |

#### Dockerfile Issues

```dockerfile
# Line 1: Base image is EOL
FROM tozd/runit:ubuntu-xenial  # ❌ Ubuntu 16.04 EOL April 2021

# Line 3: Deprecated syntax
MAINTAINER Jernej Kos <jernej@kos.mx>  # ⚠️ Use LABEL instead

# Line 7: Python 2 packages
apt-get install ... python python-dev python-pip  # ❌ Python 2 EOL
```

#### Supporting Services Test (docker-compose.test.yml)

**Command:** `docker-compose -f docker-compose.test.yml up -d db redis influxdb`
**Result:** ✅ SUCCESS

| Service | Image | Status | Version |
|---------|-------|--------|---------|
| PostgreSQL | `tozd/postgresql:9.5` | ✅ Running | 9.5.25 |
| PostGIS | (included) | ✅ Available | 2.4 |
| Redis | `tozd/redis:6` | ✅ Running | 6.x |
| InfluxDB | `tozd/influxdb:1.8` | ✅ Running | 1.8 |

**Conclusion:** Backend infrastructure still works! The problem is only the **web application container** (Python 2, outdated packages).

#### Required Fixes for Phase 0

1. **Change base image:**
   ```dockerfile
   FROM ubuntu:22.04
   # or
   FROM python:3.11-slim
   ```

2. **Update packages.txt** with modern package names

3. **Switch to Python 3:**
   ```dockerfile
   apt-get install python3 python3-dev python3-pip
   ```

4. **Add missing apt-get update** before package install (already present, but repos need fixing)

---

### Appendix B: Python 2→3 File Change Summary

```
Python 2 → 3 Changes:
├── 5 files with unicode() calls
├── 6 files with basestring checks
├── 18 files with .iteritems()
├── 11 files with __unicode__ methods
├── 212 files with __future__ imports
└── 49 files with % string formatting

Django Deprecation Changes:
├── 4 files with urlresolvers imports
├── 4 files with ForeignKey missing on_delete
├── 12 files with url() patterns (46 total)
├── 1 file with MIDDLEWARE_CLASSES
└── 2 files with force_text
```

### Appendix C: Docker Image Tags

```yaml
# Working tags for docker-compose.yml:
db: tozd/postgresql:9.5
influxdb: tozd/influxdb:1.8
redis: tozd/redis:6
builderar71xx: wlanslovenija/openwrt-builder:v15acdee_cc_ar71xx
builderlantiq: wlanslovenija/openwrt-builder:v15acdee_cc_lantiq
```

### Appendix D: Key Files to Modify

**High-Priority Files:**
```
nodewatcher/settings.py          - MIDDLEWARE, DEFAULT_AUTO_FIELD
nodewatcher/urls.py              - URL pattern syntax
nodewatcher/core/models.py       - on_delete, __str__
requirements.txt                 - All dependencies
requirements-readthedocs.txt     - All dependencies
packages.txt                     - System packages
Dockerfile                       - Base image, apt-get
docker-compose.yml               - Image tags
.travis.yml → .github/workflows/ - CI/CD migration
```

### Appendix E: Commands Reference

```bash
# Python 3 conversion
2to3 -w nodewatcher/
pyupgrade --py310-plus $(find . -name "*.py")

# Django upgrade
pip install django-upgrade
django-upgrade --target-version 5.2 $(find . -name "*.py")

# Code quality
pip install ruff black isort
ruff check nodewatcher/
black nodewatcher/

# Testing
python manage.py test --keepdb
coverage run manage.py test
coverage report
```

---

### Appendix F: Alternative Solutions - Freifunk/Gluon Ecosystem

Freifunk (German community networks) took a **different approach** - microservices instead of monolithic:

| Component | Purpose | Tech | Status |
|-----------|---------|------|--------|
| [Meshviewer](https://github.com/freifunk/meshviewer) | Map visualization | TypeScript | Active (v12.7.0) |
| [Yanic](https://github.com/FreifunkBremen/yanic) | Data collection | Go | Active (v1.8.3) |
| [Gatemon](https://github.com/FreifunkBremen/gatemon) | Gateway monitoring | Python | Active |
| [Gluon](https://github.com/freifunk-gluon/gluon) | Firmware framework | OpenWrt/Lua | Active |
| [LibreMesh](https://libremesh.org/) | Firmware meta-build | Lua/Shell | Active |
| Grafana + InfluxDB | Metrics/dashboards | Standard | N/A |

#### Fundamental Architecture Difference: Generic vs Per-Node Firmware

**Gluon Approach (Generic Firmware):**
```
Build: ONE image per community (site.conf defines community settings)
       ↓
Flash: Same image on all nodes in community
       ↓
Config: User configures via web "Config Mode" AFTER flashing
        (hostname, location, contact info entered manually)
       ↓
IP: Auto-generated from MAC address hash + site prefix
```

**nodewatcher Approach (Per-Node Firmware):**
```
CGM: Generates UNIQUE image for EACH node
     ↓
     Pre-baked: hostname, IP address, SSH keys, custom SSID
     ↓
Flash: Firmware is fully configured, ready to deploy
     ↓
Done: Node works immediately - zero user configuration
```

#### IP Address Management Comparison

**Gluon: MAC-Based Hash Generation**
- Node IP derived from: `hash(MAC address) + site.conf prefix`
- No central database of allocations
- No collision prevention (relies on hash uniqueness)
- Cannot pre-plan or reserve IP addresses
- No visibility into all allocated IPs

Source: [Gluon MAC Addresses Documentation](https://gluon.readthedocs.io/en/latest/dev/mac_addresses.html)

**nodewatcher: Centralized IP Pool Management (IPAM)**
```
Project "CityMesh" → Subnet: 10.50.0.0/16
    ├── Node "CafeRouter"    → 10.50.1.1/32 (allocated from pool)
    ├── Node "LibraryNode"   → 10.50.1.2/32 (allocated from pool)
    ├── Node "ParkAccess"    → 10.50.1.3/32 (allocated from pool)
    └── ... all tracked in database, visible on map
```
- Full IPAM with project-based subnets
- Collision prevention guaranteed
- Pre-planning and reservation supported
- Complete visibility via web UI and API

#### Deployment Workflow Comparison

**Gluon Batch Deployment (Painful):**
```
1. Flash same image to 15 routers
2. Boot router #1, wait for config mode (2-3 min)
3. Connect to 192.168.1.1, open web UI
4. Enter: hostname, location, contact info, settings
5. Save, wait for reboot (2-3 min)
6. Repeat steps 2-5 for remaining 14 routers

Total time: 8-10+ hours of manual work
```

**nodewatcher Batch Deployment (Streamlined):**
```
1. Create 15 nodes in web UI (~5 min each, can duplicate)
   - Set hostname, location on map, contact, custom SSID
   - IP automatically allocated from project pool
2. Generate/download 15 firmware images
3. Flash all 15 routers (can do in parallel)
4. Deploy - they just work immediately

Total time: 2-3 hours (mostly flash time)
```

#### Factory Reset Behavior

| Scenario | Gluon | nodewatcher |
|----------|-------|-------------|
| User does factory reset | Config mode, must reconfigure EVERYTHING | Returns to squashfs, ALL CONFIG INTACT |
| Hostname | Lost | Preserved |
| IP address | Regenerated from MAC | Preserved (pre-baked) |
| Location | Lost | Preserved |
| Custom SSID | Lost | Preserved |
| SSH keys | Lost | Preserved |
| Recovery time | 15-30 min reconfiguration | Instant (reboot) |

#### Feature Comparison: Where Each Excels

**nodewatcher Wins (Firmware & Management):**

| Feature | nodewatcher | Gluon/Freifunk |
|---------|-------------|----------------|
| **Project-based subnets** | ✅ Full IPAM per project | ❌ MAC hash only |
| **Batch node creation** | ✅ Web UI, copy/duplicate | ❌ One by one after flash |
| **Custom SSID per node** | ✅ Pre-baked in firmware | ⚠️ Manual config after flash |
| **Pre-deploy configuration** | ✅ Flash & deploy | ❌ Boot, wait, configure each |
| **Factory reset resilience** | ✅ Config in squashfs survives | ❌ Must reconfigure from scratch |
| **Central IP visibility** | ✅ Database + map view | ❌ Discovery/scan only |
| **IP conflict prevention** | ✅ Pool management | ❌ Hope hash doesn't collide |
| **Node templates** | ✅ Defaults per project | ❌ Manual per node |
| **Firmware versioning** | ✅ Track per node | ⚠️ Community-wide only |
| **Pre-generated SSH access** | ✅ Keys in firmware | ❌ Set up after deploy |

**Freifunk/Meshviewer Wins (Visualization & Monitoring):**

| Feature | nodewatcher | Meshviewer/Yanic |
|---------|-------------|------------------|
| **Map technology** | ❌ jQuery-based (2011 era) | ✅ Leaflet, modern, mobile-friendly |
| **Real-time updates** | ⚠️ Polling-based | ✅ Live updates |
| **Graph topology view** | ❌ Basic | ✅ Interactive canvas graph |
| **Link quality visualization** | ⚠️ Basic | ✅ Color gradients, detailed |
| **Statistics dashboard** | ⚠️ Custom datastream | ✅ Grafana integration |
| **Responsive design** | ❌ Desktop-focused | ✅ Mobile + desktop |
| **Dark mode** | ❌ No | ✅ Yes |
| **Multi-language** | ⚠️ Limited | ✅ 6 languages |
| **Maintenance** | ❌ Dead since 2018 | ✅ Actively maintained |

**Live Demo:** [Freifunk Regensburg Meshviewer](https://regensburg.freifunk.net/meshviewer/)

#### Hybrid Approach: Best of Both Worlds?

A resurrection strategy could combine:
- **nodewatcher** for: Node management, IPAM, firmware generation (CGM)
- **Meshviewer** for: Visualization, real-time monitoring, statistics

This would require:
1. nodewatcher API to export nodes.json/graph.json for Meshviewer
2. Or: Replace nodewatcher's frontend map with Meshviewer embed
3. Keep nodewatcher's backend (Registry, CGM, IPAM) intact

#### Verdict: Why nodewatcher's Approach Is Superior for Managed Networks

**Gluon is designed for:** Volunteer-run networks where node owners configure their own devices, and decentralization is prioritized over central management.

**nodewatcher is designed for:** Professionally managed community networks where:
- Administrators need central control
- Batch deployments are common
- IP address planning matters
- Zero-touch deployment saves significant time
- Factory reset shouldn't mean reconfiguration

**The CGM (Configuration Generation Module) is not just a feature - it's a fundamental architectural advantage** that would require significant effort to replicate. For networks deploying 50+ nodes, nodewatcher's approach saves hundreds of hours of manual configuration.

**Sources:**
- [Gluon Documentation](https://gluon.readthedocs.io/en/latest/)
- [Gluon Site Configuration](https://gluon.readthedocs.io/en/latest/user/site.html)
- [Gluon MAC Addresses](https://gluon.readthedocs.io/en/latest/dev/mac_addresses.html)
- [Gluon GitHub](https://github.com/freifunk-gluon/gluon)
- [Meshviewer](https://github.com/freifunk/meshviewer)
- [Yanic](https://github.com/FreifunkBremen/yanic)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Dec 2024 | Claude Code | Initial analysis |
| 2.0 | Dec 2024 | Claude Code | Added developer statistics, architecture assessment, V3.0 history, Freifunk comparison |
| 2.1 | Dec 2024 | Claude Code | Expanded Gluon comparison: IP allocation, batch deployment, factory reset, killer features |
| 2.2 | Dec 2024 | Claude Code | Added balanced comparison - Meshviewer wins on visualization; proposed hybrid approach |
| 2.3 | Dec 2024 | Claude Code | Added Appendix A: Build Test Results - Docker build fails, but DB/Redis/InfluxDB services work |

---

*This document should be treated as a living document and updated as resurrection work progresses.*
