# Technical Note #009: Tunneldigger - History, Architecture, and Why We're Moving On

**Type:** Technical Documentation
**Created:** 2024-12-14
**Status:** Reference Document

---

## Executive Summary

Tunneldigger is an L2 (Layer 2) tunneling solution developed by wlan slovenija for community mesh networks. While it served its purpose well for over a decade, it's being superseded by WireGuard for modern deployments. This document explains what Tunneldigger is, why it was created, and why WireGuard is the better choice today.

---

## 1. What is Tunneldigger?

Tunneldigger is **not a new protocol** - it's a management layer built on top of Linux kernel L2TP:

```
┌─────────────────────────────────────────────────────────────┐
│                     TUNNELDIGGER                             │
├─────────────────────────────────────────────────────────────┤
│  • Broker/Client architecture                               │
│  • Automatic session management                             │
│  • NAT traversal (UDP encapsulation)                        │
│  • Automatic reconnection on failure                        │
│  • Simple configuration for mesh networks                   │
│  • Multiple MTU support (for path MTU discovery)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    L2TP (Linux Kernel)                       │
│              Layer 2 Tunneling Protocol                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         UDP/IP                               │
│                   (NAT traversal friendly)                   │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **Broker** | Central server that accepts client connections |
| **Client** | Runs on mesh nodes, connects to broker |
| **L2TP Session** | Kernel-level tunnel carrying Ethernet frames |
| **Bridge Interface** | Created on broker for each client |

---

## 2. Why Was Tunneldigger Created? (~2012)

### The Problem

Community mesh networks needed to connect nodes that couldn't reach each other via wireless:

```
[Node A]  ~~~wireless~~~  [Node B]
    │
    │ (no wireless path)
    │
    X  Can't reach  X ──────  [Node C behind NAT]
```

### Available Options in 2012

| Option | Why It Didn't Work |
|--------|-------------------|
| **Raw L2TP** | Complex configuration, no management layer |
| **OpenVPN (tap)** | CPU intensive (userspace + TLS), slow on cheap routers |
| **GRE/GRETAP** | No NAT traversal (IP protocol 47, blocked by most NATs) |
| **VXLAN** | Just released (Linux 3.7), designed for data centers |
| **IPsec** | Complex, CPU intensive, configuration nightmare |

### The Solution: Tunneldigger

wlan slovenija created Tunneldigger to provide:

1. **Broker Architecture** - One server handles hundreds of clients
2. **NAT Traversal** - UDP-based, works behind any home router
3. **Automatic Reconnection** - Handles flaky connections
4. **Simple Configuration** - Minimal setup for volunteers
5. **L2 Bridging** - Extends the mesh as one L2 segment

---

## 3. Technical Architecture

### Broker Side

```
┌─────────────────────────────────────────────────────────────┐
│                    TUNNELDIGGER BROKER                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Listening on UDP ports: 8942, 53, 123 (multiple for NAT)  │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Session 1   │  │ Session 2   │  │ Session 3   │        │
│  │ Client: A   │  │ Client: B   │  │ Client: C   │        │
│  │ l2tp1       │  │ l2tp2       │  │ l2tp3       │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │
│         └────────────────┼────────────────┘                │
│                          │                                  │
│                    ┌─────┴─────┐                           │
│                    │  Bridge   │                           │
│                    │   br0     │                           │
│                    └─────┬─────┘                           │
│                          │                                  │
│                    Mesh Network                             │
└─────────────────────────────────────────────────────────────┘
```

### Client Side

```
┌─────────────────────────────────────────────────────────────┐
│                   TUNNELDIGGER CLIENT                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Config:                                                    │
│    broker = vpn.example.net                                 │
│    ports = 8942, 53, 123                                    │
│    uuid = <unique-node-id>                                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              L2TP Session (kernel)                   │   │
│  │                     │                                │   │
│  │              ┌──────┴──────┐                        │   │
│  │              │   l2tp0     │  ← Virtual interface   │   │
│  │              └──────┬──────┘                        │   │
│  │                     │                                │   │
│  │              Babel/Apex routing                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Protocol Flow

