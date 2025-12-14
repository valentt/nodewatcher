# Feature Ticket #005: Local Sheriffs (Area Administrators)

**Status:** Planned
**Priority:** CRITICAL
**Type:** Feature Request
**Created:** 2024-12-14

> ⚠️ **CRITICAL FEATURE**: Inactivity detection is essential for community networks.
> Without it, inactive sheriffs block areas and prevent new volunteers from helping.

---

## Summary

Implement a hierarchical administration system allowing "Local Sheriffs" - administrators responsible for specific geographic sub-areas of the mesh network, rather than the entire network.

---

## Problem Statement

Currently, nodewatcher has a flat admin structure:
- Superusers have full access to everything
- Regular users have limited access
- No middle ground for regional/area management

For large community mesh networks spanning multiple cities, neighborhoods, or regions, this creates problems:
- Central admins become bottlenecks
- Local knowledge is not utilized
- Inactive admins block progress in their areas
- No clear ownership of geographic regions

---

## Proposed Solution

### 1. Local Sheriff Role

A new role type: **Local Sheriff** (or "Area Admin")

**Permissions:**
- Manage nodes within their assigned area/project
- Add/remove nodes in their area
- Approve new node registrations in their area
- View monitoring data for their area
- Manage local users (co-admins) for their area

**Restrictions:**
- Cannot modify global settings
- Cannot manage other areas
- Cannot create new projects (only global admins)
- Cannot modify IP pools

### 2. Co-Admin System

Each area can have multiple administrators:

| Role | Description |
|------|-------------|
| **Primary Sheriff** | Main responsible person for the area |
| **Co-Admin** | Helper with same permissions as sheriff |
| **Observer** | Read-only access to area data |

### 3. Admin Lifecycle Management

**Adding Admins:**
- Global admin or Primary Sheriff can add co-admins
- Invitation system via email
- Approval workflow for new sheriffs

**Graceful Inactivity Handling:**

The system respects that volunteers have lives - illness, vacation, personal issues happen.

```
ACTIVE          →   AWAY           →   INACTIVE        →   REGULAR USER
(daily/weekly)      (30 days)          (60-90 days)        (needs to re-earn role)
     ↑                  ↑                   ↑
     └──────────────────┴───────────────────┘
              Return to activity = restore status
```

**Status Levels:**

| Status | Timeframe | What Happens |
|--------|-----------|--------------|
| **Active** | Regular activity | Full permissions, shown as primary contact |
| **Away** | 14-30 days inactive | Co-admin becomes primary, sheriff keeps role but marked "away" |
| **Inactive** | 30-60 days | Warning emails, co-admin fully takes over |
| **Dormant** | 60-90 days | Demoted to regular user, must re-apply |

**Key Principles:**
- **No punishment for short absence** - life happens
- **Co-admin automatically steps up** - network keeps running
- **Smooth return** - come back active = restore your role (within grace period)
- **Fair re-entry** - after long absence, prove activity again as co-admin first
- **The cycle continues** - people can move up and down based on availability

**Example Scenario:**
1. Marko is Sheriff, Ana is Co-Admin
2. Marko gets sick, inactive for 3 weeks
3. Ana automatically becomes acting Sheriff
4. Marko recovers, logs in → automatically restored as Sheriff
5. If Marko was gone 3 months → becomes regular user
6. Marko wants back in → applies as Co-Admin, proves activity, can become Sheriff again

**Succession:**
- If Primary Sheriff becomes inactive, Co-Admin automatically becomes acting Sheriff
- After grace period expires, Co-Admin officially becomes Sheriff
- No global admin approval needed for automatic succession
- Global admin can always override manually

### 4. Area Definition

Areas can be defined by:
- **Project-based:** Each project = one area
- **Geographic:** Polygon on map defining boundaries
- **Node-based:** Specific list of nodes

Recommended: Start with Project-based (simplest)

---

## User Interface

