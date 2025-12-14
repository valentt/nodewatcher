# Technical Note #007: Django Admin CSS Override

**Type:** Technical Documentation
**Created:** 2024-12-14
**Status:** Resolved

---

## Problem

Django admin panel had:
1. Left-aligned layout instead of centered
2. Narrow content area with excessive white space
3. Custom CSS rules were being ignored

---

## Root Cause

Django admin's default CSS uses specific selectors that have higher specificity than simple ID selectors. Our custom styles were being overridden.

**Django default behavior:**
```css
/* Django's admin CSS */
#container {
    /* various styles */
}
```

**Our initial attempt (FAILED):**
```css
#container {
    width: 90% !important;
    margin: 0 auto !important;
}
```

Even with `!important`, Django's styles were winning due to:
1. CSS load order (Django's CSS loaded after ours in some cases)
2. Other inherited styles affecting layout
3. Float and positioning rules interfering

---

## Solution

Use **higher specificity selectors** by chaining body with the element IDs:

```css
/* WORKING - Higher specificity */
body #container,
#container {
    width: 90% !important;
    max-width: 1600px !important;
    min-width: 800px !important;
    margin: 0 auto !important;
    padding: 0 !important;
    float: none !important;
    background: transparent !important;
}

body #container #content,
#content {
    width: 100% !important;
    max-width: 100% !important;
    padding: 20px !important;
    margin: 0 !important;
    float: none !important;
}

body #container #content #content-main,
#content-main {
    width: 100% !important;
    max-width: 100% !important;
    float: none !important;
}
```

**Key fixes:**
1. `body #container` has higher specificity than just `#container`
2. `float: none !important` removes any float interference
3. Chain selectors for nested elements (`body #container #content`)
4. Duplicate selectors (with and without body) for extra coverage

---

## CSS Specificity Reference

| Selector | Specificity |
|----------|-------------|
| `#container` | 0,1,0,0 |
| `body #container` | 0,1,0,1 |
| `body #container #content` | 0,2,0,1 |

Higher specificity = wins in CSS cascade.

---

## Files Modified

- `nodewatcher/core/static/admin/css/custom.css`

---

## Lessons Learned

1. When overriding framework CSS, always use higher specificity selectors
2. `!important` alone is often not enough
3. Check for `float` properties that can break centering
4. Test with browser DevTools to see which rules are being applied/overridden

---

## Related

- Django Admin customization docs
- CSS Specificity calculator: https://specificity.keegan.st/
