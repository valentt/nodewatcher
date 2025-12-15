# Feature Ticket #008: WireGuard VPN Support

**Status:** Planned
**Priority:** High
**Type:** Feature Request
**Created:** 2024-12-14

---

## Summary

Add WireGuard as an alternative VPN option alongside the existing Tunneldigger. WireGuard is modern, fast, and cryptographically sound - ideal for mesh networks.

---

## Why WireGuard?

### Comparison: Tunneldigger vs WireGuard

| Feature | Tunneldigger | WireGuard |
|---------|--------------|-----------|
| **Speed** | Good | Excellent (kernel-level) |
| **Latency** | Higher | Very low |
| **CPU Usage** | Moderate | Minimal |
| **Configuration** | Complex | Simple |
| **Encryption** | None (L2TP only) | ChaCha20, Curve25519 |
| **Code Size** | Large | ~4,000 lines |
| **OpenWrt Support** | Package | Built-in (21.02+) |
| **NAT Traversal** | Yes | Yes (with keepalive) |
| **Roaming** | Limited | Excellent |

### Architectural Difference: L2 vs L3

| | Tunneldigger | WireGuard |
|--|--------------|-----------|
| **OSI Layer** | L2 (Bridge) | L3 (Routing) |
| **Passes** | Ethernet frames | IP packets only |
| **Broadcast** | Yes (floods) | No |
| **ARP** | Passes through | Does not pass |
| **Best for** | Flat LAN networks | Routed mesh networks |

**Tunneldigger (L2 bridge):**
- Network appears as one big LAN segment
- Broadcast traffic passes through (can be problem at scale)
- Simpler for small "flat" networks

**WireGuard (L3 routing):**
- Requires routing protocol (Babel, OLSR, etc.)
- No broadcast flooding over tunnel
- More scalable for larger networks
- Cleaner network segmentation

### Use Cases

| Scenario | Recommended VPN |
|----------|-----------------|
| Legacy devices, older OpenWrt | Tunneldigger |
| Modern mesh, low latency needed | WireGuard |
| Mobile nodes (roaming) | WireGuard |
| High throughput links | WireGuard |
| Simple setup for volunteers | WireGuard |
| **Apex/backbone (site-to-site)** | **WireGuard** |
| **Connecting distant mesh sites** | **WireGuard** |

### Apex Networks: Connecting Distant Mesh Sites

For connecting geographically separated mesh networks (apex/backbone), **WireGuard is strongly recommended**:

```
[Zagreb Mesh]  ←──WireGuard──→  [Split Mesh]  ←──WireGuard──→  [Rijeka Mesh]
     │                               │                              │
   Babel                           Babel                          Babel
     │                               │                              │
 (local traffic                 (local traffic                (local traffic
  stays local)                   stays local)                  stays local)
```

**Why WireGuard for apex networks:**

| Factor | L2 Bridge (Tunneldigger) | L3 Routing (WireGuard) |
|--------|--------------------------|------------------------|
| WAN latency impact | Broadcasts wait for all sites | Only routed traffic |
| Bandwidth usage | Broadcast flooding wastes WAN | Efficient utilization |
| Scalability | Poor (O(n²) broadcast) | Good (routing table) |
| Babel/OLSR | Works but sees "slow" links | Native support |
| Link cost control | Difficult | Babel calculates automatically |
| Local traffic | May traverse WAN unnecessarily | Stays local |

**Key benefit:** Babel routing protocol automatically calculates that WireGuard links over WAN have higher cost (latency), so local traffic stays local and only inter-site traffic crosses the VPN.

### Apex Protocol Integration

For networks running **Apex Core** (enhanced Babel with native mobility), WireGuard is the **natural choice** for site-to-site tunnels:

```
[Site A - Apex Mesh]                           [Site B - Apex Mesh]
       │                                              │
    Apex Core                                      Apex Core
    (DAT, CMR)                                     (DAT, CMR)
       │                                              │
       └───────── WireGuard Tunnel ──────────────────┘
                         │
                 Apex sees as "tunnel" interface
                 RTT penalty applied automatically
                 Cost = 96 + RTT_penalty
```

