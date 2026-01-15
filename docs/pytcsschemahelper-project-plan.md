# pytcsschemahelper — Project Plan

## Overview

| Item | Detail |
|------|--------|
| **Project** | pytcsschemahelper |
| **Goal** | Create a pip-installable library for generating TCS-compliant JSON documents |
| **License** | CC0 1.0 Universal |
| **Estimated Duration** | 6-8 weeks (part-time) / 3-4 weeks (full-time) |

---

## Phase 1: Project Setup
**Duration:** 2-3 days

### 1.1 Repository Setup
- [x] Create GitHub repository `pytcsschemahelper`
- [x] Add CC0 LICENSE file
- [x] Create initial README.md with project description
- [x] Set up `.gitignore` (Python template)

### 1.2 Project Configuration
- [x] Create `pyproject.toml` with:
  - Project metadata (name, version, description, authors)
  - CC0-1.0 license
  - Python version requirements (>=3.9)
  - Dependencies (pydantic, jsonschema, python-dateutil, typing-extensions)
  - Optional dependencies (cli, dev, docs)
  - Build system configuration (hatchling or setuptools)
- [x] Create `src/pytcsschemahelper/__init__.py` with version
- [x] Add `py.typed` marker for PEP 561

### 1.3 Development Environment
- [x] Create `requirements-dev.txt` or use pyproject.toml extras
- [x] Set up pre-commit hooks (`.pre-commit-config.yaml`):
  - ruff (linting + formatting)
  - mypy (type checking)
- [x] Create `ruff.toml` configuration
- [x] Create `mypy.ini` configuration

### 1.4 CI/CD Pipeline
- [x] Create `.github/workflows/ci.yml`:
  - Run tests on Python 3.9, 3.10, 3.11, 3.12, 3.13
  - Run linting and type checking
  - Generate coverage report
- [x] Create `.github/workflows/release.yml`:
  - Build package on tag
  - Publish to PyPI

**Milestone 1:** ✓ Empty installable package with CI pipeline

---

## Phase 2: Core Models
**Duration:** 5-7 days

### 2.1 Version Enums & Constants
- [ ] Create `src/pytcsschemahelper/versions.py`:
  - `ReportingOrgVersion` enum
  - `EmissionsReportVersion` enum
  - `TCSVersion` enum
  - Default version constants
  - Version compatibility matrix

### 2.2 Exception Classes
- [ ] Create `src/pytcsschemahelper/exceptions.py`:
  - `TCSError` (base)
  - `TCSValidationError`
  - `TCSVersionError`
  - `TCSCompatibilityError`
  - `TCSMigrationError`
  - `TCSParseError`

### 2.3 Base Emission Models
- [ ] Create `src/pytcsschemahelper/models/base.py`:
  - `Scope2Method` enum
  - `Emissions` model
  - `Scope2Emissions` model

### 2.4 Emission Category Models
- [ ] Create `src/pytcsschemahelper/models/emissions.py`:
  - `UpstreamEmissions` model
  - `DirectEmissions` model
  - `IndirectEmissions` model
  - `DownstreamEmissions` model

### 2.5 Organisation & Report Models
- [ ] Create `src/pytcsschemahelper/models/organisation.py`:
  - `Organisation` model
- [ ] Create `src/pytcsschemahelper/models/report.py`:
  - `ReportingPeriod` model (with date validation)
  - `VerificationType` enum
  - `DocType` enum
  - `Disclosure` model
  - `TechCarbonStandard` model
  - `EmissionsReport` model (with auditor_link validation)

### 2.6 Root Document Model
- [ ] Create `src/pytcsschemahelper/models/document.py`:
  - `TCSDocument` model
  - `to_json()` method
  - `to_dict()` method
  - `save()` method
  - `from_json()` class method
  - `load()` class method
  - `from_url()` class method

### 2.7 Public Exports
- [ ] Update `src/pytcsschemahelper/models/__init__.py` with all exports
- [ ] Update `src/pytcsschemahelper/__init__.py` with public API

### 2.8 Unit Tests for Models
- [ ] Create `tests/test_models/test_base.py`
- [ ] Create `tests/test_models/test_emissions.py`
- [ ] Create `tests/test_models/test_organisation.py`
- [ ] Create `tests/test_models/test_report.py`
- [ ] Create `tests/test_models/test_document.py`
- [ ] Create test fixtures in `tests/fixtures/`

