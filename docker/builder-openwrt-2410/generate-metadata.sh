#!/bin/bash
# Generate metadata.json for nodewatcher builder integration
# This script parses the ImageBuilder's package information and creates
# metadata in the format expected by nodewatcher.

BUILDER_HOME="${BUILDER_HOME:-/home/builder}"
IMAGEBUILDER_DIR="${BUILDER_HOME}/imagebuilder"
PACKAGES_DIR="${BUILDER_HOME}/packages"

# Ensure packages directory exists
mkdir -p "${PACKAGES_DIR}"

# Extract version from ImageBuilder
if [ -f "${IMAGEBUILDER_DIR}/.config" ]; then
    VERSION=$(grep CONFIG_VERSION_NUMBER "${IMAGEBUILDER_DIR}/.config" | cut -d'"' -f2)
else
    VERSION="${OPENWRT_VERSION:-unknown}"
fi

# Extract target information
TARGET="${TARGET:-unknown}"
SUBTARGET="${SUBTARGET:-generic}"

# Get architecture from ImageBuilder
if [ -f "${IMAGEBUILDER_DIR}/.config" ]; then
    ARCH=$(grep CONFIG_TARGET_ARCH_PACKAGES "${IMAGEBUILDER_DIR}/.config" | cut -d'"' -f2)
else
    ARCH="${TARGET}"
fi

echo "Generating metadata for OpenWrt ${VERSION} (${TARGET}/${SUBTARGET})..."

# Parse available packages
PACKAGES_JSON="[]"
if [ -d "${IMAGEBUILDER_DIR}/packages" ]; then
    PACKAGES_JSON=$(find "${IMAGEBUILDER_DIR}/packages" -name "*.ipk" -type f | while read pkg; do
        PKG_NAME=$(basename "$pkg" | sed 's/_.*//g')
        PKG_VERSION=$(basename "$pkg" | sed 's/^[^_]*_//; s/_[^_]*$//g')
        echo "{\"name\":\"${PKG_NAME}\",\"version\":\"${PKG_VERSION}\"}"
    done | jq -s '.')
fi

# Get available profiles
PROFILES_JSON="[]"
if [ -f "${IMAGEBUILDER_DIR}/.profiles.mk" ]; then
    PROFILES_JSON=$(grep "^PROFILE_NAME=" "${IMAGEBUILDER_DIR}/.profiles.mk" 2>/dev/null | while read line; do
        PROFILE=$(echo "$line" | sed 's/PROFILE_NAME=//g; s/"//g')
        echo "{\"name\":\"${PROFILE}\"}"
    done | jq -s '.' 2>/dev/null || echo "[]")
fi

# Alternative: parse from .config or profiles directory
if [ "$PROFILES_JSON" = "[]" ] && [ -d "${IMAGEBUILDER_DIR}/target/linux/${TARGET}/image" ]; then
    PROFILES_JSON=$(ls "${IMAGEBUILDER_DIR}/target/linux/${TARGET}/image"/*.mk 2>/dev/null | while read f; do
        grep "^define Device/" "$f" 2>/dev/null | sed 's/define Device\///g' | while read profile; do
            echo "{\"name\":\"${profile}\"}"
        done
    done | jq -s '.' 2>/dev/null || echo "[]")
fi

# Generate metadata.json
cat > "${PACKAGES_DIR}/metadata.json" << EOF
{
    "version": "${VERSION}",
    "platform": "openwrt",
    "architecture": "${ARCH}",
    "target": "${TARGET}",
    "subtarget": "${SUBTARGET}",
    "packages": ${PACKAGES_JSON:-[]},
    "profiles": ${PROFILES_JSON:-[]}
}
EOF

echo "Metadata generated at ${PACKAGES_DIR}/metadata.json"

# Also create a simple version file
echo "${VERSION}" > "${PACKAGES_DIR}/version"