**Why WireGuard + Apex work perfectly together:**

| Factor | Tunneldigger | WireGuard |
|--------|--------------|-----------|
| OSI Layer match | L2 vs Apex L3 (mismatch) | **L3 = L3 (perfect)** |
| Apex RTT penalty | Works | **Works optimally** |
| DSO (Apex Omega) | Not designed for | **Designed for WireGuard** |
| Encryption | None | **ChaCha20** |
| Overhead | L2 bridging overhead | **Minimal L3** |

**Apex interface cost for tunnels** (from Apex docs):
```
interface_cost = 96 + rtt_penalty

Where rtt_penalty = max_rtt_penalty × (rtt - rtt_min) / (rtt_max - rtt_min)

Default: rtt_min=10ms, rtt_max=120ms, max_rtt_penalty=96
```

This means Apex automatically prefers local wireless paths over WireGuard tunnels when both exist, but uses tunnels when they're the best path.

**DSO (Dynamic Secure Overlay)** - Apex Omega module specifically designed for WireGuard:
- Automatic tunnel management
- Key rotation
- Peer discovery
- Integration with Apex routing

---

## Proposed Architecture

### Server Types (Admin Configurable)

```
VPN Server Types:
┌─────────────────────────────────────────────────────────────┐
│  ○ Tunneldigger Server (existing)                          │
│    L2TP-based tunneling, compatible with older devices      │
│                                                             │
│  ○ WireGuard Server (NEW)                                  │
│    Modern, fast, kernel-level VPN                          │
│    Requires: OpenWrt 21.02+ or Linux 5.6+                  │
└─────────────────────────────────────────────────────────────┘
```

### Node Configuration (Per Interface)

```
VPN Interface Configuration:
┌─────────────────────────────────────────────────────────────┐
│  Interface Type: [WireGuard ▼]                             │
│                                                             │
│  Server: [Zagreb Hub 1 (WireGuard) ▼]                      │
│                                                             │
│  ┌─ Auto-generated (read-only) ─────────────────────────┐  │
│  │ Public Key: abc123...xyz                              │  │
│  │ Assigned IP: 10.55.0.42/32                           │  │
│  │ Endpoint: vpn1.example.net:51820                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ☑ Persistent Keepalive (for NAT traversal)               │
│    Interval: [25] seconds                                  │
│                                                             │
│  Routing Protocol: [Babel ▼]                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Models

### New Models (following Tunneldigger pattern)

```python
# nodewatcher/modules/vpn/wireguard/models.py

class WireguardServer(polymorphic_models.PolymorphicModel):
    """WireGuard VPN server/hub configuration."""

    name = models.CharField(max_length=100)
    # Server's public key
    public_key = models.CharField(max_length=44)  # Base64 encoded
    # Endpoint address
    address = ip_models.IPAddressField(host_required=True)
    port = models.IntegerField(default=51820, validators=[PortNumberValidator()])
    # Network for client allocation
    network = ip_models.IPNetworkField()
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "WireGuard Server"


class PerProjectWireguardServer(WireguardServer):
    """WireGuard server assigned to specific project."""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='wireguard_servers'
    )


class WireguardInterfaceConfig(cgm_models.InterfaceConfig, cgm_models.RoutableInterface):
    """WireGuard interface on a node (client side)."""

    # Auto-generated keypair stored securely
    private_key = models.CharField(max_length=44)  # Encrypted in DB
    public_key = models.CharField(max_length=44)

    # Server connection
    server = registry.fields.ModelRegistryChoiceField(WireguardServer)

    # Assigned IP from server's pool
    address = ip_models.IPAddressField(host_required=True)

    # Optional settings
    persistent_keepalive = models.IntegerField(default=25)  # seconds, 0 to disable

    # Uplink interface (for routing)
    uplink_interface = registry.fields.ReferenceChoiceField(
        cgm_models.InterfaceConfig,
        related_name='wireguard_interfaces'
    )

    class Meta:
        registry_name = "WireGuard Interface"


