# IP Addressing Plan: Croatia & Slovenia Mesh Network

**Document:** #012
**Type:** Network Architecture
**Created:** 2024-12-14
**Status:** Approved

---

## Executive Summary

Unified IP addressing scheme for community mesh networks in Croatia and Slovenia based on postal code regions. Simple, memorable, and scalable.

**Formula:**
- 🇭🇷 Croatia: `10.[prva 2 broja pošte].0.0/16`
- 🇸🇮 Slovenia: `10.1[prva 2 broja pošte].0.0/16`

---

## Network Overview

```
10.0.0.0/8 - MESH NETWORK
│
├─── 10.10.0.0 - 10.53.255.255    🇭🇷 CROATIA    (20 regija)
│
├─── 10.110.0.0 - 10.190.255.255  🇸🇮 SLOVENIA   (8 regija)
│
└─── 10.200.0.0 - 10.255.255.255  📦 RESERVED    (future)
```

| Segment | Namjena | Kapacitet |
|---------|---------|-----------|
| `10.10-53.0.0` | Hrvatska | 1,310,680 IP |
| `10.110-190.0.0` | Slovenija | 524,280 IP |
| `10.200-255.0.0` | Rezervirano | 3,670,008 IP |

---

## 🇭🇷 CROATIA - 20 Regions

### Overview Map

```
                    HRVATSKA - IP REGIJE

            ┌─────────────────────────────────────┐
            │  49        42        48      40     │
            │Krapina  Varaždin  Kopriv. Čakovec   │
            │   ·────────·────────·────────·      │
            │           │        │               │
            │     ┌─────┴────────┴─────┐         │
            │     │    43 Bjelovar     │   33    │
            │     │         ·──────────│─Virovi. │
            │     └─────────┬──────────┘    │    │
   51       │   10          │     44        │    │
 Rijeka ────│─ZAGREB────────┼───Sisak ──────┤    │
    │       │               │     │    34   │    │
    │       │    47         │     │  Požega │    │  31
    │       │  Karlovac─────┘     │    │    │    │Osijek
    │       │     │               │    │    │    │  │
    │       │     │          35 Sl.Brod────┴────┴──┤
    │       │     │               │                │
   52       │    53              │           32   │
  Pazin     │  Gospić            │         Vukovar│
 (Istra)    │     │              │                │
            │     │              │                │
            └─────┴──────────────┴────────────────┘
                  │
                  │         23 Zadar
                  │            │
                  │         22 Šibenik
                  │            │
                  │         21 SPLIT
                  │            │
                  │         20 Dubrovnik
                  │
```

### Complete Region List

| # | Pošta | Regija | Glavni grad | IP raspon | Gateway |
|---|-------|--------|-------------|-----------|---------|
| 1 | **10000** | Grad Zagreb | Zagreb | `10.10.0.0/16` | `10.10.0.1` |
| 2 | **20000** | Dubrovačko-neretvanska | Dubrovnik | `10.20.0.0/16` | `10.20.0.1` |
| 3 | **21000** | Splitsko-dalmatinska | Split | `10.21.0.0/16` | `10.21.0.1` |
| 4 | **22000** | Šibensko-kninska | Šibenik | `10.22.0.0/16` | `10.22.0.1` |
| 5 | **23000** | Zadarska | Zadar | `10.23.0.0/16` | `10.23.0.1` |
| 6 | **31000** | Osječko-baranjska | Osijek | `10.31.0.0/16` | `10.31.0.1` |
| 7 | **32000** | Vukovarsko-srijemska | Vukovar | `10.32.0.0/16` | `10.32.0.1` |
| 8 | **33000** | Virovitičko-podravska | Virovitica | `10.33.0.0/16` | `10.33.0.1` |
| 9 | **34000** | Požeško-slavonska | Požega | `10.34.0.0/16` | `10.34.0.1` |
| 10 | **35000** | Brodsko-posavska | Slavonski Brod | `10.35.0.0/16` | `10.35.0.1` |
| 11 | **40000** | Međimurska | Čakovec | `10.40.0.0/16` | `10.40.0.1` |
| 12 | **42000** | Varaždinska | Varaždin | `10.42.0.0/16` | `10.42.0.1` |
| 13 | **43000** | Bjelovarsko-bilogorska | Bjelovar | `10.43.0.0/16` | `10.43.0.1` |
| 14 | **44000** | Sisačko-moslavačka | Sisak | `10.44.0.0/16` | `10.44.0.1` |
| 15 | **47000** | Karlovačka | Karlovac | `10.47.0.0/16` | `10.47.0.1` |
| 16 | **48000** | Koprivničko-križevačka | Koprivnica | `10.48.0.0/16` | `10.48.0.1` |
| 17 | **49000** | Krapinsko-zagorska | Krapina | `10.49.0.0/16` | `10.49.0.1` |
| 18 | **51000** | Primorsko-goranska | Rijeka | `10.51.0.0/16` | `10.51.0.1` |
| 19 | **52000** | Istarska | Pazin | `10.52.0.0/16` | `10.52.0.1` |
| 20 | **53000** | Ličko-senjska | Gospić | `10.53.0.0/16` | `10.53.0.1` |

