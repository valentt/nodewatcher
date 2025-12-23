# OpenWrt 24.10 ImageBuilder for Nodewatcher
# This Dockerfile creates a builder container compatible with nodewatcher's
# SSH-based firmware generation protocol.
#
# Build:
#   docker build -t nodewatcher-builder-openwrt:24.10.5-ath79 \
#     --build-arg TARGET=ath79 \
#     --build-arg SUBTARGET=generic \
#     .
#
# Run:
#   docker run -d -p 2222:22 -p 8080:80 \
#     -e BUILDER_PUBLIC_KEY="ssh-rsa AAAA..." \
#     nodewatcher-builder-openwrt:24.10.5-ath79

FROM debian:bookworm-slim

LABEL maintainer="nodewatcher@wlan-si.net"
LABEL description="OpenWrt 24.10 ImageBuilder for Nodewatcher"

# Build arguments
ARG OPENWRT_VERSION=24.10.0
ARG TARGET=ath79
ARG SUBTARGET=generic

# Environment variables
ENV OPENWRT_VERSION=${OPENWRT_VERSION}
ENV TARGET=${TARGET}
ENV SUBTARGET=${SUBTARGET}
ENV BUILDER_USER=builder
ENV BUILDER_HOME=/home/builder

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    gawk \
    gettext \
    git \
    libncurses5-dev \
    libssl-dev \
    nginx \
    openssh-server \
    python3 \
    rsync \
    sudo \
    supervisor \
    unzip \
    wget \
    xz-utils \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create builder user
RUN useradd -m -d ${BUILDER_HOME} -s /bin/bash ${BUILDER_USER} && \
    echo "${BUILDER_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Setup SSH
RUN mkdir -p /var/run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    echo "AllowUsers ${BUILDER_USER}" >> /etc/ssh/sshd_config

# Download and setup OpenWrt ImageBuilder
USER ${BUILDER_USER}
WORKDIR ${BUILDER_HOME}

# Download ImageBuilder
# Note: OpenWrt 24.10+ uses .tar.zst format instead of .tar.xz
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends zstd && sudo rm -rf /var/lib/apt/lists/*

RUN IMAGEBUILDER_URL="https://downloads.openwrt.org/releases/${OPENWRT_VERSION}/targets/${TARGET}/${SUBTARGET}/openwrt-imagebuilder-${OPENWRT_VERSION}-${TARGET}-${SUBTARGET}.Linux-x86_64.tar.zst" && \
    echo "Downloading ImageBuilder from: ${IMAGEBUILDER_URL}" && \
    wget -q "${IMAGEBUILDER_URL}" -O imagebuilder.tar.zst && \
    tar --zstd -xf imagebuilder.tar.zst && \
    rm imagebuilder.tar.zst && \
    mv openwrt-imagebuilder-* imagebuilder && \
    ln -s ${BUILDER_HOME}/imagebuilder ${BUILDER_HOME}/openwrt

# Create SSH directory
RUN mkdir -p ${BUILDER_HOME}/.ssh && \
    chmod 700 ${BUILDER_HOME}/.ssh

# Create packages metadata directory
RUN mkdir -p ${BUILDER_HOME}/packages

# Download nodewatcher-agent packages from GitHub releases
# These packages are built by GitHub Actions in valentt/nodewatcher-agent
ARG NODEWATCHER_AGENT_VERSION=latest
RUN mkdir -p ${BUILDER_HOME}/imagebuilder/packages && \
    cd ${BUILDER_HOME}/imagebuilder/packages && \
    RELEASE_URL="https://api.github.com/repos/valentt/nodewatcher-agent/releases/${NODEWATCHER_AGENT_VERSION}" && \
    echo "Fetching nodewatcher-agent packages from: ${RELEASE_URL}" && \
    (curl -sL "${RELEASE_URL}" | grep -o '"browser_download_url": "[^"]*\.ipk"' | cut -d'"' -f4 | xargs -I {} wget -q {} 2>/dev/null || \
     echo "Note: nodewatcher-agent packages not yet available, will use package filtering")

# Switch back to root for final setup
USER root

# Create symlink for nodewatcher compatibility (expects /builder/imagebuilder)
RUN mkdir -p /builder && ln -s ${BUILDER_HOME}/imagebuilder /builder/imagebuilder

# Create entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create nginx configuration for serving packages/metadata
RUN rm -f /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-enabled/builder

# Create metadata generation script
COPY generate-metadata.sh ${BUILDER_HOME}/generate-metadata.sh
RUN chmod +x ${BUILDER_HOME}/generate-metadata.sh && \
    chown ${BUILDER_USER}:${BUILDER_USER} ${BUILDER_HOME}/generate-metadata.sh

# Create supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/builder.conf

# Expose SSH and HTTP ports
EXPOSE 22 80

# Set working directory to imagebuilder
WORKDIR ${BUILDER_HOME}/imagebuilder

ENTRYPOINT ["/entrypoint.sh"]
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
