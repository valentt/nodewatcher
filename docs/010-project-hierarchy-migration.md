# Feature Ticket #010: Project Hierarchy and Node Migration

**Type:** Feature Request
**Priority:** Medium
**Status:** Proposed
**Created:** 2024-12-14

---

## Summary

Enable hierarchical project structure where a parent project (e.g., "Croatia") can spawn child projects (e.g., "Zagreb", "Split") with automatic node migration capabilities.

---

## Problem Statement

Community mesh networks often start small and grow organically:

1. **Day 1**: One project for entire country, few nodes
2. **Year 2**: 500+ nodes, local communities forming
3. **Year 3**: Need regional autonomy, local governance

Current nodewatcher requires manual node recreation when splitting projects.

---

## Proposed Solution

### Phase 1: Hierarchical Projects

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROJECT HIERARCHY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🇭🇷 Croatia (parent)                                           │
│  └── IP Pool: 10.10-53.0.0/16                                  │
│      │                                                          │
│      ├── 📍 Zagreb (child)                                     │
│      │   └── IP Pool: 10.10.0.0/16 (inherited from parent)     │
│      │                                                          │
│      ├── 📍 Split (child)                                      │
│      │   └── IP Pool: 10.21.0.0/16                             │
│      │                                                          │
│      ├── 📍 Rijeka (child)                                     │
│      │   └── IP Pool: 10.51.0.0/16                             │
│      │                                                          │
│      └── 📍 Osijek (child)                                     │
│          └── IP Pool: 10.31.0.0/16                             │
│                                                                 │
│  🇸🇮 Slovenia (parent)                                          │
│  └── IP Pool: 10.110-190.0.0/16                                │
│      │                                                          │
│      ├── 📍 Ljubljana (child)                                  │
│      │   └── IP Pool: 10.110.0.0/16                            │
│      │                                                          │
│      └── 📍 Maribor (child)                                    │
│          └── IP Pool: 10.120.0.0/16                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 2: Node Migration

