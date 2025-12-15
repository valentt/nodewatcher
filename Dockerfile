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
RUN pip install --upgrade pip wheel && \
    pip install "setuptools<58" && \
    sed -i 's/^-r.*$//g' /code/requirements.txt && \
    cat /code/requirements-readthedocs.txt /code/requirements.txt | grep -v '^#' | grep -v '^$' | while read pkg; do \
        CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install "$pkg" || true; \
    done && \
    cd /tmp && \
    apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -L https://files.pythonhosted.org/packages/source/d/datastream/datastream-0.5.19.tar.gz -o datastream-0.5.19.tar.gz && \
    tar xzf datastream-0.5.19.tar.gz && \
    cd datastream-0.5.19 && \
    sed -i "s/pytz>=2012h/pytz>=2012/" setup.py && \
    find . -name "*.py" -exec sed -i "s/except \\([A-Za-z]*\\), \\([a-z]*\\):/except \\1 as \\2:/g" {} \; && \
    pip install --no-build-isolation . && \
    cd /tmp && rm -rf datastream* && \
    git clone https://github.com/wlanslovenija/django-datastream.git && \
    cd django-datastream && \
    git checkout a54a2e735950c5c31ec71613750bdf1ce194389f && \
    sed -i "s/pytz>=2012h/pytz>=2012/" setup.py && \
    find . -name "*.py" -exec sed -i "s/except \\([A-Za-z]*\\), \\([a-z]*\\):/except \\1 as \\2:/g" {} \; && \
    pip install --no-build-isolation --no-deps . && \
    cd / && rm -rf /tmp/django-datastream

# Remove unneeded build-time dependencies
RUN apt-get purge python3-dev build-essential -y && \
    apt-get autoremove -y && \
    rm -f /code/packages.txt /code/requirements.txt

# Add the current version of the code (needed for production deployments)
WORKDIR /code
ADD . /code