### Admin Panel Section: "Area Management"

```
┌─────────────────────────────────────────────────────────┐
│ Area Management                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Your Areas:                                              │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Zagreb Center          Sheriff    12 nodes   Active │ │
│ │ [Manage] [Add Co-Admin] [View Activity]             │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Split Coastal          Co-Admin   8 nodes    Active │ │
│ │ [View] [Request Sheriff Role]                       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ Areas Needing Sheriffs:                                  │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Rijeka Downtown        No Sheriff  5 nodes          │ │
│ │ [Apply to be Sheriff]                               │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Sheriff Dashboard

```
┌─────────────────────────────────────────────────────────┐
│ Zagreb Center - Sheriff Dashboard                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Team:                                                    │
│ • marko@example.com (You) - Primary Sheriff             │
│ • ana@example.com - Co-Admin - Last active: 2 days ago  │
│ • ivan@example.com - Observer                           │
│ [+ Add Team Member]                                      │
│                                                          │
│ Pending Actions:                                         │
│ • 2 new node registrations awaiting approval            │
│ • 1 node offline for 7 days                             │
│                                                          │
│ Quick Stats:                                             │
│ • 12 total nodes                                        │
│ • 10 online / 2 offline                                 │
│ • 45 connected clients                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Database Changes

### New Models

```python
class AreaRole(models.Model):
    """Role assignment for area administration."""

    ROLE_CHOICES = (
        ('sheriff', 'Primary Sheriff'),
        ('co_admin', 'Co-Administrator'),
        ('observer', 'Observer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    assigned_by = models.ForeignKey(User, related_name='assigned_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'project')


class AdminActivity(models.Model):
    """Track admin activity for inactivity detection."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = JSONField(default=dict)


class SheriffApplication(models.Model):
    """Applications to become a sheriff for an area."""

    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    motivation = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, null=True, related_name='reviewed_applications')
    reviewed_at = models.DateTimeField(null=True)
```

---

## Implementation Phases

### Phase 1: Basic Role System + Inactivity Detection ⭐ HIGH PRIORITY
- [ ] Create AreaRole model
- [ ] Add role assignment UI in admin
- [ ] Permission checks for node management
- [ ] Basic sheriff dashboard
- [ ] **Activity tracking from day one** (last_login, last_action timestamps)
- [ ] **Inactivity indicator in admin** (visual badge: Active/Warning/Inactive)

### Phase 2: Automated Inactivity Management ⭐ HIGH PRIORITY
- [ ] Automatic inactivity detection (configurable: 30/60/90 days)
- [ ] Email notifications for inactivity warnings
- [ ] Admin dashboard showing inactive sheriffs
- [ ] One-click "remove inactive sheriff" action
- [ ] Auto-demotion option (optional, admin-configurable)

### Phase 3: Self-Service
- [ ] Sheriff application system
- [ ] Co-admin invitation system
- [ ] Role transfer workflow
- [ ] Public "areas needing sheriffs" list

### Phase 4: Succession & Advanced
- [ ] Automatic succession to co-admin
- [ ] Scheduled notifications
- [ ] Activity reports and analytics

---

## Security Considerations

- Sheriff permissions strictly scoped to their area
- Audit log for all role changes
- Two-factor authentication recommended for sheriffs
- Global admin can override any sheriff action
- Rate limiting on role change operations

---

## Success Metrics

- Number of active sheriffs per area
- Average response time to node issues
- Admin activity distribution
- Reduction in global admin workload
- Community satisfaction surveys

---

## Related Tickets

- #004 UI Redesign Concept
- (Future) #006 Email Notification System
- (Future) #007 Node Approval Workflow

---

## Notes

- Term "Sheriff" chosen to reflect community/humanitarian nature
- Consider localization: "Sheriff" → "Šerif" (HR), "Betreuer" (DE), "Skrbnik" (SI)
- Could integrate with existing django-guardian object permissions