```
┌─────────────────────────────────────────────────────────────────┐
│                     NODE MIGRATION FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BEFORE:                                                        │
│  ┌─────────────────────────────────────────┐                   │
│  │  🇭🇷 Croatia                             │                   │
│  │  ├── node-zg-001  (10.10.1.1)          │                   │
│  │  ├── node-zg-002  (10.10.1.5)          │                   │
│  │  ├── node-st-001  (10.21.0.1)          │                   │
│  │  └── node-ri-001  (10.51.0.1)          │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
│                        │                                        │
│                        ▼  [Create child project "Zagreb"]       │
│                                                                 │
│  AFTER:                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │  🇭🇷 Croatia                             │                   │
│  │  ├── node-st-001  (10.21.0.1)          │                   │
│  │  └── node-ri-001  (10.51.0.1)          │                   │
│  │                                         │                   │
│  │  └── 📍 Zagreb (child)                 │                   │
│  │      ├── node-zg-001  (10.10.1.1) ←────│── migrated        │
│  │      └── node-zg-002  (10.10.1.5) ←────│── migrated        │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
│  ✓ IP addresses preserved                                      │
│  ✓ Node configuration unchanged                                │
│  ✓ Only project assignment changes                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Model Changes

### Project Model Extension

```python
class Project(models.Model):
    # Existing fields...

    # NEW: Hierarchy support
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='children'
    )

    # NEW: IP pool inheritance
    inherit_pools = models.BooleanField(
        default=True,
        help_text="Inherit IP pools from parent project"
    )

    # NEW: Governance
    allow_node_migration = models.BooleanField(
        default=True,
        help_text="Allow nodes to be migrated to/from this project"
    )

    def get_available_pools(self):
        """Get pools from self + parent chain if inheriting"""
        pools = list(self.pools.all())
        if self.inherit_pools and self.parent:
            pools.extend(self.parent.get_available_pools())
        return pools

    def get_ancestry(self):
        """Return list of parent projects"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
```

### Node Migration Model

```python
class NodeMigration(models.Model):
    """Track node migrations between projects"""

    node = models.ForeignKey('Node', on_delete=models.CASCADE)
    from_project = models.ForeignKey(
        'Project',
        on_delete=models.PROTECT,
        related_name='migrations_out'
    )
    to_project = models.ForeignKey(
        'Project',
        on_delete=models.PROTECT,
        related_name='migrations_in'
    )

    migrated_at = models.DateTimeField(auto_now_add=True)
    migrated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    reason = models.TextField(blank=True)

    # Migration validation
    ip_preserved = models.BooleanField(default=True)
    required_reconfig = models.BooleanField(default=False)

    class Meta:
        ordering = ['-migrated_at']
```

---

## Migration Rules

### Automatic Migration (No IP Change)

Migration is automatic when:
- Child project's IP pool is subset of parent's pool
- Node's current IP falls within child's pool range

```python
def can_auto_migrate(node, target_project):
    """Check if node can migrate without IP change"""
    node_ip = node.get_primary_ip()

    for pool in target_project.get_available_pools():
        if node_ip in pool.network:
            return True, "IP preserved"

    return False, "Would require new IP assignment"
```

### Manual Migration (IP Change Required)

When IP pools don't overlap:
1. Warn user that IP will change
2. Generate new IP from target project's pool
3. Queue firmware rebuild
4. Track old IP for transition period

---

## UI: Project Creation Wizard

```
┌─────────────────────────────────────────────────────────────────┐
│  Create Child Project                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Parent Project: 🇭🇷 Croatia                                    │
│                                                                 │
│  Child Project Name: [Zagreb_________________]                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  📍 Select Geographic Area                              │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │                    [MAP]                          │  │   │
│  │  │         Draw region or select postal codes        │  │   │
│  │  │                                                   │  │   │
│  │  │    ┌─────────┐                                   │  │   │
│  │  │    │ ZAGREB  │  ← selected                       │  │   │
│  │  │    │ 10000   │                                   │  │   │
│  │  │    └─────────┘                                   │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  IP Pool Assignment:                                            │
│  ○ Inherit from parent (use parent's pools)                    │
│  ● Carve out dedicated pool:                                   │
│    └── [10.10.0.0/16_____] (matches postal code 10xxx)         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🔄 Auto-Migration Preview                              │   │
│  │                                                         │   │
│  │  Found 47 nodes in Croatia with IPs in 10.10.0.0/16:   │   │
│  │                                                         │   │
│  │  ☑ node-zg-001    10.10.1.1     ✓ auto-migrate        │   │
│  │  ☑ node-zg-002    10.10.1.5     ✓ auto-migrate        │   │
│  │  ☑ node-zg-003    10.10.2.1     ✓ auto-migrate        │   │
│  │  ...                                                    │   │
│  │  ☑ Select all 47 nodes                                 │   │
│  │                                                         │   │
│  │  These nodes will be automatically moved to Zagreb      │   │
│  │  project. No IP changes required.                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Local Sheriff: [@pero_mreza________] [+ Add more]             │
│                                                                 │
│           [ Cancel ]                [ Create Zagreb Project ]   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Migration Workflow

### Step 1: Create Child Project

```python
# Admin creates "Zagreb" under "Croatia"
zagreb = Project.objects.create(
    name="Zagreb",
    parent=croatia,
    inherit_pools=False  # Has own pool
)

# Assign dedicated IP pool
IpPool.objects.create(
    project=zagreb,
    network="10.10.0.0/16",
    description="Zagreb metropolitan area"
)
```

### Step 2: Auto-Detect Migratable Nodes

```python
def find_migratable_nodes(parent_project, child_project):
    """Find nodes that can migrate based on IP"""
    migratable = []

    child_pools = child_project.get_available_pools()

    for node in parent_project.nodes.all():
        node_ip = node.get_primary_ip()
        for pool in child_pools:
            if node_ip in pool.network:
                migratable.append({
                    'node': node,
                    'ip': node_ip,
                    'target_pool': pool,
                    'ip_change_required': False
                })
                break

    return migratable
```

### Step 3: Bulk Migration

```python
def migrate_nodes(nodes, target_project, user, reason=""):
    """Migrate multiple nodes to target project"""
    migrations = []

    for node in nodes:
        migration = NodeMigration.objects.create(
            node=node,
            from_project=node.project,
            to_project=target_project,
            migrated_by=user,
            reason=reason,
            ip_preserved=True
        )

        # Update node's project
        node.project = target_project
        node.save()

        migrations.append(migration)

    return migrations
```

---

## Governance Inheritance

```
┌─────────────────────────────────────────────────────────────────┐
│                  PERMISSION INHERITANCE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🇭🇷 Croatia (parent)                                           │
│  │   Admins: @glavni_admin                                     │
│  │   Sheriffs: (none at country level)                         │
│  │                                                              │
│  └── 📍 Zagreb                                                 │
│      │   Admins: inherits @glavni_admin                        │
│      │   Sheriffs: @pero_mreza, @ana_zg                        │
│      │   Local autonomy: ✓ Can approve up to /24               │
│      │                                                          │
│      └── 📍 Trešnjevka (micro-region)                         │
│              Admins: inherits chain                             │
│              Sheriffs: @marko_tresnja                           │
│              Local autonomy: ✓ Can approve up to /26           │
│                                                                 │
│  Permission check walks up the tree:                           │
│  Trešnjevka sheriff → Zagreb sheriff → Croatia admin           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Benefits

| Aspect | Benefit |
|--------|---------|
| **Start simple** | One project for whole country initially |
| **Grow organically** | Split when local communities form |
| **Zero downtime** | Nodes keep working during migration |
| **IP preservation** | No reconfiguration needed |
| **Clear governance** | Each region has local sheriffs |
| **Audit trail** | All migrations logged |

---

## Implementation Phases

### Phase 1: Data Model
- Add `parent` field to Project
- Create NodeMigration model
- Migration scripts for existing data

### Phase 2: Admin UI
- Project hierarchy tree view
- Bulk node migration tool
- Migration history viewer

### Phase 3: User-Facing
- Project selector with hierarchy
- "Request migration" for users
- Notification system for sheriffs

---

## Related Documents

- #011 - IP Pool Slider with Sheriff Approval
- #008 - WireGuard VPN Support
- IP Addressing Scheme (Croatia/Slovenia postal codes)
