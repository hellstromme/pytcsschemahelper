# pytcsschemahelper — Library Specification

## Executive Summary

This document specifies the design and implementation requirements for `pytcsschemahelper`, a Python library that enables developers to programmatically generate, validate, and manage Technology Carbon Standard (TCS) Schema documents conforming to the [TCS Implementation Guide](https://www.techcarbonstandard.org/schemas/implementation-guide).

---

## 1. Project Overview

### 1.1 Library Name
**`pytcsschemahelper`**

### 1.2 Purpose
Provide a Pythonic, type-safe interface for creating TCS-compliant JSON documents that organisations publish at their root domain (e.g., `https://example.com/tcs.json`) to report technology-related carbon emissions.

### 1.3 Target Audience
- Sustainability engineers and developers
- DevOps teams automating carbon reporting
- Data engineers building emission aggregation pipelines
- Organisations implementing TCS compliance

### 1.4 License
CC0 1.0 Universal (Public Domain Dedication)

The library is dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). No rights reserved — anyone can use, modify, and distribute the code for any purpose without restriction or attribution.

---

## 2. Distribution & Installation

### 2.1 Package Distribution
- **Primary**: PyPI (`pip install pytcsschemahelper`)
- **Repository**: GitHub with CI/CD via GitHub Actions
- **Documentation**: ReadTheDocs or GitHub Pages

### 2.2 Python Version Support
- **Minimum**: Python 3.9
- **Recommended**: Python 3.11+
- **Tested**: Python 3.9, 3.10, 3.11, 3.12, 3.13

### 2.3 Dependencies
```toml
[project]
name = "pytcsschemahelper"
license = "CC0-1.0"
classifiers = [
    "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering",
]

dependencies = [
    "pydantic>=2.0,<3.0",       # Data validation and serialization
    "jsonschema>=4.0,<5.0",     # JSON Schema validation
    "typing-extensions>=4.0",   # Extended typing support
    "python-dateutil>=2.8",     # Date parsing utilities
]

[project.optional-dependencies]
cli = [
    "click>=8.0,<9.0",          # CLI framework
    "rich>=13.0",               # Rich terminal output
]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0",
]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
    "mkdocstrings[python]>=0.24",
]
```

---

## 3. Schema Version Management

### 3.1 Supported Schema Versions

The library must support the complete TCS modular schema architecture with version-aware routing:

| Schema Component | Supported Versions | Latest |
|-----------------|-------------------|--------|
| Router Schema | - | index.json |
| Reporting Organisation | 0.0.1, 0.1.0, 0.1.1, 0.1.2 | 0.1.2 |
| Emissions Report | 0.0.1, 0.0.2, 0.0.3 | 0.0.3 |
| Tech Carbon Standard | 0.0.1, 0.0.2, 0.1.0 | 0.1.0 |

### 3.2 Version Compatibility Matrix

```
Router Schema 0.1.2 → Emissions Report 0.0.1, 0.0.2, 0.0.3
Router Schema 0.1.1 → Emissions Report 0.0.1, 0.0.2
Router Schema 0.1.0 → Emissions Report 0.0.1, 0.0.2
Router Schema 0.0.1 → Emissions Report 0.0.1

Emissions Report 0.0.3 → TCS Schema 0.0.1, 0.0.2, 0.1.0
Emissions Report 0.0.2 → TCS Schema 0.0.1, 0.0.2
Emissions Report 0.0.1 → TCS Schema 0.0.1
```

### 3.3 Version Management Strategy

```python
from enum import Enum

class ReportingOrgVersion(str, Enum):
    """Reporting Organisation schema versions."""
    V0_0_1 = "0.0.1"
    V0_1_0 = "0.1.0"
    V0_1_1 = "0.1.1"
    V0_1_2 = "0.1.2"  # Latest

class EmissionsReportVersion(str, Enum):
    """Emissions Report schema versions."""
    V0_0_1 = "0.0.1"
    V0_0_2 = "0.0.2"
    V0_0_3 = "0.0.3"  # Latest

class TCSVersion(str, Enum):
    """Tech Carbon Standard schema versions."""
    V0_0_1 = "0.0.1"
    V0_0_2 = "0.0.2"
    V0_1_0 = "0.1.0"  # Latest

# Default to latest versions
DEFAULT_REPORTING_ORG_VERSION = ReportingOrgVersion.V0_1_2
DEFAULT_EMISSIONS_REPORT_VERSION = EmissionsReportVersion.V0_0_3
DEFAULT_TCS_VERSION = TCSVersion.V0_1_0
```

