# OpenWrt 24.10 Builder Infrastructure Fixes

**Date:** 2024-12-19
**Commit:** e94711c2
**Branch:** feature/add-popular-freifunk-devices

## Summary

This document details the fixes made to enable OpenWrt 24.10 firmware generation for ath79 target devices (specifically TP-Link CPE210 v2) in the nodewatcher platform.

## Problems Identified and Solutions

### 1. Metadata Generation Errors

**Problem:** The builder metadata was returning incorrect values:
- `architecture`: returned `mips_24kc` instead of `ath79`
- `version`: returned empty string instead of `24.10.0`

**Root Cause:**
- The `generate-metadata.sh` script was reading `CONFIG_TARGET_ARCH_PACKAGES` which contains the CPU architecture (`mips_24kc`), not the target name (`ath79`)
- The `CONFIG_VERSION_NUMBER` field is empty in OpenWrt 24.10's ImageBuilder

**Solution:** Modified `generate-metadata.sh`:
```bash
# Use TARGET as architecture (nodewatcher uses target name, not CPU arch)
ARCH="${TARGET}"

# Extract version from CONFIG_VERSION_REPO URL if CONFIG_VERSION_NUMBER is empty
if [ -z "${VERSION}" ]; then
    VERSION=$(grep 'CONFIG_VERSION_REPO=' "${IMAGEBUILDER_DIR}/.config" | \
              grep -oP 'releases/\K[^/"]+' || echo "")
fi
```

**File:** `docker/builder-openwrt-2410/generate-metadata.sh`

---

### 2. Environment Variables Not Passed to Metadata Script

**Problem:** When running `su - builder -c "generate-metadata.sh"`, environment variables like `TARGET`, `SUBTARGET`, and `OPENWRT_VERSION` were not available.

**Root Cause:** The `su -` command creates a new login shell that doesn't inherit the parent process's environment.

**Solution:** Explicitly pass environment variables in the command:
```bash
su - ${BUILDER_USER} -c "TARGET=${TARGET:-ath79} SUBTARGET=${SUBTARGET:-generic} \
    OPENWRT_VERSION=${OPENWRT_VERSION:-24.10.0} ${BUILDER_HOME}/generate-metadata.sh"
```

**File:** `docker/builder-openwrt-2410/entrypoint.sh`

---

### 3. SSH Authentication Failures

**Problem:** SSH connections from the generator to the builder failed with "Authentication failed" errors.

**Root Cause:** Modern OpenSSH servers (Debian Bookworm) disable legacy `ssh-rsa` algorithm by default. The nodewatcher generator uses paramiko with `disabled_algorithms={'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256']}`, forcing the use of legacy `ssh-rsa`.

**Solution:** Enable legacy ssh-rsa in the builder's sshd_config:
```bash
if ! grep -q "PubkeyAcceptedAlgorithms" /etc/ssh/sshd_config; then
    echo "PubkeyAcceptedAlgorithms +ssh-rsa" >> /etc/ssh/sshd_config
fi
```

**File:** `docker/builder-openwrt-2410/entrypoint.sh`

---

### 4. SSH Key Mismatch

**Problem:** The public key in docker-compose.yml didn't match the private key stored in the database.

**Solution:** Updated `BUILDER_PUBLIC_KEY` in docker-compose.yml to match the stored private key.

**File:** `docker-compose.yml`

---

### 5. Firmware Output Files Not Found

**Problem:** Build completed successfully but files couldn't be extracted. Error: `Output file '*-ath79-generic-tplink_cpe210-v2-squashfs-factory.bin' not found!`

**Root Cause:** OpenWrt 24.10 uses a different output directory structure:
- **Old structure:** `bin/<target>/<files>`
- **New structure:** `bin/targets/<target>/<subtarget>/<files>`

The `extract_files` method only searched one level deep.

