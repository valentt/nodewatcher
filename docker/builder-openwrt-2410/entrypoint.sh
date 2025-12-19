#!/bin/bash
set -e

BUILDER_USER="${BUILDER_USER:-builder}"
BUILDER_HOME="${BUILDER_HOME:-/home/builder}"

# Enable legacy ssh-rsa algorithm (required for paramiko compatibility)
if ! grep -q "PubkeyAcceptedAlgorithms" /etc/ssh/sshd_config; then
    echo "Enabling legacy ssh-rsa algorithm..."
    echo "PubkeyAcceptedAlgorithms +ssh-rsa" >> /etc/ssh/sshd_config
fi

# Setup SSH authorized keys from environment variable
if [ -n "${BUILDER_PUBLIC_KEY}" ]; then
    echo "Setting up SSH public key..."
    echo "${BUILDER_PUBLIC_KEY}" > ${BUILDER_HOME}/.ssh/authorized_keys
    chmod 600 ${BUILDER_HOME}/.ssh/authorized_keys
    chown ${BUILDER_USER}:${BUILDER_USER} ${BUILDER_HOME}/.ssh/authorized_keys
fi

# Generate metadata for nodewatcher
echo "Generating package metadata..."
# Export environment variables needed by the metadata script
export TARGET SUBTARGET OPENWRT_VERSION
su - ${BUILDER_USER} -c "TARGET=${TARGET:-ath79} SUBTARGET=${SUBTARGET:-generic} OPENWRT_VERSION=${OPENWRT_VERSION:-24.10.0} ${BUILDER_HOME}/generate-metadata.sh"

# Ensure proper ownership
chown -R ${BUILDER_USER}:${BUILDER_USER} ${BUILDER_HOME}

# Execute the main command
exec "$@"