---

### Croatia - Detailed Breakdown by Region

#### 10.10.0.0/16 - ZAGREBAČKA REGIJA

```
10.10.0.0/16 - Zagreb i okolica
│
├── 10.10.0.0/18   - Zagreb centar (10000)      16,382 IP
├── 10.10.64.0/18  - Sesvete (10360)            16,382 IP
├── 10.10.128.0/18 - Velika Gorica (10410)      16,382 IP
└── 10.10.192.0/18 - Samobor/Zaprešić (10430)   16,382 IP
```

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Zagreb - centar | 10000 | `10.10.0.0/18` | 16,382 |
| Zagreb - Dubrava | 10040 | `10.10.16.0/20` | 4,094 |
| Zagreb - Novi Zagreb | 10020 | `10.10.32.0/20` | 4,094 |
| Sesvete | 10360 | `10.10.64.0/18` | 16,382 |
| Dugo Selo | 10370 | `10.10.80.0/20` | 4,094 |
| Velika Gorica | 10410 | `10.10.128.0/18` | 16,382 |
| Samobor | 10430 | `10.10.192.0/19` | 8,190 |
| Zaprešić | 10290 | `10.10.224.0/19` | 8,190 |
| Jastrebarsko | 10450 | `10.10.240.0/20` | 4,094 |

---

#### 10.21.0.0/16 - SPLITSKA REGIJA

```
10.21.0.0/16 - Split i Dalmacija
│
├── 10.21.0.0/18   - Split centar (21000)       16,382 IP
├── 10.21.64.0/18  - Kaštela/Solin (21210)      16,382 IP
├── 10.21.128.0/18 - Sinj/Imotski (21230)       16,382 IP
└── 10.21.192.0/18 - Makarska/Omiš (21300)      16,382 IP
```

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Split | 21000 | `10.21.0.0/18` | 16,382 |
| Solin | 21210 | `10.21.64.0/19` | 8,190 |
| Kaštela | 21212 | `10.21.96.0/19` | 8,190 |
| Sinj | 21230 | `10.21.128.0/19` | 8,190 |
| Imotski | 21260 | `10.21.160.0/19` | 8,190 |
| Makarska | 21300 | `10.21.192.0/19` | 8,190 |
| Omiš | 21310 | `10.21.224.0/19` | 8,190 |
| Trogir | 21220 | `10.21.240.0/20` | 4,094 |

---

#### 10.31.0.0/16 - OSJEČKA REGIJA