---

## 4. Data Models Architecture

### 4.1 Core Models Hierarchy

```
TCSDocument (root)
├── schema_version: str
├── organisation: Organisation
└── emissions_reports: List[EmissionsReport]
    ├── schema_version: str
    ├── reporting_unit: Optional[str]
    ├── reporting_period: ReportingPeriod
    ├── verification: VerificationType
    ├── auditor_link: Optional[HttpUrl]
    ├── disclosures: Optional[List[Disclosure]]
    └── tech_carbon_standard: TechCarbonStandard
        ├── schema_version: str
        ├── upstream_emissions: Optional[UpstreamEmissions]
        ├── direct_emissions: Optional[DirectEmissions]
        ├── indirect_emissions: Optional[IndirectEmissions]
        └── downstream_emissions: Optional[DownstreamEmissions]
```

### 4.2 Base Emission Models

```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Scope2Method(str, Enum):
    """GHG Protocol Scope 2 accounting methods."""
    LOCATION_BASED = "location-based"
    MARKET_BASED = "market-based"
    MIXED_METHODS = "mixed-methods"
    OTHER = "other"

class Emissions(BaseModel):
    """Base emissions data structure (kgCO2e)."""
    emissions: float = Field(
        ...,
        ge=0,
        description="Total carbon emissions in kgCO2e"
    )
    notes: Optional[str] = Field(
        None,
        description="Notes explaining calculation methodology or data sources"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {"emissions": 55000, "notes": "Embodied carbon of purchased laptops"}
            ]
        }

class Scope2Emissions(Emissions):
    """Emissions with optional Scope 2 methodology specification."""
    method: Optional[Scope2Method] = Field(
        None,
        description="GHG Protocol Scope 2 accounting method"
    )
```

### 4.3 Emissions Category Models

```python
# === Upstream Emissions (Embodied Carbon) ===
class UpstreamEmissions(BaseModel):
    """Upstream emissions relating to embodied carbon."""
    software: Optional[Emissions] = None
    employee_hardware: Optional[Emissions] = None
    network_hardware: Optional[Emissions] = None
    server_hardware: Optional[Emissions] = None
    # Added in TCS v0.1.0
    foundation_models: Optional[Emissions] = None
    content_and_data: Optional[Emissions] = None

# === Direct Emissions (On-site Operations) ===
class DirectEmissions(BaseModel):
    """Direct running costs from electricity."""
    onsite_employee_hardware: Optional[Scope2Emissions] = None
    networking: Optional[Scope2Emissions] = None
    servers: Optional[Scope2Emissions] = None
    generators: Optional[Emissions] = None  # No Scope 2 method (Scope 1)

# === Indirect Emissions (External Services) ===
class IndirectEmissions(BaseModel):
    """Indirect running carbon costs."""
    offsite_employee_hardware: Optional[Emissions] = None
    cloud_services: Optional[Emissions] = None
    saas: Optional[Emissions] = None
    managed_services: Optional[Emissions] = None

# === Downstream Emissions (Customer Impact) ===
class DownstreamEmissions(BaseModel):
    """Carbon from products/services use."""
    # v0.1.0 renamed end_user_devices to customer_devices
    customer_devices: Optional[Emissions] = None
    network_data_transfer: Optional[Emissions] = None
    downstream_infrastructure: Optional[Emissions] = None
```

### 4.4 Organisation & Reporting Models

```python
from datetime import date
from pydantic import HttpUrl

class Organisation(BaseModel):
    """Reporting organisation details."""
    organisation_name: str = Field(..., min_length=1)
    description: Optional[str] = None
    open_corporates_url: Optional[HttpUrl] = None
    registered_country: Optional[str] = None

class ReportingPeriod(BaseModel):
    """Reporting period with date validation."""
    from_date: date
    to_date: date

    @model_validator(mode='after')
    def validate_date_range(self) -> 'ReportingPeriod':
        if self.to_date < self.from_date:
            raise ValueError('to_date must be after from_date')
        return self

class VerificationType(str, Enum):
    """Verification status options."""
    SELF_REPORTED = "self reported"
    INDEPENDENTLY_VERIFIED = "independently verified"

class DocType(str, Enum):
    """Disclosure document types."""
    REPORT = "report"
    METHODOLOGY = "methodology"
    OTHER = "other"

class Disclosure(BaseModel):
    """Disclosure document reference."""
    url: HttpUrl
    doc_type: DocType
    description: Optional[str] = None
```