**Milestone 2:** ✓ All models implemented with >90% test coverage

---

## Phase 3: Builder API
**Duration:** 3-4 days

### 3.1 Builder Implementation
- [ ] Create `src/pytcsschemahelper/builder.py`:
  - `TCSBuilder` class
  - `organisation()` method
  - `add_report()` method
  - `upstream()` method
  - `direct()` method
  - `indirect()` method
  - `downstream()` method
  - `add_disclosure()` method
  - `build()` method
  - Internal `_finalize_current_report()` method
  - Date parsing helper

### 3.2 Convenience Functions
- [ ] Add `quick_report()` function for minimal documents

### 3.3 Builder Tests
- [ ] Create `tests/test_builder.py`:
  - Test minimal document creation
  - Test full document creation
  - Test multiple reports
  - Test validation errors
  - Test method chaining

**Milestone 3:** ✓ Builder API complete with tests

---

## Phase 4: Validation
**Duration:** 3-4 days

### 4.1 JSON Schema Validation
- [ ] Create `src/pytcsschemahelper/validation/__init__.py`
- [ ] Create `src/pytcsschemahelper/validation/schema.py`:
  - `ValidationResult` class
  - `ValidationError` class
  - `ValidationWarning` class
  - `validate_against_schema()` function
  - Schema URL constants
  - Schema fetching/caching logic

### 4.2 Custom Validators
- [ ] Create `src/pytcsschemahelper/validation/validators.py`:
  - `validate_version_compatibility()` — check nested versions are valid
  - `validate_emissions_completeness()` — check category coverage
  - `validate_date_coverage()` — check for gaps between reports

### 4.3 Validation Tests
- [ ] Create `tests/test_validation/test_schema.py`
- [ ] Create `tests/test_validation/test_validators.py`
- [ ] Create invalid fixture files for testing

**Milestone 4:** ✓ Validation system complete

---

## Phase 5: Serialization & Utilities
**Duration:** 2-3 days

### 5.1 Utility Functions
- [ ] Create `src/pytcsschemahelper/utils.py`:
  - `calculate_total_emissions()` — sum all emissions
  - `calculate_category_totals()` — breakdown by category
  - `aggregate_reports()` — combine multiple reports

### 5.2 Serialization Tests
- [ ] Create `tests/test_serialization.py`:
  - Test JSON roundtrip
  - Test date formatting
  - Test exclude_none behavior
  - Test file save/load

### 5.3 Utility Tests
- [ ] Create `tests/test_utils.py`

**Milestone 5:** ✓ Utilities complete

---

## Phase 6: Version Migration
**Duration:** 2-3 days

### 6.1 Migration Logic
- [ ] Create `src/pytcsschemahelper/migration/__init__.py`
- [ ] Create `src/pytcsschemahelper/migration/migrators.py`:
  - `MigrationPath` class
  - `migrate_document()` function
  - Version-specific migration functions
  - `VERSION_CHANGES` documentation dict

### 6.2 Migration Tests
- [ ] Create `tests/test_migration.py`:
  - Test TCS v0.0.2 → v0.1.0 (field renames)
  - Test emissions report migrations
  - Test reporting org migrations

**Milestone 6:** ✓ Migration system complete

---

## Phase 7: CLI (Optional)
**Duration:** 2-3 days

### 7.1 CLI Implementation
- [ ] Create `src/pytcsschemahelper/cli/__init__.py`
- [ ] Create `src/pytcsschemahelper/cli/commands.py`:
  - `validate` command
  - `totals` command
  - `migrate` command
  - `fetch` command
  - `init` command (interactive)
- [ ] Add CLI entry point to `pyproject.toml`

### 7.2 CLI Tests
- [ ] Create `tests/test_cli.py` using Click's test runner

**Milestone 7:** ✓ CLI complete

---

## Phase 8: Documentation
**Duration:** 3-4 days

### 8.1 README
- [x] Write comprehensive README.md:
  - Badges (PyPI, CI, coverage)
  - Installation instructions
  - Quick start example
  - Feature overview
  - Links to documentation