```
10.31.0.0/16 - Osijek i Baranja
│
├── 10.31.0.0/18   - Osijek (31000)             16,382 IP
├── 10.31.64.0/18  - Đakovo (31400)             16,382 IP
├── 10.31.128.0/18 - Beli Manastir (31300)      16,382 IP
└── 10.31.192.0/18 - Našice/Belišće (31500)     16,382 IP
```

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Osijek | 31000 | `10.31.0.0/18` | 16,382 |
| Đakovo | 31400 | `10.31.64.0/18` | 16,382 |
| Beli Manastir | 31300 | `10.31.128.0/18` | 16,382 |
| Našice | 31500 | `10.31.192.0/19` | 8,190 |
| Belišće | 31551 | `10.31.224.0/19` | 8,190 |
| Valpovo | 31550 | `10.31.240.0/20` | 4,094 |

---

#### 10.51.0.0/16 - PRIMORSKA REGIJA

```
10.51.0.0/16 - Rijeka i Primorje
│
├── 10.51.0.0/18   - Rijeka (51000)             16,382 IP
├── 10.51.64.0/18  - Opatija/Lovran (51410)     16,382 IP
├── 10.51.128.0/18 - Crikvenica/Krk (51260)     16,382 IP
└── 10.51.192.0/18 - Delnice/Gorski k. (51300)  16,382 IP
```

---

#### 10.52.0.0/16 - ISTARSKA REGIJA

```
10.52.0.0/16 - Istra
│
├── 10.52.0.0/18   - Pula (52100)               16,382 IP
├── 10.52.64.0/18  - Rovinj/Poreč (52210)       16,382 IP
├── 10.52.128.0/18 - Pazin/centar (52000)       16,382 IP
└── 10.52.192.0/18 - Umag/Novigrad (52470)      16,382 IP
```

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Pula | 52100 | `10.52.0.0/18` | 16,382 |
| Rovinj | 52210 | `10.52.64.0/19` | 8,190 |
| Poreč | 52440 | `10.52.96.0/19` | 8,190 |
| Pazin | 52000 | `10.52.128.0/18` | 16,382 |
| Umag | 52470 | `10.52.192.0/19` | 8,190 |
| Novigrad | 52466 | `10.52.224.0/19` | 8,190 |
| Labin | 52220 | `10.52.240.0/20` | 4,094 |

---

## 🇸🇮 SLOVENIA - 8 Regions

### Overview Map

```
                    SLOVENIJA - IP REGIJE

            ┌─────────────────────────────────────┐
            │                                     │
            │     9 Murska Sobota                 │
            │           ·                         │
            │           │                         │
            │     2 MARIBOR ─────── 3 Celje       │
            │           ·               ·         │
            │           │               │         │
            │     4 Kranj ──── 1 LJUBLJANA        │
            │        ·              ·      \      │
            │        │              │       \     │
            │  5 Nova Gorica        │    8 Novo   │
            │        ·              │      Mesto  │
            │        │              │             │
            │     6 Koper           │             │
            │                                     │
            └─────────────────────────────────────┘
```

### Complete Region List

| # | Pošta | Regija | Glavni grad | IP raspon | Gateway |
|---|-------|--------|-------------|-----------|---------|
| 1 | **1000** | Osrednjeslovenska | Ljubljana | `10.110.0.0/16` | `10.110.0.1` |
| 2 | **2000** | Podravska | Maribor | `10.120.0.0/16` | `10.120.0.1` |
| 3 | **3000** | Savinjska | Celje | `10.130.0.0/16` | `10.130.0.1` |
| 4 | **4000** | Gorenjska | Kranj | `10.140.0.0/16` | `10.140.0.1` |
| 5 | **5000** | Goriška | Nova Gorica | `10.150.0.0/16` | `10.150.0.1` |
| 6 | **6000** | Obalno-kraška | Koper | `10.160.0.0/16` | `10.160.0.1` |
| 7 | **8000** | Jugovzhodna | Novo Mesto | `10.180.0.0/16` | `10.180.0.1` |
| 8 | **9000** | Pomurska | Murska Sobota | `10.190.0.0/16` | `10.190.0.1` |