### 4.5 Complete TCS Document Model

```python
class TechCarbonStandard(BaseModel):
    """Tech Carbon Standard emissions data."""
    schema_version: TCSVersion = DEFAULT_TCS_VERSION
    upstream_emissions: Optional[UpstreamEmissions] = None
    direct_emissions: Optional[DirectEmissions] = None
    indirect_emissions: Optional[IndirectEmissions] = None
    downstream_emissions: Optional[DownstreamEmissions] = None

class EmissionsReport(BaseModel):
    """Individual emissions report for a reporting period."""
    schema_version: EmissionsReportVersion = DEFAULT_EMISSIONS_REPORT_VERSION
    reporting_unit: Optional[str] = None
    reporting_period: ReportingPeriod
    verification: VerificationType
    auditor_link: Optional[HttpUrl] = None
    disclosures: Optional[list[Disclosure]] = None
    tech_carbon_standard: TechCarbonStandard

    @model_validator(mode='after')
    def validate_auditor_link(self) -> 'EmissionsReport':
        """Ensure auditor_link is provided when independently verified."""
        if (self.verification == VerificationType.INDEPENDENTLY_VERIFIED
            and self.auditor_link is None):
            raise ValueError(
                'auditor_link is required when verification is "independently verified"'
            )
        return self

class TCSDocument(BaseModel):
    """Root TCS document structure."""
    schema_version: ReportingOrgVersion = DEFAULT_REPORTING_ORG_VERSION
    organisation: Organisation
    emissions_reports: list[EmissionsReport] = Field(default_factory=list)
```

---

## 5. Builder Pattern API

### 5.1 Fluent Builder Interface

The library shall provide a fluent builder API for constructing TCS documents:

```python
from pytcsschemahelper import TCSBuilder

# Simple document creation
doc = (
    TCSBuilder()
    .organisation(
        name="Example Corp",
        description="Software consultancy",
        country="England"
    )
    .add_report(
        from_date="2024-01-01",
        to_date="2024-12-31",
        verification="self reported"
    )
    .upstream(
        employee_hardware=55000,
        employee_hardware_notes="Embodied carbon of laptops"
    )
    .direct(
        onsite_employee_hardware=5000,
        onsite_employee_hardware_method="location-based"
    )
    .indirect(
        cloud_services=12000,
        cloud_services_notes="AWS carbon footprint"
    )
    .downstream(
        customer_devices=5000
    )
    .build()
)
```

### 5.2 Builder Implementation

