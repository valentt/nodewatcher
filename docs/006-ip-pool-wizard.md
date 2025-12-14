# Feature Ticket #006: IP Pool Allocation Wizard

**Status:** Planned
**Priority:** High
**Type:** Feature Request / UX Improvement
**Created:** 2024-12-14

---

## Summary

Create a step-by-step wizard that guides users through IP pool allocation without requiring networking expertise. The wizard asks simple questions and automatically calculates optimal pool configurations.

---

## Problem Statement

Current IP Pool creation requires users to:
- Understand CIDR notation
- Calculate prefix lengths manually
- Know the difference between IPv4/IPv6
- Understand subnet allocation strategies
- Make decisions about pool hierarchy

This creates barriers for:
- Community volunteers without networking background
- Experienced engineers who just want sensible defaults
- Anyone who doesn't want to do mental math

---

## Proposed Solution

### Smart IP Pool Wizard

A guided wizard that asks human-friendly questions and generates optimal configurations.

---

## Wizard Flow

### Step 1: Network Size

```
┌─────────────────────────────────────────────────────────────┐
│ IP Pool Wizard                                    Step 1/4  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  How large is your network?                                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Small (up to 50 nodes)                           │   │
│  │    Neighborhood or small village                     │   │
│  │    Recommended: /24 pool (254 addresses)            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Medium (50-250 nodes)                            │   │
│  │    Town or city district                            │   │
│  │    Recommended: /21 pool (~2,000 addresses)         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Large (250-1000 nodes)                           │   │
│  │    City-wide network                                │   │
│  │    Recommended: /18 pool (~16,000 addresses)        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Very Large (1000+ nodes)                         │   │
│  │    Regional or national network                     │   │
│  │    Recommended: /16 pool (~65,000 addresses)        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Custom - I know what I need                      │   │
│  │    Enter specific CIDR notation                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│                                          [Back] [Continue]  │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: IP Version

```
┌─────────────────────────────────────────────────────────────┐
│ IP Pool Wizard                                    Step 2/4  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Which IP version(s) do you need?                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ☑ IPv4 (Recommended)                               │   │
│  │    Works with all devices                           │   │
│  │    Required for most mesh networks                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ☐ IPv6 (Optional)                                  │   │
│  │    Future-proof, unlimited addresses                │   │
│  │    Some older devices may not support               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💡 Tip: Start with IPv4 only. You can add IPv6 later.    │
│                                                             │
│                                          [Back] [Continue]  │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Address Range

```
┌─────────────────────────────────────────────────────────────┐
│ IP Pool Wizard                                    Step 3/4  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Which address range should we use?                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ 10.x.x.x (Recommended)                           │   │
│  │    Largest private range                            │   │
│  │    Best for mesh networks                           │   │
│  │    10.0.0.0/8 - over 16 million addresses          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ 172.16.x.x - 172.31.x.x                         │   │
│  │    Medium private range                             │   │
│  │    172.16.0.0/12 - about 1 million addresses       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ 192.168.x.x                                      │   │
│  │    Smallest private range                           │   │
│  │    May conflict with home routers                   │   │
│  │    192.168.0.0/16 - about 65,000 addresses         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ 44.x.x.x (AMPRNet)                              │   │
│  │    Official amateur radio allocation                │   │
│  │    Requires AMPRNet registration                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Custom range                                     │   │
│  │    Enter your own base address                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│                                          [Back] [Continue]  │
└─────────────────────────────────────────────────────────────┘
```

### Step 4: Allocation Strategy

```
┌─────────────────────────────────────────────────────────────┐
│ IP Pool Wizard                                    Step 4/4  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  How should addresses be allocated to nodes?               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Automatic (Recommended)                          │   │
│  │    System assigns next available /32                │   │
│  │    Simple, no conflicts                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Subnet per node                                  │   │
│  │    Each node gets a /28 (16 addresses)             │   │
│  │    Good if nodes need multiple IPs                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ○ Geographic blocks                                │   │
│  │    Reserve ranges for different areas              │   │
│  │    Example: 10.1.x.x for Zone A, 10.2.x.x for B    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│                                          [Back] [Continue]  │
└─────────────────────────────────────────────────────────────┘
```

### Step 5: Summary & Confirmation