class WireguardBrokerConfig(cgm_models.PackageConfig, cgm_models.RoutableInterface):
    """WireGuard broker/server running on a node."""

    port = models.IntegerField(default=51820)
    private_key = models.CharField(max_length=44)  # Encrypted
    public_key = models.CharField(max_length=44)

    # Network for peers
    network = ip_models.IPNetworkField()

    class Meta:
        registry_name = "WireGuard Broker"
```

### Key Management

```python
# nodewatcher/modules/vpn/wireguard/crypto.py

import subprocess

def generate_keypair():
    """Generate WireGuard keypair."""
    private_key = subprocess.check_output(['wg', 'genkey']).decode().strip()
    public_key = subprocess.check_output(
        ['wg', 'pubkey'],
        input=private_key.encode()
    ).decode().strip()
    return private_key, public_key

def generate_preshared_key():
    """Generate optional preshared key for extra security."""
    return subprocess.check_output(['wg', 'genpsk']).decode().strip()
```

---

## CGM Configuration Generation

```python
# nodewatcher/modules/vpn/wireguard/cgm.py

@cgm_base.register_platform_module('openwrt', 100)
def wireguard(node, cfg):
    """Generate WireGuard client configuration for OpenWrt."""

    for idx, interface in enumerate(node.config.core.interfaces(onlyclass=WireguardInterfaceConfig)):
        if not interface.enabled:
            continue

        iface_name = f'wg{idx}'

        # Network interface
        wg_iface = cfg.network.add(interface=iface_name)
        wg_iface.proto = 'wireguard'
        wg_iface.private_key = interface.private_key
        wg_iface.addresses = [str(interface.address)]

        # Peer (server) configuration
        peer = cfg.network.add(**{f'wireguard_{iface_name}': interface.server.name})
        peer.public_key = interface.server.public_key
        peer.endpoint_host = str(interface.server.address)
        peer.endpoint_port = interface.server.port
        peer.persistent_keepalive = interface.persistent_keepalive
        peer.allowed_ips = ['0.0.0.0/0', '::/0']  # Or specific routes

        # Firewall zone
        cfg.firewall.add_zone_interface('mesh', iface_name)
```

Generated UCI configuration example:

```
# /etc/config/network
config interface 'wg0'
    option proto 'wireguard'
    option private_key 'PRIVATE_KEY_HERE'
    list addresses '10.55.0.42/32'

config wireguard_wg0 'peer_hub1'
    option public_key 'SERVER_PUBLIC_KEY'
    option endpoint_host 'vpn1.example.net'
    option endpoint_port '51820'
    option persistent_keepalive '25'
    list allowed_ips '10.55.0.0/21'