> ⚠️ **Napomena:** Pošta 7xxx ne postoji u slovenskom sustavu

---

### Slovenia - Detailed Breakdown

#### 10.110.0.0/16 - LJUBLJANA

```
10.110.0.0/16 - Ljubljana i okolica
│
├── 10.110.0.0/18   - Ljubljana centar (1000)   16,382 IP
├── 10.110.64.0/18  - Domžale (1230)            16,382 IP
├── 10.110.128.0/18 - Vrhnika/Logatec (1360)    16,382 IP
└── 10.110.192.0/18 - Grosuplje/Škofljica       16,382 IP
```

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Ljubljana centar | 1000 | `10.110.0.0/18` | 16,382 |
| Ljubljana Šiška | 1000 | `10.110.16.0/20` | 4,094 |
| Ljubljana Moste | 1000 | `10.110.32.0/20` | 4,094 |
| Domžale | 1230 | `10.110.64.0/19` | 8,190 |
| Kamnik | 1240 | `10.110.96.0/19` | 8,190 |
| Vrhnika | 1360 | `10.110.128.0/19` | 8,190 |
| Logatec | 1370 | `10.110.160.0/19` | 8,190 |
| Grosuplje | 1290 | `10.110.192.0/19` | 8,190 |

---

#### 10.120.0.0/16 - MARIBOR

```
10.120.0.0/16 - Maribor i Podravje
│
├── 10.120.0.0/18   - Maribor (2000)            16,382 IP
├── 10.120.64.0/18  - Ptuj (2250)               16,382 IP
├── 10.120.128.0/18 - Slovenska Bistrica        16,382 IP
└── 10.120.192.0/18 - Ruše/Selnica              16,382 IP
```

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Maribor | 2000 | `10.120.0.0/18` | 16,382 |
| Ptuj | 2250 | `10.120.64.0/18` | 16,382 |
| Slovenska Bistrica | 2310 | `10.120.128.0/19` | 8,190 |
| Lenart | 2230 | `10.120.160.0/19` | 8,190 |
| Ruše | 2342 | `10.120.192.0/19` | 8,190 |
| Ormož | 2270 | `10.120.224.0/19` | 8,190 |

---

#### 10.130.0.0/16 - CELJE

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Celje | 3000 | `10.130.0.0/18` | 16,382 |
| Velenje | 3320 | `10.130.64.0/18` | 16,382 |
| Žalec | 3310 | `10.130.128.0/19` | 8,190 |
| Šentjur | 3230 | `10.130.160.0/19` | 8,190 |
| Laško | 3270 | `10.130.192.0/19` | 8,190 |
| Šmarje | 3240 | `10.130.224.0/19` | 8,190 |

---

#### 10.140.0.0/16 - KRANJ (Gorenjska)

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Kranj | 4000 | `10.140.0.0/18` | 16,382 |
| Škofja Loka | 4220 | `10.140.64.0/18` | 16,382 |
| Tržič | 4290 | `10.140.128.0/19` | 8,190 |
| Radovljica | 4240 | `10.140.160.0/19` | 8,190 |
| Bled | 4260 | `10.140.192.0/19` | 8,190 |
| Jesenice | 4270 | `10.140.224.0/19` | 8,190 |

---

#### 10.160.0.0/16 - KOPER (Obala)

| Grad | Pošta | Subnet | Kapacitet |
|------|-------|--------|-----------|
| Koper | 6000 | `10.160.0.0/18` | 16,382 |
| Izola | 6310 | `10.160.64.0/19` | 8,190 |
| Piran | 6330 | `10.160.96.0/19` | 8,190 |
| Portorož | 6320 | `10.160.128.0/19` | 8,190 |
| Sežana | 6210 | `10.160.160.0/19` | 8,190 |
| Postojna | 6230 | `10.160.192.0/18` | 16,382 |

---

