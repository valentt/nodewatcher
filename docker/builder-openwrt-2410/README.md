# OpenWrt 24.10 ImageBuilder for Nodewatcher

This directory contains a Dockerfile and supporting scripts to build an OpenWrt 24.10.x ImageBuilder container that is compatible with nodewatcher's firmware generation system.

## Building the Image

Build for specific target/subtarget:

```bash
# For ath79 (successor to ar71xx) - most common for older devices
docker build -t nodewatcher-builder-openwrt:24.10.3-ath79-generic \
  --build-arg OPENWRT_VERSION=24.10.0-rc3 \
  --build-arg TARGET=ath79 \
  --build-arg SUBTARGET=generic \
  .

# For x86_64 (virtual machines, PCs)
docker build -t nodewatcher-builder-openwrt:24.10.3-x86-64 \
  --build-arg OPENWRT_VERSION=24.10.0-rc3 \
  --build-arg TARGET=x86 \
  --build-arg SUBTARGET=64 \
  .

# For mediatek/filogic (newer MediaTek devices)
docker build -t nodewatcher-builder-openwrt:24.10.3-mediatek-filogic \
  --build-arg OPENWRT_VERSION=24.10.0-rc3 \
  --build-arg TARGET=mediatek \
  --build-arg SUBTARGET=filogic \
  .
```

## Running the Container

```bash
docker run -d \
  --name builder-openwrt-ath79 \
  -p 2222:22 \
  -p 8080:80 \
  -e BUILDER_PUBLIC_KEY="ssh-rsa AAAA... builder@nodewatcher" \
  nodewatcher-builder-openwrt:24.10.3-ath79-generic
```

## Registering with Nodewatcher

1. Access the Django admin at http://localhost:8000/admin/
2. Navigate to Generator > Builders
3. Add a new builder with:
   - Platform: openwrt
   - Architecture: ath79 (or your target)
   - Host: builder-openwrt-ath79 (container name)
   - Private key: (corresponding SSH private key)
4. The version will be auto-detected from the builder's metadata

## Architecture Notes

### Target Migration from ar71xx to ath79

OpenWrt has migrated from `ar71xx` to `ath79` target. Most devices that were on ar71xx are now on ath79. You may need to update device definitions in nodewatcher to reflect this change.

### Common Targets in OpenWrt 24.10

| Target | Subtarget | Description |
|--------|-----------|-------------|
| ath79 | generic | Atheros AR7xxx/AR9xxx (most TP-Link, Ubiquiti) |
| ath79 | nand | Atheros with NAND flash |
| x86 | 64 | x86_64 PCs and VMs |
| ramips | mt7621 | MediaTek MT7621 (many modern routers) |
| mediatek | filogic | Newer MediaTek WiFi 6/6E devices |
| ipq40xx | generic | Qualcomm IPQ40xx |

## Verifying the Builder

Test SSH connectivity:
```bash
ssh -p 2222 -i /path/to/private_key builder@localhost
```

Test HTTP metadata:
```bash
curl http://localhost:8080/metadata
```

## Troubleshooting

### Build fails with "No rule to make target"
The device profile may have changed in OpenWrt 24.10. Check available profiles:
```bash
docker exec -it builder-openwrt-ath79 make info
```

### SSH connection refused
Check that BUILDER_PUBLIC_KEY environment variable is set correctly.

### Metadata not generated
Check logs:
```bash
docker logs builder-openwrt-ath79
```