```python
class TCSBuilder:
    """Fluent builder for TCS documents."""

    def __init__(
        self,
        reporting_org_version: ReportingOrgVersion = DEFAULT_REPORTING_ORG_VERSION
    ):
        self._version = reporting_org_version
        self._organisation: Optional[Organisation] = None
        self._reports: list[EmissionsReport] = []
        self._current_report: Optional[dict] = None
        self._current_tcs: Optional[dict] = None

    def organisation(
        self,
        name: str,
        description: Optional[str] = None,
        open_corporates_url: Optional[str] = None,
        country: Optional[str] = None
    ) -> 'TCSBuilder':
        """Set organisation details."""
        self._organisation = Organisation(
            organisation_name=name,
            description=description,
            open_corporates_url=open_corporates_url,
            registered_country=country
        )
        return self

    def add_report(
        self,
        from_date: str | date,
        to_date: str | date,
        verification: str | VerificationType,
        reporting_unit: Optional[str] = None,
        auditor_link: Optional[str] = None,
        emissions_report_version: EmissionsReportVersion = DEFAULT_EMISSIONS_REPORT_VERSION,
        tcs_version: TCSVersion = DEFAULT_TCS_VERSION
    ) -> 'TCSBuilder':
        """Start a new emissions report."""
        # Finalize previous report if exists
        self._finalize_current_report()

        self._current_report = {
            "schema_version": emissions_report_version,
            "reporting_unit": reporting_unit,
            "reporting_period": ReportingPeriod(
                from_date=_parse_date(from_date),
                to_date=_parse_date(to_date)
            ),
            "verification": VerificationType(verification),
            "auditor_link": auditor_link,
            "disclosures": []
        }
        self._current_tcs = {"schema_version": tcs_version}
        return self

    def upstream(
        self,
        software: Optional[float] = None,
        software_notes: Optional[str] = None,
        employee_hardware: Optional[float] = None,
        employee_hardware_notes: Optional[str] = None,
        # ... other fields
    ) -> 'TCSBuilder':
        """Set upstream emissions for current report."""
        emissions = {}
        if software is not None:
            emissions["software"] = Emissions(emissions=software, notes=software_notes)
        if employee_hardware is not None:
            emissions["employee_hardware"] = Emissions(
                emissions=employee_hardware,
                notes=employee_hardware_notes
            )
        # ... other fields

        self._current_tcs["upstream_emissions"] = UpstreamEmissions(**emissions)
        return self

    # Similar methods for direct(), indirect(), downstream()

    def add_disclosure(
        self,
        url: str,
        doc_type: str | DocType,
        description: Optional[str] = None
    ) -> 'TCSBuilder':
        """Add disclosure to current report."""
        self._current_report["disclosures"].append(
            Disclosure(url=url, doc_type=DocType(doc_type), description=description)
        )
        return self

    def build(self) -> TCSDocument:
        """Build and validate the complete TCS document."""
        self._finalize_current_report()

        if self._organisation is None:
            raise ValueError("Organisation details are required")

        return TCSDocument(
            schema_version=self._version,
            organisation=self._organisation,
            emissions_reports=self._reports
        )

    def _finalize_current_report(self) -> None:
        """Finalize the current report and add to list."""
        if self._current_report is not None:
            self._current_report["tech_carbon_standard"] = TechCarbonStandard(
                **self._current_tcs
            )
            self._reports.append(EmissionsReport(**self._current_report))
            self._current_report = None
            self._current_tcs = None
```

---

## 6. Serialization & Deserialization

### 6.1 JSON Serialization

```python
class TCSDocument(BaseModel):
    # ... fields ...

    def to_json(
        self,
        indent: Optional[int] = 2,
        exclude_none: bool = True
    ) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(
            indent=indent,
            exclude_none=exclude_none,
            by_alias=True
        )

    def to_dict(self, exclude_none: bool = True) -> dict:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=exclude_none, by_alias=True)

    def save(
        self,
        path: str | Path,
        indent: Optional[int] = 2
    ) -> None:
        """Save to file."""
        path = Path(path)
        path.write_text(self.to_json(indent=indent))

    @classmethod
    def from_json(cls, json_str: str) -> 'TCSDocument':
        """Parse from JSON string."""
        return cls.model_validate_json(json_str)

    @classmethod
    def load(cls, path: str | Path) -> 'TCSDocument':
        """Load from file."""
        path = Path(path)
        return cls.from_json(path.read_text())

    @classmethod
    def from_url(cls, url: str) -> 'TCSDocument':
        """Fetch and parse from URL."""
        import urllib.request
        with urllib.request.urlopen(url) as response:
            return cls.from_json(response.read().decode())
```

### 6.2 Date Serialization

Dates must serialize to ISO 8601 format (`YYYY-MM-DD`):

```python
class ReportingPeriod(BaseModel):
    from_date: date
    to_date: date

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }
```

---

## 7. Validation

### 7.1 Pydantic Validation (Built-in)

All models use Pydantic's built-in validation:

```python
# Automatic validation on creation
try:
    emissions = Emissions(emissions=-100)  # Raises ValidationError
except ValidationError as e:
    print(e.errors())
```

### 7.2 JSON Schema Validation

```python
from pytcsschemahelper.validation import validate_against_schema

def validate_against_schema(
    document: TCSDocument | dict | str,
    schema_url: Optional[str] = None
) -> ValidationResult:
    """
    Validate document against official TCS JSON Schema.

    Args:
        document: TCS document (model, dict, or JSON string)
        schema_url: Override schema URL (defaults to official router schema)

    Returns:
        ValidationResult with is_valid, errors, and warnings
    """
    ...

class ValidationResult:
    is_valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationWarning]

    def raise_for_errors(self) -> None:
        """Raise exception if validation failed."""
        if not self.is_valid:
            raise TCSValidationError(self.errors)
```