```
1. Client sends UDP "hello" to broker
2. Broker responds, negotiates session parameters
3. L2TP session established in kernel
4. Ethernet frames flow through tunnel
5. Keepalives maintain NAT mappings
6. On failure: automatic reconnection with backoff
```

---

## 4. The Architectural Mismatch

### L2 Tunnel + L3 Routing = Unnecessary Overhead

```
Babel/Apex (L3 routing) + Tunneldigger (L2 tunnel):

[IP Packet]
    │
    ▼
[Ethernet Frame]      ← Added by L2 tunnel (14+ bytes overhead)
    │
    ▼
[L2TP Header]         ← Tunnel encapsulation
    │
    ▼
[UDP Header]
    │
    ▼
[IP Header]
    │
    ▼
─────── Internet ───────
```

vs.

```
Babel/Apex (L3 routing) + WireGuard (L3 tunnel):

[IP Packet]
    │
    ▼
[WireGuard Header]    ← Minimal encapsulation + encryption
    │
    ▼
[UDP Header]
    │
    ▼
[IP Header]
    │
    ▼
─────── Internet ───────
```

### Overhead Comparison

| Tunnel Type | Header Overhead | Encryption | MTU Impact |
|-------------|-----------------|------------|------------|
| Tunneldigger (L2TP) | ~26 bytes + Ethernet 14 bytes | **None** | -40 bytes |
| WireGuard | ~32 bytes | **ChaCha20** | -32 bytes |

**Tunneldigger has MORE overhead AND no encryption!**

---

## 5. Why L2 Tunneling Was Used

### Possible Historical Reasons

1. **BATMAN-adv Integration**
   - Some networks used BATMAN-adv (L2 mesh) + Babel (L3)
   - L2 tunnel made sense for extending BATMAN-adv domain

2. **Bridge-based Architecture**
   - Early mesh designs bridged everything to one L2 segment
   - Simpler mental model: "one big switch"

3. **DHCP Distribution**
   - L2 allows DHCP broadcasts
   - Clients could get IPs from central DHCP server

4. **"It Works, Don't Touch It"**
   - Once deployed, changing tunnel technology is disruptive
   - Pragmatic: working > optimal

### What L2 Tunneling Actually Provides

| Feature | Needed for L3 Routing? |
|---------|----------------------|
| Ethernet frame transport | **No** |
| Broadcast/multicast pass-through | **No** (routing handles this) |
| ARP pass-through | **No** (each site has own ARP) |
| Same L2 segment illusion | **No** |

**For pure L3 routing (Babel, Apex), none of L2's features are needed.**

---

## 6. Security Concerns

### Tunneldigger Has No Encryption

