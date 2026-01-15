# Test Suite for First-Time Loan Application

Automated test suite covering API and UI testing for the loan application system.


## Setup

### Prerequisites

- Python 3.9+
- Docker (for running the application)

### 1. Start the Application

```bash
cd quality-assurance
docker compose up --build
```

This starts:
- API server at `http://localhost:5001`
- Web app at `http://localhost:5173`

### 2. Create Virtual Environment

```bash
python3 -m venv numida-env
source numida-env/bin/activate  # On Windows: numida-env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r tests/requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run Specific Test Suites

```bash
# API tests only
pytest tests/api/

# UI tests only
pytest tests/ui/

# Specific test file
pytest tests/api/test_auth.py
pytest tests/ui/step_defs/test_login.py
```

### Run with Tags

Feature files support tags for filtering tests:

```bash
# Skip tests marked with @skip
pytest tests/ -m "not skip"

# Run only skipped tests (to check if bugs are fixed)
pytest tests/ -m "skip"

# Run tests by custom tags (if defined in feature files)
pytest tests/ -k "login"
pytest tests/ -k "decision"
```

### Run with HTML Report

```bash
pip install pytest-html
pytest tests/ --html=report.html --self-contained-html
```

### Run in Headed Mode (UI Tests)

```bash
pytest tests/ui/ --headed
```

### Run with Specific Browser

```bash
pytest tests/ui/ --browser chromium
pytest tests/ui/ --browser firefox
pytest tests/ui/ --browser webkit
```

## Design Rationale

### API Tests

**Framework:** pytest + requests

**Why this approach:**
- **Simplicity**: requests library is lightweight and intuitive for HTTP testing
- **Speed**: API tests run in ~1 second, providing fast feedback
- **Independence**: Each test uses unique phone numbers via fixtures to avoid state conflicts
- **Parametrization**: Used `@pytest.mark.parametrize` for data-driven tests (e.g., valid loan terms)

**Test Organization:**
- `TestApplicationStatus` - GET /api/application/status
- `TestApplicationSubmit` - POST /api/application/submit
- `TestApplicationValidation` - Field validation tests
- `TestLoanDecisionLogic` - Decision outcome tests (approved/pending)
- `TestRequestOTP` / `TestVerifyOTP` - Authentication flow

### UI Tests

**Framework:** pytest-bdd + Playwright

**Why BDD (Behavior-Driven Development):**
- **Readable specs**: Gherkin feature files serve as living documentation
- **Stakeholder communication**: Non-technical team members can read/write scenarios
- **Traceability**: Each scenario maps directly to a business requirement

**Why Playwright:**
- **Modern architecture**: Auto-waiting, reliable selectors
- **Cross-browser**: Chromium, Firefox, WebKit support
- **Fast execution**: Parallel test execution capability

**Page Object Model (POM):**
- **Encapsulation**: UI selectors and actions are centralized in page classes
- **Maintainability**: Selector changes only require updates in one place
- **Reusability**: Common actions (login, form submission) are reusable across tests

### Fixture Strategy

**`test_phone` fixture:**
- Generates unique random phone numbers for each test
- Prevents test pollution from existing application data
- Enables parallel test execution without conflicts

**`auth_headers` fixture:**
- Creates authenticated session automatically
- Reduces boilerplate in tests requiring authentication

**`valid_application_data` fixture:**
- Provides consistent test data across tests
- Single source of truth for valid form values

### Test Isolation

Each test is designed to be:
- **Independent**: No dependencies on other tests
- **Repeatable**: Same result on every run
- **Self-contained**: Creates its own test data

This is achieved by:
1. Using unique phone numbers per test (not fixed values)
2. Server stores data in-memory (resets on restart)
3. No shared state between tests


## Known Issues

See [BUGS_AND_GAPS.md](BUGS_AND_GAPS.md) for documented bugs and specification gaps discovered during testing.
