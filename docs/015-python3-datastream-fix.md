# Python 3 Migration: Fixing Datastream Dependencies

## Overview

The nodewatcher project depends on `datastream` and `django-datastream` packages that were written for Python 2 and have never been updated for Python 3. This document outlines the issues and the fix plan.

## Current State

- Tag `v0.1.0-broken-py3-migration` marks the state before these fixes
- Docker image builds but Django fails to start due to datastream Python 2 incompatibilities

## Issues Identified

### 1. Metaclass Syntax (Critical)

**File:** `datastream/api.py`

Python 2 syntax:
```python
class _Base(object):
    class _BaseMetaclass(type):
        def __lt__(cls, other):
            return cls._order < other._order
        # ...

    __metaclass__ = _BaseMetaclass  # Python 2 only!
```

Python 3 requires:
```python
class _Base(object, metaclass=_BaseMetaclass):
    pass
```

**Problem:** The metaclass provides comparison operators (`__lt__`, `__gt__`, etc.) so that Granularity classes can be sorted. Without the metaclass properly applied, sorting fails with:
```
TypeError: '<' not supported between instances of 'type' and 'type'
```

### 2. basestring Reference

**File:** `datastream/api.py` line ~63

Python 2:
```python
if isinstance(atom, basestring):
```

Python 3 fix:
```python
if isinstance(atom, str):
```

### 3. Exception Syntax (Already Fixed)

**Files:** Multiple files in datastream and django-datastream

Python 2:
```python
except KeyError, exception:
```

Python 3:
```python
except KeyError as exception:
```

### 4. Dictionary Methods

Python 2 `.iteritems()`, `.iterkeys()`, `.itervalues()` need to become `.items()`, `.keys()`, `.values()`.

### 5. Print Statements

Any remaining `print "x"` needs to become `print("x")`.

### 6. Unicode/String Handling

Python 2 `unicode` type doesn't exist in Python 3 - use `str` instead.

## Fix Strategy

### Option A: Patch During Docker Build (Current Approach)

Modify Dockerfile to apply sed patches to the downloaded packages before installation.

**Pros:**
- No need to maintain forks
- Changes are isolated to build process

**Cons:**
- Complex sed commands
- Fragile if package structure changes
- Hard to test patches

### Option B: Create Local Patched Copies (Recommended)

1. Download datastream and django-datastream source
2. Apply all necessary Python 3 fixes
3. Store patched versions in `vendor/` directory
4. Install from local path in Dockerfile

**Pros:**
- Full control over the code
- Easy to test and debug
- Can be committed to repository

**Cons:**
- Need to maintain vendored copies

### Option C: Fork on GitHub

Fork both repositories, apply fixes, and install from forked URLs.

**Pros:**
- Clean separation
- Could contribute back upstream

**Cons:**
- More infrastructure to maintain

## Implementation Plan (Option B - Recommended)

### Step 1: Create Vendor Directory Structure

```
vendor/
├── datastream/
│   └── (patched datastream package)
└── django-datastream/
    └── (patched django-datastream package)
```

### Step 2: Patch datastream Package

Files to modify:
- `datastream/api.py` - metaclass syntax, basestring, exception syntax
- `datastream/backends/*.py` - exception syntax, dict methods
- `datastream/utils.py` - any Python 2 specific code

Specific fixes for `api.py`:

1. Move `_BaseMetaclass` outside of `_Base` class
2. Change `_Base` definition to use Python 3 metaclass syntax
3. Replace `basestring` with `str`
4. Fix all exception syntax

### Step 3: Patch django-datastream Package

Files to modify:
- `django_datastream/__init__.py` - exception syntax
- `django_datastream/views.py` - any Python 2 code
- `django_datastream/resources.py` - any Python 2 code

### Step 4: Update Dockerfile

```dockerfile
# Copy vendored packages
ADD ./vendor /vendor

# Install vendored packages
RUN pip install /vendor/datastream && \
    pip install /vendor/django-datastream
```

### Step 5: Update .gitignore

Ensure vendor directory is tracked (not ignored).

### Step 6: Test

1. Run `python manage.py check`
2. Run `python manage.py migrate --check`
3. Run `python manage.py runserver` (with database)

## Detailed Patches Required

### datastream/api.py

```python
# Before (around line 10-40):
class Granularity(object):
    class _Base(object):
        class _BaseMetaclass(type):
            def __lt__(cls, other):
                return cls._order < other._order
            # ... other comparison methods

        __metaclass__ = _BaseMetaclass
        # ... rest of _Base

# After:
class Granularity(object):
    class _BaseMetaclass(type):
        def __lt__(cls, other):
            return cls._order < other._order
        def __gt__(cls, other):
            return cls._order > other._order
        def __le__(cls, other):
            return cls._order <= other._order
        def __ge__(cls, other):
            return cls._order >= other._order
        def __eq__(cls, other):
            return cls._order == other._order
        def __str__(cls):
            return cls._name

    class _Base(object, metaclass=_BaseMetaclass):
        _order = None
        _key = None
        # ... rest of _Base (without metaclass definition inside)
```

```python
# Before (line ~63):
if isinstance(atom, basestring):

# After:
if isinstance(atom, str):
```

### All Files - Exception Syntax

```python
# Before:
except SomeError, e:

# After:
except SomeError as e:
```

## Timeline

1. Create vendor directory and copy packages - 5 min
2. Apply Python 3 patches to datastream - 20 min
3. Apply Python 3 patches to django-datastream - 10 min
4. Update Dockerfile - 5 min
5. Test and iterate - 15 min

**Total estimated time: ~1 hour**

## Success Criteria

1. `docker-compose build web` succeeds
2. `python manage.py check` runs without errors
3. Web application starts and responds to requests

## Rollback Plan

If fixes don't work:
- Return to tag `v0.1.0-broken-py3-migration`
- Consider alternative time-series solutions (InfluxDB direct, TimescaleDB, etc.)
