FROM ubuntu:22.04

LABEL maintainer="Jernej Kos <jernej@kos.mx>"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Update packages and install base dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    git python3 python3-dev python3-pip python3-setuptools build-essential \
    runit && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Install code dependencies
ADD ./packages.txt /code/packages.txt
RUN apt-get update && \
    cat /code/packages.txt | xargs apt-get --no-install-recommends -y install && \
    chmod 4755 /usr/bin/fping && \
    chmod 4755 /usr/bin/fping6

# Install Python package dependencies (do not use pip install -r here!)
ADD ./requirements.txt /code/requirements.txt
ADD ./requirements-readthedocs.txt /code/requirements-readthedocs.txt
ADD ./vendor /code/vendor
RUN pip install --upgrade pip wheel && \
    pip install "setuptools<58" && \
    sed -i 's/^-r.*$//g' /code/requirements.txt && \
    cat /code/requirements-readthedocs.txt /code/requirements.txt | grep -v '^#' | grep -v '^$' | while read pkg; do \
        CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install "$pkg" || true; \
    done && \
    pip install /code/vendor/datastream && \
    pip install --no-deps /code/vendor/django-datastream && \
    # Fix grako for Python 3.10+ (collections.Mapping -> collections.abc.Mapping)
    sed -i 's/from collections import defaultdict, Mapping/from collections import defaultdict\nfrom collections.abc import Mapping/' /usr/local/lib/python*/dist-packages/grako/grammars.py && \
    sed -i 's/from collections import Mapping/from collections.abc import Mapping/' /usr/local/lib/python*/dist-packages/grako/contexts.py 2>/dev/null || true

# Remove unneeded build-time dependencies
RUN apt-get purge python3-dev build-essential -y && \
    apt-get autoremove -y && \
    rm -f /code/packages.txt /code/requirements.txt

# Add the current version of the code (needed for production deployments)
WORKDIR /code
ADD . /code