```
┌─────────────────────────────────────────────────────────────┐
│                    ⚠️  WARNING                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Tunneldigger traffic is sent IN PLAINTEXT                  │
│                                                             │
│  Anyone on the path can:                                    │
│    • Read all traffic                                       │
│    • See which nodes are communicating                      │
│    • Potentially inject packets                             │
│                                                             │
│  This was "acceptable" for:                                 │
│    • Internal community traffic                             │
│    • Non-sensitive data                                     │
│    • Trust-based community networks                         │
│                                                             │
│  This is NOT acceptable for:                                │
│    • Any sensitive data                                     │
│    • Modern security requirements                           │
│    • Compliance-required networks                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### WireGuard Security

| Aspect | Tunneldigger | WireGuard |
|--------|--------------|-----------|
| Encryption | **None** | ChaCha20-Poly1305 |
| Key Exchange | N/A | Curve25519 |
| Authentication | UUID only | Cryptographic keys |
| Forward Secrecy | **No** | Yes |
| Attack Surface | Large (L2TP) | Minimal (~4000 LOC) |

---

## 7. Performance Comparison

### CPU Usage

| Operation | Tunneldigger | WireGuard |
|-----------|--------------|-----------|
| Encryption | N/A | ~3% (with AES-NI) |
| Encapsulation | Userspace daemon | **Kernel native** |
| Context Switches | Many (userspace) | **Few (kernel)** |

### Throughput (typical)

| Hardware | Tunneldigger | WireGuard |
|----------|--------------|-----------|
| Raspberry Pi 3 | ~100 Mbps | ~300 Mbps |
| x86 (modern) | ~500 Mbps | ~1+ Gbps |
| OpenWrt router | ~50 Mbps | ~100-200 Mbps |

**WireGuard is faster DESPITE doing encryption!**

---

## 8. Migration Path: Tunneldigger → WireGuard

### Phase 1: Parallel Operation

```
┌─────────────────────────────────────────────────────────────┐
│                     TRANSITION PERIOD                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Node A] ──── Tunneldigger ──── [Broker]                  │
│     │                               │                       │
│     └─────── WireGuard ─────────────┘                      │
│            (new, preferred)                                 │
│                                                             │
│  Routing protocol (Babel/Apex) sees both paths             │
│  Prefers WireGuard due to better metrics                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Gradual Migration

1. Deploy WireGuard server alongside Tunneldigger broker
2. Update nodes one by one to support WireGuard
3. Both tunnels active - routing chooses best path
4. Monitor for issues

### Phase 3: Tunneldigger Deprecation

1. All nodes on WireGuard
2. Disable Tunneldigger broker
3. Remove Tunneldigger packages from firmware
4. Archive documentation

---

## 9. When to Still Use Tunneldigger

### Valid Use Cases (Legacy)

| Scenario | Why Tunneldigger |
|----------|------------------|
| Very old OpenWrt (< 18.06) | No WireGuard support |
| Devices without crypto acceleration | WireGuard might be slow |
| Existing stable deployment | "If it ain't broke..." |
| L2 bridging actually needed | Rare, but possible |

### When NOT to Use Tunneldigger

- New deployments → **Use WireGuard**
- Security is a concern → **Use WireGuard**
- Performance matters → **Use WireGuard**
- Modern OpenWrt (21.02+) → **Use WireGuard**
- Apex protocol deployment → **Use WireGuard** (DSO module)

---

## 10. Conclusion

### Tunneldigger Was...

- **Pragmatic** - Solved a real problem with available tools
- **Community-built** - By wlan slovenija, for mesh networks
- **Good enough** - Worked reliably for 10+ years

### But Today...

- **Architecturally wrong** - L2 tunnel for L3 routing
- **Insecure** - No encryption in 2024 is unacceptable
- **Slower** - Despite no encryption overhead
- **Obsolete** - WireGuard does everything better

### The Future

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Tunneldigger (2012-2024)                                 │
│   ════════════════════════                                 │
│   Thank you for your service.                              │
│   Time to retire.                                          │
│                                                             │
│   ──────────────────────────────────────────────────────   │
│                                                             │
│   WireGuard (2018+)                                        │
│   ═════════════════                                        │
│   The future of mesh VPN connectivity.                     │
│                                                             │
│   • L3 native (matches Babel/Apex)                         │
│   • Encrypted by default                                   │
│   • Faster than unencrypted alternatives                   │
│   • Kernel-native on Linux and OpenWrt                     │
│   • Apex DSO module designed for it                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## References

- [Tunneldigger GitHub](https://github.com/wlanslovenija/tunneldigger)
- [WireGuard Official](https://www.wireguard.com/)
- [L2TP RFC 2661](https://tools.ietf.org/html/rfc2661)
- wlan slovenija mesh network documentation
- Apex Core documentation (see apex-core/docs/)

---

## Related Documents

- #008 - WireGuard VPN Support (feature ticket)
- Apex Core Whitepaper (apex-core/docs/31 - Apex Core v1.5 Whitepaper.md)
- Apex Protocol Overview (apex-core/docs/01 - Protocol Overview.md)

