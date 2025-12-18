#!/bin/bash
set -e

BUILDER_USER="${BUILDER_USER:-builder}"
BUILDER_HOME="${BUILDER_HOME:-/home/builder}"

# Setup SSH authorized keys from environment variable
if [ -n "${BUILDER_PUBLIC_KEY}" ]; then
    echo "Setting up SSH public key..."
    echo "${BUILDER_PUBLIC_KEY}" > ${BUILDER_HOME}/.ssh/authorized_keys
    chmod 600 ${BUILDER_HOME}/.ssh/authorized_keys
    chown ${BUILDER_USER}:${BUILDER_USER} ${BUILDER_HOME}/.ssh/authorized_keys
fi

# Generate metadata for nodewatcher
echo "Generating package metadata..."
su - ${BUILDER_USER} -c "${BUILDER_HOME}/generate-metadata.sh"

# Ensure proper ownership
chown -R ${BUILDER_USER}:${BUILDER_USER} ${BUILDER_HOME}

# Execute the main command
exec "$@"
