# Feature Ticket #011: IP Pool Slider with Sheriff Approval

**Type:** Feature Request
**Priority:** High
**Status:** Proposed
**Created:** 2024-12-14

---

## Summary

Replace technical subnet mask selection with user-friendly client count slider. Self-service for small allocations (/28 = 14 clients), sheriff approval required for larger requests.

---

## Problem Statement

Current IP allocation UX issues:

1. **Technical jargon**: Users must understand CIDR notation (/28, /26, etc.)
2. **No governance**: Anyone can request large IP blocks
3. **Resource waste**: Over-allocation depletes shared pools
4. **No accountability**: No tracking of who approved what

---

## Proposed Solution

### Core Concept

```
USER THINKS:     "I need ~50 clients"
NOT:             "I need a /26 subnet"

SYSTEM SHOWS:    Slider with client count
CONVERTS TO:     Appropriate subnet automatically
```

### Self-Service Limits

| Subnet | Usable IPs | Self-Service? |
|--------|------------|---------------|
| /30 | 2 | ✓ Yes |
| /29 | 6 | ✓ Yes |
| /28 | 14 | ✓ Yes (DEFAULT MAX) |
| /27 | 30 | ✗ Sheriff approval |
| /26 | 62 | ✗ Sheriff approval |
| /25 | 126 | ✗ Sheriff approval |
| /24 | 254 | ✗ Sheriff approval |

---

## UI Design

### Default View (Self-Service Zone)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🌐 Zatraži IP adrese za svoj node                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Projekt: 🇭🇷 Croatia → 📍 Zagreb                                           │
│  Lokacija: Trešnjevka                                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  Koliko klijenata trebaš?                                          │   │
│  │                                                                     │   │
│  │      2      6      14     30     62     126    254                 │   │
│  │      ├──────┼──────┼──────┼──────┼──────┼──────┤                   │   │
│  │      ●━━━━━━━━━━━━━○      ┆                                        │   │
│  │                    ▲      ┆                                        │   │
│  │                   10      ┆                                        │   │
│  │                          ┆                                         │   │
│  │   ├─── ODMAH DOSTUPNO ───┤ ├──── TREBA ODOBRENJE ─────────────┤   │   │
│  │         (do 14)                    (15+)                          │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  📊 Tvoja alokacija                                                 │   │
│  │                                                                     │   │
│  │   Subnet:       /28                                                │   │
│  │   IP raspon:    10.10.47.0 - 10.10.47.15                          │   │
│  │   Gateway:      10.10.47.1                                         │   │
│  │   DHCP pool:    10.10.47.2 - 10.10.47.14                          │   │
│  │   Za klijente:  14 uređaja max                                     │   │
│  │                                                                     │   │
│  │   ┌─────────────────────────────────────────────────────────┐     │   │
│  │   │ █████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │     │   │
│  │   │ Tražiš 10 od 14 dostupnih (71%)                        │     │   │
│  │   └─────────────────────────────────────────────────────────┘     │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│                                              [ Zatraži IP adrese ]          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### When Slider Exceeds Self-Service Limit

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🌐 Zatraži IP adrese za svoj node                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  Koliko klijenata trebaš?                                          │   │
│  │                                                                     │   │
│  │      2      6      14     30     62     126    254                 │   │
│  │      ├──────┼──────┼──────┼──────┼──────┼──────┤                   │   │
│  │      ○──────────────────────━━━━━●                                 │   │
│  │                                  ▲                                  │   │
│  │                                 45                                  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  ⚠️  Trebaš odobrenje šerifa                                        │   │
│  │                                                                     │   │
│  │  Za više od 14 klijenata potrebno je odobrenje lokalnog šerifa.   │   │
│  │                                                                     │   │
│  │  Zašto? IP adrese su zajednički resurs. Veće alokacije trebaju    │   │
│  │  provjeru da se osigura odgovorno korištenje.                     │   │
│  │                                                                     │   │
│  │  ───────────────────────────────────────────────────────────────   │   │
│  │                                                                     │   │
│  │  📊 Zatražena alokacija                                            │   │
│  │                                                                     │   │
│  │   Subnet:       /26                                                │   │
│  │   IP raspon:    10.10.48.0 - 10.10.48.63                          │   │
│  │   Za klijente:  62 uređaja max                                     │   │
│  │                                                                     │   │
│  │  ───────────────────────────────────────────────────────────────   │   │
│  │                                                                     │   │
│  │  📝 Obrazloženje (obavezno):                                       │   │
│  │  ┌───────────────────────────────────────────────────────────────┐ │   │
│  │  │ Planiram pokriti stambeni blok od 40 stanova. Imam dogovor   │ │   │
│  │  │ sa upraviteljem zgrade za postavljanje antena na krov.       │ │   │
│  │  │                                                               │ │   │
│  │  └───────────────────────────────────────────────────────────────┘ │   │
│  │                                                                     │   │
│  │  👤 Šerif za Zagreb: @pero_mreza                                   │   │
│  │     Prosječno vrijeme odgovora: ~4 sata                            │   │
│  │                                                                     │   │
│  │  [ Pošalji zahtjev ]         [ Vrati na 14 klijenata ]            │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Sheriff Dashboard

