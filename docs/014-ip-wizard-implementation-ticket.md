# Implementation Ticket #014: IP Allocation Wizard

**Type:** Implementation
**Priority:** High
**Status:** In Progress
**Created:** 2024-12-14
**Spec:** #013

---

## Scope

Implement IP Allocation Wizard with two modes:
1. **Simple Mode** - Region-based automatic allocation
2. **Advanced Mode** - Manual subnet selection

---

## Implementation Tasks

### Backend

- [ ] Create `IpAllocationWizard` view
- [ ] Create `IpAllocationRequest` model
- [ ] Create `RegionPool` model for region→subnet mapping
- [ ] API endpoints for wizard steps
- [ ] Subnet validation logic
- [ ] Auto-allocation algorithm

### Frontend

- [ ] Wizard container component
- [ ] Mode selector (Simple/Advanced)
- [ ] Country selector
- [ ] Region selector with map
- [ ] City selector (optional)
- [ ] Client count slider
- [ ] Manual subnet input (Advanced)
- [ ] Visual subnet browser (Advanced)
- [ ] Summary/confirmation screen

### Integration

- [ ] Connect to existing IP Pool system
- [ ] Sheriff notification hooks
- [ ] Audit logging

---

## Files to Create/Modify

```
nodewatcher/
├── core/
│   ├── allocation/
│   │   ├── __init__.py
│   │   ├── models.py        # IpAllocationRequest, RegionPool
│   │   ├── views.py         # Wizard views
│   │   ├── forms.py         # Wizard forms
│   │   ├── api.py           # REST endpoints
│   │   └── utils.py         # Validation, auto-allocation
│   ├── templates/
│   │   └── allocation/
│   │       ├── wizard.html
│   │       ├── step_country.html
│   │       ├── step_region.html
│   │       ├── step_city.html
│   │       ├── step_clients.html
│   │       ├── step_advanced_pool.html
│   │       ├── step_advanced_subnet.html
│   │       └── step_confirm.html
│   └── static/
│       └── allocation/
│           ├── css/
│           │   └── wizard.css
│           └── js/
│               ├── wizard.js
│               ├── slider.js
│               ├── subnet-browser.js
│               └── region-map.js
```

---

## Acceptance Criteria

1. User can complete Simple flow in 4 steps
2. User can complete Advanced flow in 3 steps
3. Self-service allocations (/28+) are instant
4. Larger allocations trigger sheriff notification
5. Visual subnet browser shows availability
6. Mobile-responsive design
