# Bugs and Gaps Report

## Summary

| Category | Count |
|----------|-------|
| Spec vs Implementation Gaps | 6 |
| Potential Bugs | 5 |
| Open Questions | 4 |

---

## Spec vs Implementation Gaps

### GAP-001: Loan amount validation stricter than documented
- **SPEC says:** "Loan amount must be greater than zero"
- **API does:** Min 1000, Max 5000000
- **Severity:** Medium
- **Location:** `app.py` lines 18-19, 187-196

### GAP-002: Loan terms not specified in SPEC
- **SPEC says:** "one of the supported values" (unspecified)
- **API does:** 15, 30, 45, 60 days only
- **Severity:** Low
- **Location:** `app.py` line 20

### GAP-003: National ID uniqueness not enforced
- **SPEC says:** "Must be unique"
- **API does:** Only checks length >= 5, no uniqueness validation
- **Severity:** High
- **Location:** `app.py` lines 53-55

### GAP-004: "Rejected" status never returned
- **SPEC says:** Decision can be Approved / Rejected / Pending
- **API does:** Only returns "approved" or "pending", never "rejected"
- **Severity:** High
- **Location:** `app.py` lines 218-228

**Current decision logic:**
```python
if loan_amount >= 1000000:
    decision_status = "pending"
elif age >= 60:
    decision_status = "pending"
elif loan_amount < 50000 and age >= 25 and age < 60:
    decision_status = "approved"
else:
    decision_status = "approved"  # Default - no path to "rejected"
```

### GAP-005: Duplicate submission logic inconsistent
- **SPEC says:** "Duplicate submissions should be prevented"
- **API does:** Only blocks if existing status is "approved" or "pending"
- **Severity:** Medium
- **Location:** `app.py` lines 152-156

### GAP-006: Phone number validation rules not specified
- **SPEC says:** "Phone number must be in a valid format (as defined by the application)"
- **API does:** Requires 9-15 digits after removing +, spaces, and dashes
- **Severity:** Low
- **Impact:** Testers/users have no clear guidance on what phone formats are acceptable
- **Location:** `app.py` lines 23-30

---

## Potential Bugs

### BUG-001: Users under 18 can proceed past personal details form
- **Description:** UI relies on browser date validation, doesn't calculate age
- **Impact:** Medium - User submits form, then gets API error — poor UX
- **Expected:** UI should validate age >= 18 before allowing submission

### BUG-002: Short full name accepted by UI
- **Description:** UI only checks `required`, not minimum 2 characters
- **Impact:** Medium - User submits form, then gets API error - poor UX
- **Expected:** UI should validate min length before submission

### BUG-003: UI does not display validation error for zero loan amount
- **Description:** When user enters "0" as loan amount and submits, the UI does not display an error message. The API correctly returns error "Loan amount must be greater than zero" but the frontend doesn't show it to the user.
- **Impact:** Medium - poor user experience, user gets no feedback on invalid input
- **Location:** Frontend loan details form (error message element not rendered)
- **Related test:** `test_user_cannot_proceed_with_zero_loan_amount` (skipped)

### BUG-004: Data not persistent
- **Description:** In-memory storage resets on server restart
- **Impact:** Medium — expected for test environment but not documented
- **Location:** `app.py` lines 11-14

### BUG-005: OTP comparison is case-insensitive
- **Description:** OTP check uses `.lower()` comparison
- **Impact:** Low (doesn't affect "0000" but inconsistent behavior)
- **Location:** `app.py` line 101

### Browser vs API Validation Summary

| Field | Browser Validation | API Validation | Gap? |
|-------|-------------------|----------------|:----:|
| Full name | `required` only | Min 2 characters | ⚠️ |
| National ID | `required` only | Min 5 characters | ⚠️ |
| Email | `type="email"` | Regex pattern | ✅ |
| Date of birth | `type="date"` | Format + age >= 18 | ⚠️ |
| Loan amount | `type="number"` | Range 1000-5000000 | ⚠️ |
| Loan term | `<select>` dropdown | Must be 15/30/45/60 | ✅ |
| Purpose | `required` only | Non-empty string | ✅ |

- **Impact:** Users can submit invalid data that passes browser validation but fails API validation, resulting in poor user experience.
- **Related Bugs:** BUG-001, BUG-002, BUG-003

---

## Open Questions (from SPEC)

These were intentionally unanswered in the SPEC. Here's what testing revealed:

| Question | Observed Behavior |
|----------|-------------------|
| What happens if the user abandons the flow halfway? | Session persists in memory. No partial application saved. User can log in again and start fresh. |
| How are retries handled? | No retry limits. OTP can be requested unlimited times for the same phone number. |
| Are there rate limits? | None implemented. Potential security risk for OTP abuse. |
| What happens if the same National ID is reused? | Allowed. No uniqueness validation exists (see GAP-003). |

---

## Suggestions for Improvement

### IMP-001: Add data-testid attributes
- **Current:** Locators rely on IDs, classes, and text selectors
- **Suggested:** Add `data-testid` attributes to all interactive elements
- **Benefit:** More stable test automation, decoupled from styling changes
- **Priority:** Medium

**Example:**
```html
<!-- Before -->
<button class="btn-primary">Submit</button>

<!-- After -->
<button class="btn-primary" data-testid="submit-button">Submit</button>
```

### IMP-002: Disable submit buttons when form is invalid
- **Current:** Submit buttons always enabled, validation happens on click
- **Suggested:** Disable submit button until all required fields are valid
- **Benefit:** Prevents unnecessary API calls, better UX, clearer feedback
- **Priority:** Low

### IMP-003: Add custom validation error messages
- **Current:** Relies on native browser validation tooltips (e.g., "Please fill in this field")
- **Suggested:** Display inline error messages below each field
- **Benefit:** Consistent UX across browsers, more descriptive errors, testable with automation
- **Affected Screens:** Login (phone input), OTP screen, Personal Details, Loan Details
- **Priority:** Medium
- **Note:** Native browser validation tooltips cannot be selected with Playwright locators, making them difficult to test

### IMP-004: Add rate limiting for OTP requests
- **Current:** No rate limiting implemented. OTP can be requested unlimited times for the same phone number.
- **Suggested:** Limit OTP requests (e.g., max 5 requests per phone number per hour)
- **Benefit:** Prevents brute-force attacks and OTP abuse
- **Priority:** High
- **Related:** See Open Questions - "Are there rate limits?"