### Pending Requests View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🤠 Sheriff Dashboard                                          @pero_mreza  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📍 Zagreb     📊 Pool: 10.10.0.0/16     Iskorišteno: 23%                  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  📬 Zahtjevi na čekanju (3)                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  #201                                                 prije 2 sata  │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │  👤 marko_tresnja                                                   │   │
│  │                                                                     │   │
│  │  Traži:     /26 (62 klijenta)                                      │   │
│  │  Trenutno:  /28 (14 klijenata) - 89% iskorišteno                   │   │
│  │                                                                     │   │
│  │  📍 Trešnjevka, Zagreb                                             │   │
│  │                                                                     │   │
│  │  📝 "Planiram pokriti stambeni blok od 40 stanova. Imam dogovor   │   │
│  │      sa upraviteljem zgrade za postavljanje antena na krov."       │   │
│  │                                                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  📈 Povijest korisnika                                      │   │   │
│  │  │  • Član od: 2023-05-12 (1.5 godina)                        │   │   │
│  │  │  • Aktivnih nodeova: 2                                      │   │   │
│  │  │  • Trenutna iskorištenost: 89% (12/14 IP)                  │   │   │
│  │  │  • Prethodni zahtjevi: 1 (odobren, koristi 100%)           │   │   │
│  │  │  • Status u zajednici: ⭐ Aktivan kontributor               │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                     │   │
│  │  [ ✓ Odobri /26 ]  [ ✓ Odobri /27 ]  [ ✗ Odbij ]  [ 💬 Komentiraj ]│   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  #200                                                 prije 6 sati  │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │  👤 novi_korisnik_123                                               │   │
│  │                                                                     │   │
│  │  Traži:     /24 (254 klijenta)                                     │   │
│  │  Trenutno:  Novi korisnik                                          │   │
│  │                                                                     │   │
│  │  📝 "trebam puno ip adresa"                                        │   │
│  │                                                                     │   │
│  │  ⚠️  UPOZORENJA:                                                    │   │
│  │  • Novi korisnik bez povijesti                                     │   │
│  │  • Nejasno obrazloženje                                            │   │
│  │  • Zahtjev za /24 je neuobičajeno velik                           │   │
│  │                                                                     │   │
│  │  💡 Preporuka: Odobri /28 za početak, neka dokaže korištenje      │   │
│  │                                                                     │   │
│  │  [ ✓ Odobri /24 ]  [ ✓ Odobri /28 ]  [ ✗ Odbij ]  [ 💬 Komentiraj ]│   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Approval/Rejection Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Odobri zahtjev #201                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Korisnik: marko_tresnja                                                    │
│  Tražio: /26 (62 klijenta)                                                 │
│                                                                             │
│  Odobri:                                                                    │
│  ○ /26 - 62 klijenta (kako zatraženo)                                      │
│  ● /27 - 30 klijenata (dovoljno za početak)                                │
│  ○ /28 - 14 klijenata (samo samouslužni minimum)                           │
│                                                                             │
│  Komentar za korisnika (opcionalno):                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │ Odobravam /27 za sada. Kad popuniš 80%, javi se za proširenje.       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ☑ Pošalji email obavijest korisniku                                       │
│                                                                             │
│                               [ Odustani ]    [ Odobri ]                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Model

### IP Allocation Request