```
┌─────────────────────────────────────────────────────────────┐
│ IP Pool Wizard                                    Summary   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Your IP Pool Configuration:                               │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  📊 Pool Size:        Medium (up to 250 nodes)             │
│  🔢 IP Version:       IPv4                                  │
│  🌐 Network:          10.55.0.0/21                         │
│  📍 Usable Range:     10.55.0.1 - 10.55.7.254              │
│  🔢 Total Addresses:  2,046                                 │
│  📦 Allocation:       Automatic /32 per node               │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  This configuration will support:                          │
│  • Up to 2,046 individual node addresses                   │
│  • Room to grow 10x from your current size                │
│  • No conflicts with typical home networks                 │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  Pool Name: [Medium IPv4 Pool_________________]            │
│  Description: [Primary pool for city network___]           │
│                                                             │
│  ☐ Also create IPv6 pool with same settings               │
│                                                             │
│                               [Back] [Create IP Pool]      │
└─────────────────────────────────────────────────────────────┘
```

---

## Smart Features

### 1. Conflict Detection

```
⚠️ Warning: The range 10.0.0.0/24 may conflict with
   existing pool "Downtown Network" (10.0.0.0/22).

   Suggested alternative: 10.1.0.0/24
   [Use Suggested] [Keep Original]
```

### 2. Growth Recommendations

```
💡 Based on your selection of 50 nodes, we recommend
   a /22 pool instead of /24.

   This gives you room to grow 4x without creating
   a new pool later.

   [Accept Recommendation] [Keep /24]
```

### 3. Quick Presets

For power users who just want sensible defaults:

```
Quick Setup Presets:
┌────────────────────────────────────────────────────┐
│ 🏘️ Small Community    10.x.0.0/24    [Create]     │
│ 🏙️ City Network       10.x.0.0/20    [Create]     │
│ 🌍 Regional Network   10.x.0.0/16    [Create]     │
└────────────────────────────────────────────────────┘
```

---

## Technical Implementation

### Wizard State Machine

```python
class IPPoolWizard:
    STEPS = ['size', 'version', 'range', 'strategy', 'confirm']

    def get_recommendation(self, network_size):
        """Return recommended prefix based on network size."""
        recommendations = {
            'small': {'prefix': 24, 'description': 'Up to 254 nodes'},
            'medium': {'prefix': 21, 'description': 'Up to 2,046 nodes'},
            'large': {'prefix': 18, 'description': 'Up to 16,382 nodes'},
            'xlarge': {'prefix': 16, 'description': 'Up to 65,534 nodes'},
        }
        return recommendations.get(network_size)

    def find_available_range(self, base, prefix, existing_pools):
        """Find next available range that doesn't conflict."""
        # Implementation using ipaddress module
        pass

    def calculate_pool_details(self, network, prefix):
        """Calculate usable addresses, range, etc."""
        import ipaddress
        net = ipaddress.ip_network(f'{network}/{prefix}')
        return {
            'network': str(net.network_address),
            'broadcast': str(net.broadcast_address),
            'first_usable': str(net.network_address + 1),
            'last_usable': str(net.broadcast_address - 1),
            'total_hosts': net.num_addresses - 2,
            'prefix': prefix,
        }
```

### Frontend (JavaScript)

```javascript
class IPPoolWizard {
    constructor(container) {
        this.step = 0;
        this.data = {};
        this.container = container;
    }

    nextStep() {
        this.validateCurrentStep();
        this.step++;
        this.render();
    }

    calculateRecommendation() {
        // Real-time calculation as user selects options
    }

    render() {
        // Render current step
    }
}
```

---

## Integration Points

1. **Admin Panel:** "Create IP Pool" button opens wizard
2. **Project Creation:** Option to create pool during project setup
3. **API:** Wizard can also be accessed via API for automation

---

## Implementation Phases

### Phase 1: Basic Wizard (MVP)
- [ ] Step-by-step form
- [ ] Size recommendations
- [ ] IPv4 support
- [ ] Basic conflict detection

### Phase 2: Smart Features
- [ ] IPv6 support
- [ ] Growth recommendations
- [ ] Geographic block allocation
- [ ] Preset quick-create buttons

### Phase 3: Advanced
- [ ] Pool splitting wizard
- [ ] Pool expansion wizard
- [ ] Import from existing network
- [ ] Visual subnet map

---

## Success Metrics

- Time to create first IP pool (target: < 2 minutes)
- User errors during pool creation (target: near zero)
- Support requests about IP allocation (target: 50% reduction)

---

## Related Tickets

- #005 Local Sheriffs (area admins need to understand their IP ranges)
- (Future) #007 Node Registration Wizard

---

## Notes

- Wizard should work without JavaScript (progressive enhancement)
- All calculations happen server-side for security
- Pool configurations are validated before creation
- Consider adding "What's this?" tooltips for each option