```

---

## Admin Interface

### Server Management

```
┌─────────────────────────────────────────────────────────────┐
│ VPN Servers                                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Type: [All ▼]  Project: [All ▼]  Status: [All ▼]  [Filter] │
│                                                             │
│ ┌───────────────────────────────────────────────────────┐  │
│ │ Name          │ Type        │ Project │ Peers │ Status│  │
│ ├───────────────────────────────────────────────────────┤  │
│ │ Zagreb Hub 1  │ WireGuard   │ Zagreb  │ 45    │ ● Up  │  │
│ │ Zagreb Hub 2  │ Tunneldigger│ Zagreb  │ 23    │ ● Up  │  │
│ │ Split Hub     │ WireGuard   │ Split   │ 12    │ ● Up  │  │
│ │ Rijeka Old    │ Tunneldigger│ Rijeka  │ 8     │ ○ Down│  │
│ └───────────────────────────────────────────────────────┘  │
│                                                             │
│ [+ Add WireGuard Server] [+ Add Tunneldigger Server]       │
└─────────────────────────────────────────────────────────────┘
```

### Add WireGuard Server Form

```
┌─────────────────────────────────────────────────────────────┐
│ Add WireGuard Server                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Name: [Zagreb WireGuard Hub_______________]                │
│                                                             │
│ Endpoint Address: [vpn.zagreb.example.net_]                │
│ Port: [51820____]                                          │
│                                                             │
│ ┌─ Server Keys ─────────────────────────────────────────┐  │
│ │ ○ Generate new keypair                                 │  │
│ │ ○ Enter existing keys:                                 │  │
│ │   Public Key:  [________________________________]      │  │
│ │   Private Key: [________________________________]      │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                             │
│ Client IP Pool: [10.55.0.0/24_____________]                │
│                                                             │
│ Project: [Zagreb Community ▼] (or Global)                  │
│                                                             │
│ ☑ Enabled                                                  │
│                                                             │
│                              [Cancel] [Save WireGuard Server]│
└─────────────────────────────────────────────────────────────┘
```

---

## Migration Path

### For Existing Networks

1. **Add WireGuard server** alongside existing Tunneldigger
2. **Migrate nodes gradually** - no big bang
3. **Keep both running** during transition
4. **Deprecate Tunneldigger** when all nodes migrated (optional)

### Node Upgrade Flow

```
Node currently using Tunneldigger:
┌─────────────────────────────────────────────────────────────┐
│ VPN Configuration                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Current: Tunneldigger → Zagreb Hub 2                       │
│                                                             │
│ ⚠️ WireGuard is available for this project!                │
│    Benefits: Lower latency, better performance             │
│                                                             │
│    [Upgrade to WireGuard] [Keep Tunneldigger]              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Core WireGuard Support
- [ ] Create `nodewatcher/modules/vpn/wireguard/` module
- [ ] Implement WireguardServer model (polymorphic)
- [ ] Implement WireguardInterfaceConfig model
- [ ] Basic admin interface for servers
- [ ] CGM configuration generation for OpenWrt
- [ ] Key generation utilities

### Phase 2: Integration
- [ ] Per-project server support
- [ ] Babel routing integration
- [ ] QoS support on WireGuard interfaces
- [ ] Form defaults (auto-configure WG on uplink)
- [ ] Monitoring/processors for WG interfaces

### Phase 3: Management Features
- [ ] Peer status monitoring
- [ ] Bandwidth statistics
- [ ] Key rotation support
- [ ] Bulk migration tool (TD → WG)

### Phase 4: Advanced
- [ ] WireGuard broker support (node as server)
- [ ] Multi-hop WireGuard
- [ ] Site-to-site WireGuard links
- [ ] IPv6 support

---

## Security Considerations

1. **Private keys** - Store encrypted in database, never expose in admin
2. **Key rotation** - Plan for periodic key rotation
3. **Preshared keys** - Optional additional layer of security
4. **Endpoint privacy** - Consider hiding server IPs from non-admins
5. **Audit logging** - Log all key generation and configuration changes

---

## Performance Notes

### Can Encryption Be Disabled?

**No.** WireGuard encryption is fundamental to the protocol, not optional. Every packet must be encrypted (ChaCha20) and authenticated (Poly1305).

However, **this is rarely a problem** because WireGuard's crypto is extremely efficient:

| Hardware | WireGuard Throughput | Bottleneck |
|----------|---------------------|------------|
| Modern x86 (AES-NI) | 5-10 Gbps | Not crypto |
| Raspberry Pi 4 | 500+ Mbps | CPU general |
| OpenWrt (MT7621) | 200-400 Mbps | CPU general |
| Old router (AR71xx) | 30-50 Mbps | May be crypto |

### WireGuard vs Tunneldigger Performance

**WireGuard is faster DESPITE encryption:**

| Aspect | Tunneldigger | WireGuard |
|--------|--------------|-----------|
| Encryption | None | ChaCha20 |
| Processing | Userspace daemon | **Kernel native** |
| Context switches | Many | **Few** |
| Typical throughput | ~100 Mbps | **~300 Mbps** |