### 7.3 Validation Rules

The library must enforce these validation rules:

1. **Schema Version Compatibility**: Ensure nested schema versions are compatible
2. **Conditional Fields**: `auditor_link` required when `verification == "independently verified"`
3. **Date Validation**: `to_date >= from_date`
4. **Emissions Values**: Must be non-negative numbers
5. **URL Formats**: Must be valid URIs
6. **Required Fields**: Enforce all required fields per schema version

### 7.4 Custom Validators

```python
from pytcsschemahelper.validators import (
    validate_version_compatibility,
    validate_emissions_completeness,
    validate_date_coverage,
)

# Check if all categories have data
completeness = validate_emissions_completeness(doc)
print(f"Coverage: {completeness.coverage_percentage}%")
print(f"Missing categories: {completeness.missing_categories}")

# Check for date gaps between reports
gaps = validate_date_coverage(doc)
if gaps:
    print(f"Gap detected: {gaps[0].from_date} to {gaps[0].to_date}")
```

---

## 8. Version Migration

### 8.1 Migration Utilities

```python
from pytcsschemahelper.migration import migrate_document, MigrationPath

# Migrate a document to latest versions
migrated = migrate_document(
    document=old_doc,
    target_reporting_org_version=ReportingOrgVersion.V0_1_2,
    target_emissions_report_version=EmissionsReportVersion.V0_0_3,
    target_tcs_version=TCSVersion.V0_1_0
)

# Get migration path
path = MigrationPath.get_path(
    from_version=TCSVersion.V0_0_2,
    to_version=TCSVersion.V0_1_0
)
print(path.changes)  # List of breaking changes
```

### 8.2 Version-Specific Changes

Document known breaking changes between versions:

```python
VERSION_CHANGES = {
    TCSVersion.V0_1_0: {
        "added_fields": ["foundation_models", "content_and_data"],
        "renamed_fields": {"end_user_devices": "customer_devices"},
        "removed_fields": [],
        "breaking": False
    }
}
```

---

## 9. Command-Line Interface

### 9.1 CLI Commands

```bash
# Validate a TCS document
tcs validate tcs.json

# Validate against specific schema version
tcs validate tcs.json --schema-version 0.1.2

# Create a new TCS document interactively
tcs init --output tcs.json

# Convert between versions
tcs migrate tcs.json --to-version 0.1.2 --output tcs-new.json

# Fetch and validate from URL
tcs fetch https://example.com/tcs.json --validate

# Generate schema documentation
tcs docs --format markdown --output schema-docs.md

# Calculate totals
tcs totals tcs.json
```

### 9.2 CLI Implementation

```python
import click
from rich.console import Console
from rich.table import Table

@click.group()
@click.version_option()
def cli():
    """TCS Schema - Technology Carbon Standard Schema Generator"""
    pass

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--schema-version', '-v', help='Validate against specific version')
@click.option('--strict', is_flag=True, help='Fail on warnings')
def validate(file: str, schema_version: Optional[str], strict: bool):
    """Validate a TCS document."""
    console = Console()

    try:
        doc = TCSDocument.load(file)
        result = validate_against_schema(doc, schema_version)

        if result.is_valid:
            console.print("✓ Document is valid", style="green")
        else:
            console.print("✗ Validation failed", style="red")
            for error in result.errors:
                console.print(f"  - {error.path}: {error.message}")
            raise SystemExit(1)

    except Exception as e:
        console.print(f"Error: {e}", style="red")
        raise SystemExit(1)

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def totals(file: str):
    """Calculate emission totals from a TCS document."""
    doc = TCSDocument.load(file)

    table = Table(title="Emissions Summary (kgCO2e)")
    table.add_column("Category")
    table.add_column("Total", justify="right")

    for report in doc.emissions_reports:
        # Calculate totals per category
        ...
```

---

## 10. Utility Functions

### 10.1 Calculation Helpers

