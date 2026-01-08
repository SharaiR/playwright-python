# TAF (Playwright + Python) for saucedemo.com

[![CI](https://github.com/SharaiR/playwright-python/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SharaiR/playwright-python/actions/workflows/ci.yml)
[![pages-build-deployment](https://github.com/SharaiR/playwright-python/actions/workflows/pages/pages-build-deployment.yml/badge.svg)](https://github.com/SharaiR/playwright-python/actions/workflows/pages/pages-build-deployment.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/pypi/v/playwright.svg?label=playwright)](https://pypi.org/project/playwright/)
[![pytest](https://img.shields.io/badge/tested_with-pytest-green.svg)](https://docs.pytest.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/)
[![flake8](https://img.shields.io/badge/lint-flake8-lightgrey.svg)](https://flake8.pycqa.org/)
![parallel](https://img.shields.io/badge/parallel-pytest--xdist-yellowgreen)
![coverage](https://img.shields.io/endpoint?url=https://SharaiR.github.io/playwright-python/coverage.json)
[![Allure](https://img.shields.io/badge/report-Allure-ff69b4)](https://SharaiR.github.io/playwright-python/)

> ✨ UI Test Automation Framework: **Python 3.13+**, **Playwright**, **Pytest**, **Allure**, typed layers, DI, logging, videos & screenshots on failure, GitHub Actions CI + GitHub Pages (Allure + coverage badge).

---

## 🔧 Stack
- Python 3.13+
- Playwright
- Pytest (+ xdist, rerunfailures, cov)
- Allure + pytest-html
- Logging for every action
- Type hints + mypy
- pre-commit (Black, Flake8, MyPy)
- dotenv (.env secrets)
- GitHub Actions (CI + Pages)
- DI (simple container), PageObjects, Services

## 📁 Project layout
```
.
├── .env.example
├── Makefile
├── pyproject.toml
├── pytest.ini
├── src/taf/...
└── tests/e2e/...
```

---

## 🏁 Local setup

### 1) Clone and configure
```bash
git clone https://github.com/SharaiR/playwright-python.git
cd playwright-python
cp .env.example .env               # edit BROWSER/HEADLESS/creds if needed
```

### 2) Install
```bash
pip install poetry
poetry install

make install                       # creates .venv, installs dependencies and the chromium browser

# or manually:
python3 -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
pip install install-playwright
python3 -m playwright install chromium
python3 -m playwright install firefox webkit
```

### 3) Run tests
#### Basic run (headless, chromium)
```bash
make test
```

#### Choose browser / headed / test set
```bash
# browser: chromium | firefox | webkit
pytest --browser=firefox

# headed mode (browser window visible)
pytest --headed

# force headless (overrides .env)
pytest --headless

# test type: all | smoke | regression
pytest --test-type=smoke
pytest --test-type=regression

# combine
pytest --browser=webkit --headed --test-type=regression -n auto
```

#### With markers manually
```bash
pytest -m "smoke"
pytest -m "regression and ui"
```

#### Parallel run
```bash
# requires pytest-xdist (installed via pip install -e .[dev])
pytest -n auto
```

#### Allure
```bash
# results are saved to artifacts/allure-results (automatically via addopts)
pytest --browser=firefox

# open interactive report
 # requires Allure CLI (e.g., brew install allure)
allure serve artifacts/allure-results

# or generate a static report
allure generate artifacts/allure-results -o artifacts/allure-report --clean
```

### 4) Local reports
- **pytest-html**: `artifacts/report.html` (generated automatically via `--html`)
- **Allure**:
  ```bash
  allure serve artifacts/allure-results
  ```
- **Coverage**:
  ```bash
  pytest --cov=src --cov-report=xml:artifacts/coverage.xml
  python tools/coverage_badge.py artifacts/coverage.xml site/coverage.json
  ```

---

## 🤖 CI (GitHub Actions)

### Workflows
- **CI** — `.github/workflows/ci.yml`

  - Parallel run (`-n auto`)

  - **Auto-restart failed tests once**: `--reruns 1 --reruns-delay 1`

  - Generates `artifacts/coverage.xml`, attaches artifacts (video, screenshots, HTML report)

- **Pages** — `.github/workflows/pages/pages-build-deployment.yml`

  - Run tests with `--reruns 1` and `--alluredir`

  - Build **Allure HTML** and publish to **GitHub Pages**

  - Generate `site/coverage.json` for the `coverage` badge


### GitHub secrets (optional)
- `STANDARD_USER` — default `standard_user`

- `LOCKED_OUT_USER` — default `locked_out_user`

- `PASSWORD` — default `secret_sauce`


### CI run customization
- Browser:

  ```yaml
  - name: Run tests
    run: pytest --browser=firefox -n auto --reruns 1 --reruns-delay 1
  ```
- Test subsets:

  ```yaml
  - name: Smoke only
    run: pytest --test-type=smoke -n auto --reruns 1 --reruns-delay 1
  ```
- Headed (usually not needed in CI):

  ```yaml
  - name: Headed
    run: pytest --headed -n auto --reruns 1 --reruns-delay 1
  ```

> Reports and coverage are generated **after** the retry — reruns are built into the pytest command.

---

## 🧩 Useful commands
```bash
make fmt        # Black
make lint       # Flake8 + mypy
make test       # pytest (headless)
make ci         # pytest + coverage xml + reruns
make browsers   # install Playwright browsers and dependencies
```

## 🔐 .env
See `.env.example` — BASE_URL, BROWSER, HEADLESS, artifact paths, and public creds.

---

## License
Distributed under the [MIT License](LICENSE).

## 👤 Author
**Raman Sharai**