The kernel-native implementation more than compensates for crypto overhead.

### Alternatives for Zero-Encryption (Not Recommended)

If encryption is truly a bottleneck on very old hardware:

| Option | NAT Traversal | Management | Use Case |
|--------|---------------|------------|----------|
| GRE/IPIP | **No** | Manual | Point-to-point, static IPs |
| VXLAN | Limited | Manual | Data center |
| FOU | **No** | Manual | Experimental |

**Recommendation:** Use WireGuard. Encryption overhead is negligible on any hardware capable of useful throughput.

---

## Historical Context: Why Tunneldigger Existed

### What Tunneldigger Is

Tunneldigger is a **management layer on top of L2TP**, developed by wlan slovenija (~2012):

```
Tunneldigger = L2TP + Broker architecture + NAT traversal + Auto-reconnect
```

### Why It Was Created

In 2012, available options were limited:

| Option | Problem |
|--------|---------|
| Raw L2TP | Complex configuration, no management |
| OpenVPN (tap) | CPU intensive, slow on cheap routers |
| GRE | No NAT traversal |
| IPsec | Complex, CPU intensive |

WireGuard didn't exist until 2018.

### The Architectural Mismatch

**Using L2 tunnel (Tunneldigger) with L3 routing (Babel/Apex) was never optimal:**

```
L2 tunnel overhead:
[IP] → [Ethernet Frame] → [L2TP] → [UDP] → [IP] → Internet
              ↑
        Unnecessary for L3 routing
```

vs.

```
L3 tunnel (WireGuard):
[IP] → [WireGuard] → [UDP] → [IP] → Internet
         ↑
    Direct, encrypted
```

### Security Problem

**Tunneldigger has NO encryption.** All traffic is plaintext. This was "acceptable" for internal community networks in 2012, but is unacceptable today.

### Summary: Tunneldigger vs WireGuard

| Aspect | Tunneldigger | WireGuard |
|--------|--------------|-----------|
| Year | 2012 | 2018 |
| Layer | L2 (bridge) | L3 (routing) |
| Encryption | **None** | ChaCha20 |
| Performance | Good | **Better** |
| NAT traversal | Yes | Yes |
| Apex compatibility | Works (mismatch) | **Native (DSO)** |
| Status | Legacy | **Modern standard** |

**Conclusion:** Tunneldigger was a pragmatic solution for its time. WireGuard is the correct solution today.

---

## File Structure

```
nodewatcher/modules/vpn/wireguard/
├── __init__.py
├── apps.py
├── models.py          # WireguardServer, WireguardInterfaceConfig, etc.
├── admin.py           # Django admin registration
├── forms.py           # Form customization
├── cgm.py             # OpenWrt configuration generation
├── crypto.py          # Key generation utilities
├── processors.py      # Monitoring processors
├── signals.py         # Signal definitions
├── defaults.py        # Form default handlers
└── migrations/
    └── 0001_initial.py
```

---

## Success Metrics

- WireGuard available as option in node configuration
- < 5 minute setup time for new WireGuard server
- Successful coexistence with Tunneldigger
- Lower latency reported by users after migration
- No increase in support requests

---

## Related Documents

- #005 Local Sheriffs (sheriffs should be able to manage VPN servers for their area)
- #006 IP Pool Wizard (VPN clients need IPs from pool)
- #009 Tunneldigger Explained (historical context, why we're moving on)
- Apex Core Whitepaper (apex-core/docs/31 - Apex Core v1.5 Whitepaper.md)
- Apex Protocol Overview (apex-core/docs/01 - Protocol Overview.md)

---

## Notes

- WireGuard requires OpenWrt 21.02+ or newer kernel (5.6+)
- Consider fallback to Tunneldigger for older devices
- WireGuard uses UDP, ensure firewalls allow it
- Some ISPs block non-standard UDP ports, offer port 443 as option