```python
from pytcsschemahelper.utils import (
    calculate_total_emissions,
    calculate_category_totals,
    aggregate_reports,
)

# Calculate total emissions across all categories
total = calculate_total_emissions(doc)  # Returns float in kgCO2e

# Get breakdown by category
breakdown = calculate_category_totals(doc)
# Returns: {
#     "upstream": 56000,
#     "direct": 7000,
#     "indirect": 97000,
#     "downstream": 4000,
#     "total": 164000
# }

# Aggregate multiple reports (e.g., for multi-year comparison)
aggregated = aggregate_reports(doc.emissions_reports)
```

### 10.2 Convenience Constructors

```python
from pytcsschemahelper import quick_report

# Create a minimal valid document quickly
doc = quick_report(
    org_name="My Company",
    year=2024,
    upstream_total=50000,
    direct_total=10000,
    indirect_total=80000,
    downstream_total=5000
)
```

---

## 11. Error Handling

### 11.1 Exception Hierarchy

```python
class TCSError(Exception):
    """Base exception for TCS Schema library."""
    pass

class TCSValidationError(TCSError):
    """Raised when document validation fails."""
    def __init__(self, errors: list[ValidationError]):
        self.errors = errors
        super().__init__(f"Validation failed with {len(errors)} error(s)")

class TCSVersionError(TCSError):
    """Raised for version-related errors."""
    pass

class TCSCompatibilityError(TCSVersionError):
    """Raised when schema versions are incompatible."""
    pass

class TCSMigrationError(TCSError):
    """Raised when migration fails."""
    pass

class TCSParseError(TCSError):
    """Raised when parsing fails."""
    pass
```

---

## 12. Project Structure

```
pytcsschemahelper/
├── src/
│   └── pytcsschemahelper/
│       ├── __init__.py           # Public API exports
│       ├── py.typed              # PEP 561 marker
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py           # Base emission models
│       │   ├── emissions.py      # Emission category models
│       │   ├── organisation.py   # Organisation models
│       │   ├── report.py         # Report models
│       │   └── document.py       # TCSDocument model
│       ├── builder.py            # TCSBuilder class
│       ├── validation/
│       │   ├── __init__.py
│       │   ├── schema.py         # JSON Schema validation
│       │   └── validators.py     # Custom validators
│       ├── migration/
│       │   ├── __init__.py
│       │   └── migrators.py      # Version migration logic
│       ├── cli/
│       │   ├── __init__.py
│       │   └── commands.py       # CLI implementation
│       ├── utils.py              # Utility functions
│       ├── exceptions.py         # Exception classes
│       └── versions.py           # Version enums and constants
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_builder.py
│   ├── test_validation.py
│   ├── test_migration.py
│   ├── test_cli.py
│   └── fixtures/
│       ├── valid_minimal.json
│       ├── valid_complete.json
│       └── invalid_*.json
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   ├── api-reference.md
│   ├── schema-versions.md
│   └── migration-guide.md
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE                   # CC0 1.0 Universal
└── .github/
    └── workflows/
        ├── ci.yml
        └── release.yml
```

---

## 13. Testing Strategy

### 13.1 Test Categories

1. **Unit Tests**: Test individual models, validators, and utilities
2. **Integration Tests**: Test builder patterns and serialization roundtrips
3. **Schema Tests**: Validate against official TCS JSON schemas
4. **CLI Tests**: Test command-line interface
5. **Migration Tests**: Test version migration paths

### 13.2 Test Coverage Requirements

- **Minimum**: 90% code coverage
- **Critical paths**: 100% coverage for validation and serialization

### 13.3 Example Tests

```python
import pytest
from pytcsschemahelper import TCSDocument, TCSBuilder, Emissions

class TestEmissions:
    def test_valid_emissions(self):
        e = Emissions(emissions=1000, notes="Test")
        assert e.emissions == 1000
        assert e.notes == "Test"

    def test_negative_emissions_rejected(self):
        with pytest.raises(ValidationError):
            Emissions(emissions=-100)

    def test_notes_optional(self):
        e = Emissions(emissions=500)
        assert e.notes is None

class TestTCSBuilder:
    def test_minimal_document(self):
        doc = (
            TCSBuilder()
            .organisation(name="Test Corp")
            .add_report(
                from_date="2024-01-01",
                to_date="2024-12-31",
                verification="self reported"
            )
            .build()
        )
        assert doc.organisation.organisation_name == "Test Corp"
        assert len(doc.emissions_reports) == 1

    def test_auditor_link_required_for_verified(self):
        with pytest.raises(ValidationError):
            TCSBuilder()
            .organisation(name="Test")
            .add_report(
                from_date="2024-01-01",
                to_date="2024-12-31",
                verification="independently verified"
                # Missing auditor_link
            )
            .build()

class TestSerialization:
    def test_roundtrip(self, sample_document):
        json_str = sample_document.to_json()
        loaded = TCSDocument.from_json(json_str)
        assert loaded == sample_document

    def test_date_format(self, sample_document):
        json_str = sample_document.to_json()
        assert '"from_date": "2024-01-01"' in json_str
```