### 8.2 Documentation Site
- [ ] Set up MkDocs with Material theme
- [ ] Create `docs/index.md` — overview
- [ ] Create `docs/getting-started.md` — tutorial
- [ ] Create `docs/api-reference.md` — auto-generated from docstrings
- [ ] Create `docs/schema-versions.md` — version documentation
- [ ] Create `docs/migration-guide.md` — upgrading documents
- [ ] Create `docs/examples.md` — real-world examples
- [ ] Configure `mkdocs.yml`
- [ ] Set up GitHub Pages or ReadTheDocs deployment

### 8.3 Docstrings
- [ ] Ensure all public functions/classes have Google-style docstrings
- [ ] Add usage examples in docstrings

**Milestone 8:** ✓ Documentation complete

---

## Phase 9: Release Preparation
**Duration:** 2-3 days

### 9.1 Final Polish
- [ ] Review and update CHANGELOG.md
- [ ] Verify all tests pass on all Python versions
- [ ] Verify type checking passes
- [ ] Verify linting passes
- [ ] Check test coverage ≥90%
- [ ] Test package installation in clean environment

### 9.2 PyPI Setup
- [ ] Create PyPI account (if needed)
- [ ] Configure PyPI trusted publisher for GitHub Actions
- [ ] Test release to TestPyPI

### 9.3 Initial Release
- [ ] Tag version 0.1.0
- [ ] Create GitHub release with notes
- [ ] Verify PyPI publication
- [ ] Verify `pip install pytcsschemahelper` works

**Milestone 9:** ✓ v0.1.0 released on PyPI

---

## Task Summary

| Phase | Tasks | Est. Days |
|-------|-------|-----------|
| 1. Project Setup | 12 | 2-3 |
| 2. Core Models | 24 | 5-7 |
| 3. Builder API | 8 | 3-4 |
| 4. Validation | 9 | 3-4 |
| 5. Utilities | 6 | 2-3 |
| 6. Migration | 5 | 2-3 |
| 7. CLI (Optional) | 5 | 2-3 |
| 8. Documentation | 12 | 3-4 |
| 9. Release | 8 | 2-3 |
| **Total** | **89** | **25-34** |

---

## Recommended Task Order

```
Week 1:  Phase 1 (Setup) → Phase 2 (Models - start)
Week 2:  Phase 2 (Models - finish) → Phase 3 (Builder)
Week 3:  Phase 4 (Validation) → Phase 5 (Utilities)
Week 4:  Phase 6 (Migration) → Phase 7 (CLI)
Week 5:  Phase 8 (Documentation)
Week 6:  Phase 9 (Release) → Buffer
```

---

## Dependencies Between Phases

```
Phase 1 (Setup)
    ↓
Phase 2 (Models) ──────────────────┐
    ↓                              │
Phase 3 (Builder)                  │
    ↓                              ↓
Phase 4 (Validation) ←─────── Phase 5 (Utilities)
    ↓
Phase 6 (Migration)
    ↓
Phase 7 (CLI) ← requires all above
    ↓
Phase 8 (Documentation) ← requires all above
    ↓
Phase 9 (Release)
```

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| TCS schema updates during development | Medium | Pin to current versions, add update task post-release |
| Pydantic v2 complexity | Low | Use official migration guide, extensive testing |
| JSON Schema validation edge cases | Medium | Test against official TCS examples, add regression tests |
| PyPI publishing issues | Low | Test with TestPyPI first, use trusted publishers |

---

## Success Criteria

- [ ] `pip install pytcsschemahelper` works
- [ ] Library generates valid TCS JSON documents
- [ ] Documents validate against official TCS schemas
- [ ] All schema versions (0.0.1 → latest) supported
- [ ] Test coverage ≥90%
- [ ] Type checking passes (mypy)
- [ ] Documentation published and accessible
- [ ] At least one real-world example in docs

---

## Post-Release Roadmap

**v0.2.0**
- Async URL fetching
- Schema caching
- Additional convenience functions

**v0.3.0**
- Report generation (HTML/PDF summaries)
- Diff tool for comparing documents

**v1.0.0**
- Stable API guarantee
- Framework integrations (Django, FastAPI)
- Carbon calculation helpers

---

*Plan Version: 1.0*
*Created: December 2024*
