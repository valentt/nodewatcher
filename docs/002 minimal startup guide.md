# Nodewatcher minimal startup guide

Getting nodewatcher v3.0 running with minimal changes (December 2024).

## Current state (after fixes)

| Component | Before | After |
|-----------|--------|-------|
| Base image | Ubuntu 16.04 (EOL) | Ubuntu 18.04 |
| Docker build | fails | **works** |
| Django version | 1.10.8 | 1.11.29 |
| Django startup | GEOS error | **works** |
| HTTP server | - | **HTTP 200** |
| Migrations | - | **219 applied** |
| PostgreSQL 9.5 + PostGIS | works | works |
| Redis 6 | works | works |
| InfluxDB 1.8 | works | works |

## Quick start

```bash
# Build and start
docker-compose -f docker-compose.test.yml build web
docker-compose -f docker-compose.test.yml up -d

# Wait for services, then run migrations
docker-compose -f docker-compose.test.yml exec web python manage.py migrate --noinput

# Collect static files (CSS, JS, icons)
docker-compose -f docker-compose.test.yml exec web python manage.py collectstatic --noinput

# Access at http://localhost:8000
```

## Changes made

### 1. Dockerfile
- Changed base image from `tozd/runit:ubuntu-xenial` to `ubuntu:18.04`
- Added `DEBIAN_FRONTEND=noninteractive`
- Added `runit` package

### 2. packages.txt
- Fixed Windows line endings (CRLF to LF)
- Updated package names for Ubuntu 18.04:
  - Removed `postgresql-client-9.5`, `postgresql-server-dev-9.5`
  - Added `libpq-dev`
  - Changed `libgdal1i` to `libgdal20`
  - Added `python-fontforge` (required for static files)

### 3. requirements-readthedocs.txt
- Upgraded Django from 1.10.8 to 1.11.29 (fixes GEOS version parsing)
- Added `django-braces==1.14.0` (last Python 2.7 compatible version)

### 4. scripts/docker-run, scripts/docker-wait-pgsql
- Fixed Windows line endings (CRLF to LF)

## Issues fixed

### Issue 1: GEOS version parsing (FIXED)

Django 1.10 couldn't parse GEOS 3.6 version string:
```
GEOSException: Could not parse version info string "3.6.2-CAPI-1.10.2 4d2925d6"
```

**Solution:** Upgraded Django to 1.11.29 (last Python 2.7 LTS version)

### Issue 2: django-braces Python 3 syntax (FIXED)

The oauth2_provider dependency pulled in django-braces 1.17 which uses Python 3 f-strings:
```
SyntaxError: invalid syntax
f"Define {self._class_name}.login_url..."
```

**Solution:** Pinned `django-braces==1.14.0` (last Python 2.7 compatible)

### Issue 3: Missing fontforge (FIXED)

Static files storage depends on fontforge for icon generation:
```
ImportError: No module named fontforge
```

**Solution:** Added `python-fontforge` to packages.txt

## Current packages.txt

```
libpq-dev
libxml2-dev
libxslt1-dev
libpcre3-dev
libgeoip1
libgeos-c1v5
libgdal-dev
libgdal20
fping
libffi-dev
python-apt
libaprutil1-dev
liblzma-dev
python-fontforge
eot-utils
```

## docker-compose.test.yml

```yaml
version: '2'
services:
    db:
        image: tozd/postgresql:9.5
        environment:
            PGSQL_ROLE_1_USERNAME: nodewatcher
            PGSQL_ROLE_1_PASSWORD: nodewatcher
            PGSQL_ROLE_1_FLAGS: LOGIN SUPERUSER
            PGSQL_DB_1_NAME: nodewatcher
            PGSQL_DB_1_OWNER: nodewatcher
            PGSQL_DB_1_ENCODING: UNICODE
            PGSQL_DB_1_POSTGIS: "true"
        volumes:
            - ./data/db:/var/lib/postgresql/9.5/main
    influxdb:
        image: tozd/influxdb:1.8
        volumes:
            - ./data/influxdb:/data
    redis:
        image: tozd/redis:6
    web:
        build: .
        command: bash -c "sleep 5 && python manage.py runserver 0.0.0.0:8000"
        environment:
            PYTHONUNBUFFERED: 1
        volumes:
            - .:/code
        ports:
            - "8000:8000"
        depends_on:
            - db
            - influxdb
            - redis
```

## Deprecation warnings (non-blocking)

These warnings appear but don't prevent operation:

1. **CryptographyDeprecationWarning**: Python 2 no longer supported
   - Will be fixed when upgrading to Python 3

2. **docker-compose version warning**: `version` attribute is obsolete
   - Can be removed from docker-compose.yml files

## Success criteria achieved

1. `docker-compose build` completes without errors
2. `docker-compose up` starts all services
3. `python manage.py migrate` runs without errors (219 migrations)
4. `python manage.py runserver` starts
5. http://localhost:8000 returns HTTP 200

## Next steps

1. Create superuser: `python manage.py createsuperuser`
2. Test basic functionality (create project, create node)
3. Test firmware generation
4. Document what works and what doesn't
5. Plan Python 3 migration (Django 2.2+ required)

## Technical notes

### Why Django 1.11.29?

- Last Django version supporting Python 2.7
- LTS release with security fixes
- Fixes GEOS version parsing issue
- Minimal breaking changes from 1.10

### Why Ubuntu 18.04?

- Still has Python 2.7 packages
- Has GEOS 3.6, GDAL 2.2
- Will reach EOL in 2028
- Provides bridge to Python 3 migration