---

## 14. Documentation Requirements

### 14.1 Required Documentation

1. **README.md**: Quick start, installation, basic usage
2. **Getting Started Guide**: Step-by-step tutorial
3. **API Reference**: Auto-generated from docstrings
4. **Schema Version Guide**: Document all supported versions and differences
5. **Migration Guide**: How to upgrade documents between versions
6. **Examples**: Real-world usage examples

### 14.2 Docstring Standard

Use Google-style docstrings:

```python
def calculate_total_emissions(document: TCSDocument) -> float:
    """
    Calculate total emissions across all categories and reports.

    Args:
        document: A valid TCS document

    Returns:
        Total emissions in kgCO2e

    Raises:
        TCSValidationError: If document is invalid

    Example:
        >>> doc = TCSDocument.load("tcs.json")
        >>> total = calculate_total_emissions(doc)
        >>> print(f"Total: {total:,.0f} kgCO2e")
        Total: 164,000 kgCO2e
    """
```

---

## 15. Release Process

### 15.1 Versioning

Follow Semantic Versioning (SemVer):
- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### 15.2 Release Checklist

1. Update `CHANGELOG.md`
2. Update version in `pyproject.toml`
3. Run full test suite
4. Build and verify package
5. Create GitHub release with tag
6. Publish to PyPI via GitHub Actions

### 15.3 CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest --cov=pytcsschemahelper --cov-report=xml
      - run: mypy src/pytcsschemahelper
      - run: ruff check src/pytcsschemahelper
```

---

## 16. Future Considerations

### 16.1 Potential Enhancements

1. **Async Support**: Async file I/O and URL fetching
2. **Schema Caching**: Cache remote schemas locally
3. **Diff Tool**: Compare two TCS documents
4. **Report Generation**: Generate human-readable reports (PDF, HTML)
5. **Integration Plugins**: Django, FastAPI, Flask integrations
6. **Carbon Calculators**: Built-in emission estimation helpers

### 16.2 Schema Updates

The library should be designed to easily accommodate future TCS schema versions:

1. Add new version enums
2. Create version-specific model variants if needed
3. Update migration paths
4. Update validation logic
5. Update documentation

---

## Appendix A: Complete Usage Example

```python
from datetime import date
from pytcsschemahelper import (
    TCSBuilder,
    TCSDocument,
    VerificationType,
    Scope2Method,
)
from pytcsschemahelper.validation import validate_against_schema
from pytcsschemahelper.utils import calculate_category_totals

# Build a complete TCS document
doc = (
    TCSBuilder()
    .organisation(
        name="Acme Technology Ltd",
        description="Cloud-native software development company",
        open_corporates_url="https://opencorporates.com/companies/gb/12345678",
        country="England"
    )

    # 2024 Report
    .add_report(
        from_date=date(2024, 1, 1),
        to_date=date(2024, 12, 31),
        verification=VerificationType.SELF_REPORTED,
        reporting_unit="Global Operations"
    )
    .add_disclosure(
        url="https://acme.com/sustainability-2024.pdf",
        doc_type="report",
        description="Annual Sustainability Report 2024"
    )
    .upstream(
        software=2000,
        software_notes="Development tools and libraries",
        employee_hardware=55000,
        employee_hardware_notes="MacBooks and monitors - manufacturer LCA data",
        network_hardware=3000,
        server_hardware=0,
        server_hardware_notes="Fully cloud-based, no on-premise servers"
    )
    .direct(
        onsite_employee_hardware=5000,
        onsite_employee_hardware_method=Scope2Method.LOCATION_BASED,
        onsite_employee_hardware_notes="Office electricity consumption",
        networking=2000,
        servers=0
    )
    .indirect(
        offsite_employee_hardware=3000,
        offsite_employee_hardware_notes="Remote work estimates",
        cloud_services=45000,
        cloud_services_notes="AWS Carbon Footprint Tool data",
        saas=25000,
        saas_notes="Spend-based calculation via Climatiq",
        managed_services=5000
    )
    .downstream(
        customer_devices=8000,
        customer_devices_notes="Based on API usage patterns",
        network_data_transfer=3000,
        downstream_infrastructure=2000
    )

    # 2023 Report (historical)
    .add_report(
        from_date=date(2023, 1, 1),
        to_date=date(2023, 12, 31),
        verification=VerificationType.SELF_REPORTED
    )
    .upstream(employee_hardware=48000)
    .direct(onsite_employee_hardware=6000)
    .indirect(cloud_services=38000, saas=22000)
    .downstream(customer_devices=6000)

    .build()
)

