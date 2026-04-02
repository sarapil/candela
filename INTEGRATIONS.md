# 🔗 Candela — Integrations Guide

> **Domain:** Restaurant & F&B Management
> **Prefix:** CD

---

## Integration Map

```
Candela
  ├── ERPNext
  ├── CAPS
  ├── frappe_visual
  ├── POS Systems
```

---

## ERPNext

### Connection Type
- **Direction:** Bidirectional
- **Protocol:** Python API / REST
- **Authentication:** Frappe session / API key

### Data Flow
| Source | Target | Trigger | Data |
|--------|--------|---------|------|
| Candela | ERPNext | On submit | Document data |
| ERPNext | Candela | On change | Updated data |

### Configuration
```python
# In CD Settings or site_config.json
# erpnext_enabled = 1
```

---

## CAPS

### Connection Type
- **Direction:** Bidirectional
- **Protocol:** Python API / REST
- **Authentication:** Frappe session / API key

### Data Flow
| Source | Target | Trigger | Data |
|--------|--------|---------|------|
| Candela | CAPS | On submit | Document data |
| CAPS | Candela | On change | Updated data |

### Configuration
```python
# In CD Settings or site_config.json
# caps_enabled = 1
```

---

## frappe_visual

### Connection Type
- **Direction:** Bidirectional
- **Protocol:** Python API / REST
- **Authentication:** Frappe session / API key

### Data Flow
| Source | Target | Trigger | Data |
|--------|--------|---------|------|
| Candela | frappe_visual | On submit | Document data |
| frappe_visual | Candela | On change | Updated data |

### Configuration
```python
# In CD Settings or site_config.json
# frappe_visual_enabled = 1
```

---

## POS Systems

### Connection Type
- **Direction:** Bidirectional
- **Protocol:** Python API / REST
- **Authentication:** Frappe session / API key

### Data Flow
| Source | Target | Trigger | Data |
|--------|--------|---------|------|
| Candela | POS Systems | On submit | Document data |
| POS Systems | Candela | On change | Updated data |

### Configuration
```python
# In CD Settings or site_config.json
# pos_systems_enabled = 1
```

---

## API Endpoints

All integration APIs use the standard response format from `candela.api.response`:

```python
from candela.api.response import success, error

@frappe.whitelist()
def sync_data():
    return success(data={}, message="Sync completed")
```

---

*Part of Candela by Arkan Lab*