**Solution:** Added recursive file search method:
```python
def _find_files_recursive(self, base_dir, max_depth=4):
    """Recursively find all files in directory up to max_depth."""
    results = []

    def _scan(current_path, depth):
        if depth > max_depth:
            return
        try:
            items = self._builder.list_dir(current_path)
        except IOError:
            return

        for item in items:
            item_path = os.path.join(current_path, item)
            if '.' in item and not item.startswith('.'):
                results.append((current_path, item))
            else:
                _scan(item_path, depth + 1)

    _scan(base_dir, 0)
    return results
```

**File:** `nodewatcher/modules/platforms/openwrt/builder.py`

---

### 6. ImageBuilder Path Mismatch

**Problem:** Nodewatcher expects the ImageBuilder at `/builder/imagebuilder`, but the container has it at `/home/builder/imagebuilder`.

**Solution:** Added symlink in Dockerfile:
```dockerfile
RUN mkdir -p /builder && ln -s ${BUILDER_HOME}/imagebuilder /builder/imagebuilder
```

**File:** `docker/builder-openwrt-2410/Dockerfile`

---

### 7. Docker Container Startup Issues

**Problem:** The web container was failing to start with "no job control" errors.

**Root Cause:** The `scripts/docker-run` script used `-i` (interactive) flag which requires a TTY.

**Solution:** Removed the `-i` flag:
```bash
#!/bin/bash
exec /bin/bash -c "$*"
```

**File:** `scripts/docker-run`

---

## Files Modified

| File | Changes |
|------|---------|
| `.gitignore` | Added exclusions for binary images, local scripts |
| `docker-compose.yml` | Removed obsolete builders, updated SSH public key |
| `docker/builder-openwrt-2410/Dockerfile` | Added /builder/imagebuilder symlink |
| `docker/builder-openwrt-2410/entrypoint.sh` | SSH RSA support, env var passing |
| `docker/builder-openwrt-2410/generate-metadata.sh` | Fixed architecture and version extraction |
| `nodewatcher/modules/platforms/openwrt/builder.py` | Recursive file search for new directory structure |
| `scripts/docker-run` | Removed -i flag |

## Testing Results

### Successful Firmware Build

**Device:** TP-Link CPE210 v2
**Target:** ath79/generic
**OpenWrt Version:** 24.10.0
**Build UUID:** 86f67eb6-ab21-45cd-afdf-b2bb27465e4a

**Generated Files:**

| File | Size | MD5 Checksum |
|------|------|--------------|
| Osijek-Mestrovic-v24100-openwrt-24.10.0-ath79-generic-tplink_cpe210-v2-squashfs-factory.bin | 6.5 MB | c42d54d521312382ed8588fe2152a1f1 |
| Osijek-Mestrovic-v24100-openwrt-24.10.0-ath79-generic-tplink_cpe210-v2-squashfs-sysupgrade.bin | 7.4 MB | d0eec93666b0124b68efaf49997dfdb3 |
| manifest.json | 632 B | - |

## Known Limitations

### Custom Packages Not Available

The following nodewatcher-specific packages are not available in standard OpenWrt repositories and must be built separately:

- `nodewatcher-agent`
- `nodewatcher-agent-mod-general`
- `nodewatcher-agent-mod-resources`
- `nodewatcher-agent-mod-interfaces`
- `nodewatcher-agent-mod-wireless`
- `nodewatcher-agent-mod-clients`
- `nodewatcher-watchdog`
- `nodeupgrade`
- `identity-pubkey`

The current build uses only standard OpenWrt packages (`ip`, `qos-scripts`). To include the full nodewatcher monitoring stack, these packages need to be compiled and added to the ImageBuilder's package repository.

## Recommendations

1. **Build Custom Packages:** Set up a package build pipeline for nodewatcher-agent and related packages compatible with OpenWrt 24.10.

2. **Update Device Profiles:** Review and update device profiles in `nodewatcher/modules/devices/` to ensure file patterns match OpenWrt 24.10 naming conventions.

3. **Add More Targets:** Consider adding additional target/subtarget combinations (e.g., ramips/mt7621, mediatek/filogic) for broader device support.

4. **Automate Metadata Refresh:** Consider adding periodic metadata refresh to detect builder changes automatically.