```python
class IpAllocationRequest(models.Model):
    """Request for IP pool allocation"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Na čekanju'
        APPROVED = 'approved', 'Odobreno'
        PARTIALLY_APPROVED = 'partial', 'Djelomično odobreno'
        REJECTED = 'rejected', 'Odbijeno'

    # Request details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    node = models.ForeignKey('Node', on_delete=models.CASCADE, null=True)

    # What they requested
    requested_clients = models.IntegerField()
    requested_prefix = models.IntegerField()  # e.g., 26 for /26

    # Justification
    reason = models.TextField()

    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # Approval details
    approved_prefix = models.IntegerField(null=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_allocations'
    )
    approved_at = models.DateTimeField(null=True)
    sheriff_comment = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
```

### Project Sheriff Configuration

```python
class ProjectSheriff(models.Model):
    """Sheriff assignment for a project"""

    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='sheriffs'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Permissions
    can_approve_up_to = models.IntegerField(
        default=24,
        help_text="Smallest prefix this sheriff can approve (e.g., 24 = /24)"
    )

    # Notifications
    notify_on_request = models.BooleanField(default=True)
    notify_email = models.EmailField(blank=True)

    # Stats
    avg_response_time = models.DurationField(null=True)
    total_approved = models.IntegerField(default=0)
    total_rejected = models.IntegerField(default=0)

    class Meta:
        unique_together = ['project', 'user']
```

### Self-Service Limits

```python
class ProjectAllocationPolicy(models.Model):
    """IP allocation policy for a project"""

    project = models.OneToOneField(
        'Project',
        on_delete=models.CASCADE,
        related_name='allocation_policy'
    )

    # Self-service limits
    self_service_max_prefix = models.IntegerField(
        default=28,
        help_text="Largest allocation users can get without approval (/28 = 14 clients)"
    )

    # Per-user limits
    max_allocations_per_user = models.IntegerField(
        default=5,
        help_text="Maximum number of allocations per user"
    )

    # Cooldown
    request_cooldown_hours = models.IntegerField(
        default=24,
        help_text="Hours to wait between requests"
    )

    # Justification requirements
    require_reason_above_prefix = models.IntegerField(
        default=28,
        help_text="Require justification for allocations larger than this"
    )
    min_reason_length = models.IntegerField(default=50)
```

---

## Slider Logic

### Frontend (JavaScript)

```javascript
const ALLOCATION_TIERS = [
  { prefix: 30, clients: 2,   selfService: true },
  { prefix: 29, clients: 6,   selfService: true },
  { prefix: 28, clients: 14,  selfService: true },   // ← DEFAULT MAX
  { prefix: 27, clients: 30,  selfService: false },
  { prefix: 26, clients: 62,  selfService: false },
  { prefix: 25, clients: 126, selfService: false },
  { prefix: 24, clients: 254, selfService: false },
];

class IpAllocationSlider {
  constructor(options) {
    this.selfServiceLimit = options.selfServiceLimit || 28;
    this.currentValue = options.defaultClients || 10;
  }

  clientsToPrefix(clients) {
    // Find smallest prefix that fits requested clients
    for (const tier of ALLOCATION_TIERS) {
      if (clients <= tier.clients) {
        return tier;
      }
    }
    return ALLOCATION_TIERS[ALLOCATION_TIERS.length - 1];
  }

  onSliderChange(clientCount) {
    const tier = this.clientsToPrefix(clientCount);

    // Update subnet display
    this.updateSubnetInfo(tier);

    // Check if approval needed
    if (tier.prefix < this.selfServiceLimit) {
      this.showApprovalRequired(tier);
    } else {
      this.hideApprovalRequired();
    }

    // Update submit button
    this.updateSubmitButton(tier.selfService);
  }

  showApprovalRequired(tier) {
    document.getElementById('approval-panel').classList.remove('hidden');
    document.getElementById('requested-prefix').textContent = `/${tier.prefix}`;
    document.getElementById('requested-clients').textContent = tier.clients;
  }
}
```

### Backend Validation