## Quick Reference Card

### Kako izračunati IP iz poštanskog broja?

#### 🇭🇷 Hrvatska (5-znamenkasta pošta)

```
Pošta:    31400 (Đakovo)
          ──
          │
          └──► 10.31.0.0/16

Jednostavno: 10.[prve 2 znamenke].0.0/16
```

#### 🇸🇮 Slovenija (4-znamenkasta pošta)

```
Pošta:    2000 (Maribor)
          ──
          │
          └──► 10.1[20].0.0/16 = 10.120.0.0/16

Formula: 10.(100 + prve 2 znamenke).0.0/16
```

---

## Subnet Allocation Policy

### Self-Service Limits

| Veličina | Kapacitet | Self-service? | Odobrenje |
|----------|-----------|---------------|-----------|
| /30 | 2 IP | ✅ Da | Automatski |
| /29 | 6 IP | ✅ Da | Automatski |
| /28 | 14 IP | ✅ Da | Automatski |
| /27 | 30 IP | ❌ Ne | Lokalni šerif |
| /26 | 62 IP | ❌ Ne | Lokalni šerif |
| /25 | 126 IP | ❌ Ne | Regionalni admin |
| /24 | 254 IP | ❌ Ne | Nacionalni admin |

### Per-Node Allocation

```
Tipična /28 alokacija za jedan node:

10.31.47.0/28
├── 10.31.47.0    Network address (reserved)
├── 10.31.47.1    Gateway (router)
├── 10.31.47.2    Router management
├── 10.31.47.3-14 DHCP pool (12 clients)
└── 10.31.47.15   Broadcast (reserved)
```

---

## Reserved Ranges

### Special Purpose Allocations

| Raspon | Namjena |
|--------|---------|
| `10.0.0.0/16` | Backbone infrastructure |
| `10.1.0.0/16` | Management network |
| `10.2.0.0/16` | Monitoring systems |
| `10.200.0.0/16` | VPN concentrators |
| `10.255.0.0/16` | Anycast services |

### Future Expansion

| Raspon | Rezervirano za |
|--------|----------------|
| `10.60-99.0.0/16` | Hrvatska - buduće regije |
| `10.170.0.0/16` | Slovenija - regija 7 (ako se uvede) |
| `10.200-254.0.0/16` | Nove države / posebne namjene |

---

## Implementation Checklist

### Phase 1: Initial Setup
- [ ] Kreirati projekt "Croatia" s poolom `10.10.0.0/8`
- [ ] Kreirati projekt "Slovenia" kao child s poolom `10.110-190.0.0`
- [ ] Definirati 20 HR regija kao sub-projekte
- [ ] Definirati 8 SI regija kao sub-projekte
- [ ] Postaviti šerife za svaku regiju

### Phase 2: Migration
- [ ] Migrirati postojeće nodeove u odgovarajuće regije
- [ ] Verificirati IP alokacije
- [ ] Ažurirati DNS zapise
- [ ] Testirati routing između regija

### Phase 3: Governance
- [ ] Implementirati slider UI za alokaciju
- [ ] Aktivirati sheriff approval workflow
- [ ] Postaviti notifikacije
- [ ] Dokumentirati procedure

---

## Summary Statistics

| Metrika | Hrvatska | Slovenija | Ukupno |
|---------|----------|-----------|--------|
| Broj regija | 20 | 8 | 28 |
| IP adresa | 1,310,680 | 524,280 | 1,834,960 |
| Max routera | ~65,000 | ~26,000 | ~91,000 |
| Max klijenata | ~1,200,000 | ~500,000 | ~1,700,000 |

---

## Related Documents

- #010 - Project Hierarchy and Node Migration
- #011 - IP Pool Slider with Sheriff Approval
- #008 - WireGuard VPN Support

---

## Changelog

| Datum | Verzija | Promjena |
|-------|---------|----------|
| 2024-12-14 | 1.0 | Initial version |