# Validate against official schema
result = validate_against_schema(doc)
if result.is_valid:
    print("✓ Document is valid")
else:
    for error in result.errors:
        print(f"✗ {error}")

# Calculate totals
totals = calculate_category_totals(doc.emissions_reports[0])
print(f"\n2024 Emissions Breakdown:")
print(f"  Upstream:   {totals['upstream']:>10,} kgCO2e")
print(f"  Direct:     {totals['direct']:>10,} kgCO2e")
print(f"  Indirect:   {totals['indirect']:>10,} kgCO2e")
print(f"  Downstream: {totals['downstream']:>10,} kgCO2e")
print(f"  ─────────────────────────")
print(f"  Total:      {totals['total']:>10,} kgCO2e")

# Save to file
doc.save("tcs.json")
print("\n✓ Saved to tcs.json")

# Load and verify roundtrip
loaded = TCSDocument.load("tcs.json")
assert loaded == doc
print("✓ Roundtrip verification passed")
```

---

## Appendix B: JSON Output Example

```json
{
  "schema_version": "0.1.2",
  "organisation": {
    "organisation_name": "Acme Technology Ltd",
    "description": "Cloud-native software development company",
    "open_corporates_url": "https://opencorporates.com/companies/gb/12345678",
    "registered_country": "England"
  },
  "emissions_reports": [
    {
      "schema_version": "0.0.3",
      "reporting_unit": "Global Operations",
      "reporting_period": {
        "from_date": "2024-01-01",
        "to_date": "2024-12-31"
      },
      "verification": "self reported",
      "disclosures": [
        {
          "url": "https://acme.com/sustainability-2024.pdf",
          "doc_type": "report",
          "description": "Annual Sustainability Report 2024"
        }
      ],
      "tech_carbon_standard": {
        "schema_version": "0.1.0",
        "upstream_emissions": {
          "software": {
            "emissions": 2000,
            "notes": "Development tools and libraries"
          },
          "employee_hardware": {
            "emissions": 55000,
            "notes": "MacBooks and monitors - manufacturer LCA data"
          },
          "network_hardware": {
            "emissions": 3000
          },
          "server_hardware": {
            "emissions": 0,
            "notes": "Fully cloud-based, no on-premise servers"
          }
        },
        "direct_emissions": {
          "onsite_employee_hardware": {
            "emissions": 5000,
            "notes": "Office electricity consumption",
            "method": "location-based"
          },
          "networking": {
            "emissions": 2000
          },
          "servers": {
            "emissions": 0
          }
        },
        "indirect_emissions": {
          "offsite_employee_hardware": {
            "emissions": 3000,
            "notes": "Remote work estimates"
          },
          "cloud_services": {
            "emissions": 45000,
            "notes": "AWS Carbon Footprint Tool data"
          },
          "saas": {
            "emissions": 25000,
            "notes": "Spend-based calculation via Climatiq"
          },
          "managed_services": {
            "emissions": 5000
          }
        },
        "downstream_emissions": {
          "customer_devices": {
            "emissions": 8000,
            "notes": "Based on API usage patterns"
          },
          "network_data_transfer": {
            "emissions": 3000
          },
          "downstream_infrastructure": {
            "emissions": 2000
          }
        }
      }
    }
  ]
}
```

---

*Document Version: 1.0.0*
*Last Updated: December 2024*
*TCS Schema Versions Covered: Router 0.0.1-0.1.2, Emissions Report 0.0.1-0.0.3, TCS 0.0.1-0.1.0*
