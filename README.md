# pytcsschemahelper

[![PyPI version](https://img.shields.io/pypi/v/pytcsschemahelper.svg)](https://pypi.org/project/pytcsschemahelper/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytcsschemahelper.svg)](https://pypi.org/project/pytcsschemahelper/)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![CI](https://github.com/your-org/pytcsschemahelper/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/pytcsschemahelper/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/codecov/c/github/your-org/pytcsschemahelper)](https://codecov.io/gh/your-org/pytcsschemahelper)

A Python library for generating, validating, and managing [Technology Carbon Standard (TCS)](https://www.techcarbonstandard.org/) schema documents.

## What is TCS?

The Technology Carbon Standard is a framework for organisations to measure and report technology-related carbon emissions. Organisations publish TCS-compliant JSON documents at their root domain (e.g., `https://example.com/tcs.json`) to transparently report their technology carbon footprint.

**pytcsschemahelper** makes it easy to create these documents programmatically with full type safety and validation.

## Installation

```bash
pip install pytcsschemahelper
```

For CLI support:

```bash
pip install pytcsschemahelper[cli]
```

## Quick Start

### Using the Builder API

The fluent builder interface provides the easiest way to create TCS documents:

```python
from pytcsschemahelper import TCSBuilder

doc = (
    TCSBuilder()
    .organisation(
        name="Acme Technology Ltd",
        description="Cloud-native software company",
        country="England"
    )
    .add_report(
        from_date="2024-01-01",
        to_date="2024-12-31",
        verification="self reported"
    )
    .upstream(
        employee_hardware=55000,
        employee_hardware_notes="Embodied carbon from laptops and monitors"
    )
    .direct(
        onsite_employee_hardware=5000,
        onsite_employee_hardware_method="location-based"
    )
    .indirect(
        cloud_services=45000,
        cloud_services_notes="AWS Carbon Footprint Tool data",
        saas=25000
    )
    .downstream(
        customer_devices=8000,
        network_data_transfer=3000
    )
    .build()
)

# Save to file
doc.save("tcs.json")
```

### Using Models Directly

For more control, use the Pydantic models directly:

```python
from datetime import date
from pytcsschemahelper import (
    TCSDocument,
    Organisation,
    EmissionsReport,
    ReportingPeriod,
    TechCarbonStandard,
    UpstreamEmissions,
    Emissions,
    VerificationType,
)

doc = TCSDocument(
    organisation=Organisation(
        organisation_name="Acme Technology Ltd",
        description="Cloud-native software company",
        registered_country="England"
    ),
    emissions_reports=[
        EmissionsReport(
            reporting_period=ReportingPeriod(
                from_date=date(2024, 1, 1),
                to_date=date(2024, 12, 31)
            ),
            verification=VerificationType.SELF_REPORTED,
            tech_carbon_standard=TechCarbonStandard(
                upstream_emissions=UpstreamEmissions(
                    employee_hardware=Emissions(
                        emissions=55000,
                        notes="Embodied carbon from laptops"
                    )
                )
            )
        )
    ]
)

print(doc.to_json())
```

### Quick Report Helper

For simple documents, use the convenience function:

```python
from pytcsschemahelper import quick_report

doc = quick_report(
    org_name="My Company",
    year=2024,
    upstream_total=50000,
    direct_total=10000,
    indirect_total=80000,
    downstream_total=5000
)
```

## Features

### Document Creation
- **Fluent Builder API** — chainable methods for intuitive document construction
- **Type-safe Models** — Pydantic models with full validation
- **Multiple Schema Versions** — support for all TCS schema versions

### Validation
- **Pydantic Validation** — automatic validation on model creation
- **JSON Schema Validation** — validate against official TCS schemas
- **Custom Validators** — check version compatibility, emissions completeness, and date coverage

### Serialization
- **JSON Export** — serialize to JSON with configurable formatting
- **File I/O** — save to and load from files
- **URL Fetching** — load documents from remote URLs

### Migration
- **Version Migration** — upgrade documents between schema versions
- **Change Documentation** — track breaking changes between versions

### CLI (Optional)
- **Validate** — check documents against TCS schemas
- **Calculate Totals** — summarize emissions by category
- **Migrate** — upgrade documents to newer schema versions

## Validation

Validate documents against the official TCS JSON schemas:

```python
from pytcsschemahelper.validation import validate_against_schema

result = validate_against_schema(doc)

if result.is_valid:
    print("✓ Document is valid")
else:
    for error in result.errors:
        print(f"✗ {error.path}: {error.message}")
```

Check emissions coverage:

```python
from pytcsschemahelper.validators import validate_emissions_completeness

completeness = validate_emissions_completeness(doc)
print(f"Coverage: {completeness.coverage_percentage}%")
print(f"Missing: {completeness.missing_categories}")
```

## Calculating Totals

```python
from pytcsschemahelper.utils import calculate_category_totals

totals = calculate_category_totals(doc.emissions_reports[0])

print(f"Upstream:   {totals['upstream']:>10,} kgCO2e")
print(f"Direct:     {totals['direct']:>10,} kgCO2e")
print(f"Indirect:   {totals['indirect']:>10,} kgCO2e")
print(f"Downstream: {totals['downstream']:>10,} kgCO2e")
print(f"Total:      {totals['total']:>10,} kgCO2e")
```

## CLI Usage

```bash
# Validate a document
tcs validate tcs.json

# Calculate emission totals
tcs totals tcs.json

# Migrate to a newer schema version
tcs migrate tcs.json --to-version 0.1.2 --output tcs-new.json

# Fetch and validate from URL
tcs fetch https://example.com/tcs.json --validate
```

## Supported Schema Versions

| Component | Versions | Latest |
|-----------|----------|--------|
| Reporting Organisation | 0.0.1, 0.1.0, 0.1.1, 0.1.2 | 0.1.2 |
| Emissions Report | 0.0.1, 0.0.2, 0.0.3 | 0.0.3 |
| Tech Carbon Standard | 0.0.1, 0.0.2, 0.1.0 | 0.1.0 |

The library defaults to the latest versions but supports creating documents with any combination of compatible versions.

## Emissions Categories

The TCS organises emissions into four categories:

| Category | Description | Examples |
|----------|-------------|----------|
| **Upstream** | Embodied carbon | Hardware manufacturing, software development |
| **Direct** | On-site operations | Office electricity, on-premise servers |
| **Indirect** | External services | Cloud providers, SaaS applications |
| **Downstream** | Customer impact | End-user devices, data transfer |

## Documentation

- [Getting Started Guide](https://your-org.github.io/pytcsschemahelper/getting-started/)
- [API Reference](https://your-org.github.io/pytcsschemahelper/api-reference/)
- [Schema Versions](https://your-org.github.io/pytcsschemahelper/schema-versions/)
- [Migration Guide](https://your-org.github.io/pytcsschemahelper/migration-guide/)

## Requirements

- Python 3.9+
- pydantic >= 2.0
- jsonschema >= 4.0
- python-dateutil >= 2.8

## License

This project is dedicated to the public domain under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). No rights reserved — you can use, modify, and distribute this code for any purpose without restriction or attribution.

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Related Links

- [Technology Carbon Standard](https://www.techcarbonstandard.org/)
- [TCS Implementation Guide](https://www.techcarbonstandard.org/schemas/implementation-guide)
- [TCS JSON Schemas](https://www.techcarbonstandard.org/schemas/)

## Acknowledgements

This library implements the [Technology Carbon Standard](https://www.techcarbonstandard.org/) specification developed by the TCS community to help organisations measure and report their technology carbon footprint.
