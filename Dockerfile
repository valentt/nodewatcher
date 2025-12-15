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
RUN pip install --upgrade pip setuptools wheel && \
    sed -i 's/^-r.*$//g' /code/requirements.txt && \
    cat /code/requirements-readthedocs.txt /code/requirements.txt | xargs -n 1 sh -c 'CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install $0 || true'

# Remove unneeded build-time dependencies
RUN apt-get purge python3-dev build-essential -y && \
    apt-get autoremove -y && \
    rm -f /code/packages.txt /code/requirements.txt

# Add the current version of the code (needed for production deployments)
WORKDIR /code
ADD . /code
