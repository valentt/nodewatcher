FROM ubuntu:18.04

LABEL maintainer="Jernej Kos <jernej@kos.mx>"

ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install base dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    git python python-dev python-pip python-setuptools build-essential \
    runit

# Install code dependencies
ADD ./packages.txt /code/packages.txt
RUN apt-get update && \
    cat /code/packages.txt | xargs apt-get --no-install-recommends -y install && \
    chmod 4755 /usr/bin/fping && \
    chmod 4755 /usr/bin/fping6

# Install Python package dependencies (do not use pip install -r here!)
ADD ./requirements.txt /code/requirements.txt
ADD ./requirements-readthedocs.txt /code/requirements-readthedocs.txt
RUN pip install --upgrade pip==20.3.4 setuptools==44.1.1 wheel six requests && \
    sed -i 's/^-r.*$//g' /code/requirements.txt && \
    cat /code/requirements-readthedocs.txt /code/requirements.txt | xargs -n 1 sh -c 'CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install $0 || true'

# Remove unneeded build-time dependencies
RUN apt-get purge python-dev build-essential -y && \
    apt-get autoremove -y && \
    rm -f /code/packages.txt /code/requirements.txt

# Add the current version of the code (needed for production deployments)
WORKDIR /code
ADD . /code