```python
def validate_allocation_request(user, project, requested_prefix):
    """Validate IP allocation request"""
    policy = project.allocation_policy

    # Check if self-service is allowed
    if requested_prefix >= policy.self_service_max_prefix:
        return {
            'allowed': True,
            'needs_approval': False,
            'message': 'Alokacija odobrena automatski'
        }

    # Check user history
    user_stats = get_user_allocation_stats(user, project)

    # Check cooldown
    if user_stats['last_request']:
        hours_since = (now() - user_stats['last_request']).total_seconds() / 3600
        if hours_since < policy.request_cooldown_hours:
            return {
                'allowed': False,
                'needs_approval': False,
                'message': f'Moraš pričekati još {policy.request_cooldown_hours - hours_since:.0f} sati'
            }

    # Check max allocations
    if user_stats['total_allocations'] >= policy.max_allocations_per_user:
        return {
            'allowed': False,
            'needs_approval': False,
            'message': 'Dosegnut maksimalan broj alokacija'
        }

    # Needs sheriff approval
    return {
        'allowed': True,
        'needs_approval': True,
        'sheriff': get_project_sheriff(project),
        'message': 'Zahtjev će biti poslan šerifu na odobrenje'
    }
```

---

## Notification System

### Email Templates

```
Subject: 🌐 Novi zahtjev za IP alokaciju - {project_name}

Pozdrav {sheriff_name},

Korisnik {user_name} je zatražio veću IP alokaciju:

📍 Projekt: {project_name}
📊 Zatraženo: /{requested_prefix} ({requested_clients} klijenata)
📝 Obrazloženje: {reason}

👤 O korisniku:
• Član od: {member_since}
• Aktivnih nodeova: {active_nodes}
• Trenutna iskorištenost: {utilization}%

[Odobri] [Odbij] [Pogledaj detalje]

--
Nodewatcher Sheriff System
```

### In-App Notifications

```python
def notify_sheriff_new_request(request):
    """Notify sheriff about new allocation request"""
    for sheriff in request.project.sheriffs.filter(notify_on_request=True):
        Notification.objects.create(
            user=sheriff.user,
            type='allocation_request',
            title=f'Novi zahtjev: {request.user.username} traži /{request.requested_prefix}',
            message=request.reason[:100],
            action_url=reverse('admin:allocation_request', args=[request.id])
        )

        if sheriff.notify_email:
            send_sheriff_email(sheriff, request)
```

---

## User Feedback After Approval

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ✅ Tvoj zahtjev je odobren!                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Šerif @pero_mreza je odobrio tvoj zahtjev za IP adrese.                   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  📊 Tvoja nova alokacija                                            │   │
│  │                                                                     │   │
│  │  Zatraženo:     /26 (62 klijenta)                                  │   │
│  │  Odobreno:      /27 (30 klijenata)                                 │   │
│  │                                                                     │   │
│  │  IP raspon:     10.10.48.0 - 10.10.48.31                          │   │
│  │  Gateway:       10.10.48.1                                         │   │
│  │  DHCP pool:     10.10.48.2 - 10.10.48.30                          │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  💬 Komentar šerifa:                                                        │
│  "Odobravam /27 za sada. Kad popuniš 80%, javi se za proširenje."          │
│                                                                             │
│  [ Preuzmi konfiguraciju ]    [ Zatraži firmware rebuild ]                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Benefits

| Stakeholder | Benefit |
|-------------|---------|
| **Korisnici** | Jednostavno - biraju broj klijenata, ne subnet maske |
| **Šerifi** | Kontrola nad velikim alokacijama, jasna obrazloženja |
| **Zajednica** | Odgovorno korištenje IP resursa |
| **Admini** | Audit trail, statistike, policy konfiguracija |

---

## Implementation Phases

### Phase 1: Core Models
- IpAllocationRequest model
- ProjectSheriff model
- ProjectAllocationPolicy model

### Phase 2: Slider UI
- Client count slider component
- Subnet calculation logic
- Approval panel toggle

### Phase 3: Sheriff Dashboard
- Pending requests list
- User history view
- Approve/reject workflow

### Phase 4: Notifications
- Email notifications
- In-app notifications
- Request status tracking

---

## Configuration Defaults

```python
# settings.py or project config

IP_ALLOCATION_DEFAULTS = {
    'self_service_max_prefix': 28,      # /28 = 14 clients
    'max_allocations_per_user': 5,
    'request_cooldown_hours': 24,
    'min_reason_length': 50,
    'notify_sheriffs': True,
}
```

---

## Related Documents

- #010 - Project Hierarchy and Node Migration
- #008 - WireGuard VPN Support
- IP Addressing Scheme (Croatia/Slovenia postal codes)
