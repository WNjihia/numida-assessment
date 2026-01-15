# Numida Test Plan Document

## 1. Overview

| Item | Details |
|------|---------|
| **Feature** | First-Time Loan Application |
| **Environment(s)** | Local (Docker) |
| **Related Docs** | SPEC.md, QUICK_START.md, README.md |

## 2. Objective

To validate that first-time users can successfully:
- Authenticate using phone number + OTP
- Submit accurate personal and loan details
- Receive and clearly understand a loan decision

This plan ensures functional correctness, data validation, API/UI consistency, and basic risk coverage before release.

## 3. Scope

### In Scope
- First-time loan application flow
- Phone + OTP authentication
- Personal details capture
- Loan details capture
- Loan decision & summary
- UI and API validation
- Automated smoke, regression, and E2E tests

### Out of Scope

| Feature | Reason |
|---------|--------|
| Repeat loan applications | Out of scope per SPEC |
| Loan repayment flows | Out of scope per SPEC |
| Admin / back-office features | Out of scope per SPEC |
| Performance and load testing | Future phase |
| Fraud detection logic | Beyond basic validation |
| Payment / disbursement | Out of scope per SPEC |

## 4. Assumptions & Dependencies

- **OTP is hardcoded to 0000**: Non-production environment only.
- **Test data resets on server restart**: In-memory storage.
- **Loan decision logic is deterministic**: Based on amount and age.
- **SMS delivery is mocked**: OTP not actually sent.
- **Unique phone numbers per test**: Prevents duplicate application errors.

## 5. User Stories & Test Coverage

### Story 1: User Authentication

> As a user, I want to log in with my phone number and OTP so that I can access the loan application.

| Acceptance Criteria | UI | API | Status |
|---------------------|:--:|:---:|--------|
| Request OTP with valid phone number | Y | Y | Done |
| Invalid phone format shows validation error | Y | Y | Done |
| Empty phone number rejected | Y | Y | Done |
| Valid OTP grants access | Y | Y | Done |
| Invalid OTP shows error message | Y | Y | Done |
| Can navigate back from OTP screen | Y | - | Done |
| Session token created after successful login | - | Y | Done |

### Story 2: Personal Details

> As a user, I want to enter my personal information so that I can apply for a loan.

| Acceptance Criteria | UI | API | Status |
|---------------------|:--:|:---:|--------|
| Can submit valid personal details | Y | Y | Done |
| Full name required (min 2 characters) | Y | Y | Done |
| National ID required (min 5 characters) | Y | Y | Done |
| National ID must be unique | - | - | GAP-003 |
| Must be 18+ years old | Y | Y | Done |

## 6. Test Types & Strategy

| Test Type | Description | Tooling | Run Frequency |
|-----------|-------------|---------|---------------|
| Smoke | Critical happy paths | `pytest -m smoke` | Every commit |
| UI E2E | Full user journeys | pytest-bdd + Playwright | PR, Deploy |
| API Tests | Validation & business rules | pytest + requests | PR, Deploy |
| Regression | All automated suites | pytest | Before release |
| Exploratory | Edge cases & UX | Manual | Each sprint |

## 7. Test Data Strategy

- **Phone numbers**: Randomly generated per test (prevents duplicates)
- **OTP**: Static: `0000`
- **Personal details**: Fixture-based defaults in conftest.py
- **Loan amounts**: Varied for decision logic testing

## 8. Known Bugs & Gaps

| ID | Summary | Severity | Status |
|----|---------|----------|--------|
| GAP-001 | Loan amount limits (1000-5000000) not in SPEC | Medium | Documented |
| GAP-003 | National ID uniqueness not enforced | High | Documented |
| GAP-004 | "Rejected" status never returned | High | Documented |
| BUG-001 | OTP comparison is case-insensitive | Low | Open |
| BUG-002 | No code path to "rejected" decision | High | Open |

## 9. Definition of Done

- Acceptance criteria covered by automated tests
- Smoke tests passing in CI
- Regression suite executed
- Bugs & gaps documented in BUGS_AND_GAPS.md
- QA sign-off provided
