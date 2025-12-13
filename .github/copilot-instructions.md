# GitHub Copilot Instructions for pytcsschemahelper

## Project Overview

**pytcsschemahelper** is a Python library for generating, validating, and managing Technology Carbon Standard (TCS) schema documents. The library enables organizations to programmatically create TCS-compliant JSON documents that report technology-related carbon emissions.

### Key Goals
- Provide a type-safe, Pythonic interface for TCS document creation
- Support all TCS schema versions with version-aware routing
- Offer fluent builder API for intuitive document construction
- Enable validation against official TCS JSON schemas
- Support migration between schema versions

## Tech Stack

### Core Dependencies
- **Python**: 3.9+ (test on 3.9, 3.10, 3.11, 3.12, 3.13)
- **pydantic**: >=2.0,<3.0 - Data validation and serialization
- **jsonschema**: >=4.0,<5.0 - JSON Schema validation
- **typing-extensions**: >=4.0 - Extended typing support
- **python-dateutil**: >=2.8 - Date parsing utilities

### Optional Dependencies
- **CLI**: click>=8.0, rich>=13.0
- **Development**: pytest>=7.0, pytest-cov>=4.0, mypy>=1.0, ruff>=0.1.0
- **Documentation**: mkdocs>=1.5, mkdocs-material>=9.0

### Build System
- Use **pyproject.toml** for project configuration
- Package structure: `src/pytcsschemahelper/`
- Include `py.typed` marker for PEP 561 type hint support

## Project Structure

```
pytcsschemahelper/
├── src/pytcsschemahelper/
│   ├── __init__.py           # Public API exports
│   ├── py.typed              # PEP 561 marker
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py           # Base emission models
│   │   ├── emissions.py      # Emission category models
│   │   ├── organisation.py   # Organisation models
│   │   ├── report.py         # Report models
│   │   └── document.py       # TCSDocument model
│   ├── builder.py            # TCSBuilder class
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── schema.py         # JSON Schema validation
│   │   └── validators.py     # Custom validators
│   ├── migration/
│   │   ├── __init__.py
│   │   └── migrators.py      # Version migration logic
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py       # CLI implementation
│   ├── utils.py              # Utility functions
│   ├── exceptions.py         # Exception classes
│   └── versions.py           # Version enums and constants
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_builder.py
│   ├── test_validation.py
│   ├── test_migration.py
│   ├── test_cli.py
│   └── fixtures/
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   ├── api-reference.md
│   ├── schema-versions.md
│   └── migration-guide.md
└── pyproject.toml
```

## Coding Standards

### Style Guidelines
- **Type Hints**: Use type hints for all function signatures and class attributes
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Line Length**: Maximum 100 characters (configurable in ruff.toml)
- **Imports**: Group imports (standard library, third-party, local) and sort alphabetically
- **Naming**:
  - Classes: PascalCase (e.g., `TCSDocument`, `EmissionsReport`)
  - Functions/Methods: snake_case (e.g., `calculate_total_emissions`)
  - Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_TCS_VERSION`)
  - Private members: prefix with underscore (e.g., `_finalize_current_report`)

### Code Formatting
- Use **ruff** for linting and formatting
- Use **mypy** for static type checking
- Enable Pydantic strict mode where appropriate
- Prefer Pydantic v2 patterns and validators

### Comments
- Write comments only when code intent is not obvious
- Focus on "why" not "what"
- Use docstrings for public APIs
- Add examples in docstrings where helpful

## Development Workflow

### Running Tests
```bash
# Run all tests with coverage
pytest --cov=pytcsschemahelper --cov-report=term-missing

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Linting and Type Checking
```bash
# Run ruff linter
ruff check src/pytcsschemahelper

# Run ruff formatter
ruff format src/pytcsschemahelper

# Run type checker
mypy src/pytcsschemahelper
```

### Building the Package
```bash
# Install in development mode
pip install -e .

# Install with optional dependencies
pip install -e ".[cli,dev,docs]"

# Build distribution
python -m build
```

## Schema Version Management

### Supported Versions
- **Reporting Organisation**: 0.0.1, 0.1.0, 0.1.1, 0.1.2 (latest: 0.1.2)
- **Emissions Report**: 0.0.1, 0.0.2, 0.0.3 (latest: 0.0.3)
- **Tech Carbon Standard**: 0.0.1, 0.0.2, 0.1.0 (latest: 0.1.0)

### Version Compatibility
- Always ensure nested schema versions are compatible
- Default to latest versions when not specified
- Support backward compatibility for older versions
- Document breaking changes between versions

## Key Design Patterns

### 1. Pydantic Models
All data structures use Pydantic v2 BaseModel:
```python
from pydantic import BaseModel, Field, model_validator

class Emissions(BaseModel):
    emissions: float = Field(..., ge=0, description="Total carbon emissions in kgCO2e")
    notes: Optional[str] = Field(None, description="Calculation methodology notes")
```

### 2. Fluent Builder Pattern
Use method chaining for document construction:
```python
doc = (
    TCSBuilder()
    .organisation(name="Corp", country="England")
    .add_report(from_date="2024-01-01", to_date="2024-12-31", verification="self reported")
    .upstream(employee_hardware=55000)
    .build()
)
```

### 3. Validation Strategy
- **Pydantic validators**: Built-in field validation
- **Model validators**: Cross-field validation (e.g., date ranges)
- **JSON Schema validation**: Validate against official TCS schemas
- **Custom validators**: Domain-specific checks (completeness, compatibility)

### 4. Serialization
- Use Pydantic's `model_dump()` and `model_dump_json()`
- Support `exclude_none=True` to omit optional fields
- Ensure dates serialize to ISO 8601 format (YYYY-MM-DD)
- Support roundtrip serialization/deserialization

## Testing Strategy

### Test Categories
1. **Unit Tests**: Individual models, validators, utilities
2. **Integration Tests**: Builder patterns, serialization roundtrips
3. **Schema Tests**: Validate against official TCS JSON schemas
4. **CLI Tests**: Command-line interface using Click's test runner
5. **Migration Tests**: Version migration paths

### Test Coverage
- Minimum: 90% code coverage
- Critical paths (validation, serialization): 100% coverage
- Use pytest fixtures for common test data
- Create fixture files in `tests/fixtures/`

### Test Examples
```python
def test_emissions_validation():
    # Valid emissions
    e = Emissions(emissions=1000, notes="Test")
    assert e.emissions == 1000
    
    # Negative emissions should fail
    with pytest.raises(ValidationError):
        Emissions(emissions=-100)
```

## Documentation Standards

### Docstring Format
Use Google-style docstrings with examples:
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

### Documentation Files
- **README.md**: Quick start, installation, basic usage
- **docs/getting-started.md**: Step-by-step tutorial
- **docs/api-reference.md**: Auto-generated from docstrings
- **docs/schema-versions.md**: Document all supported versions
- **docs/migration-guide.md**: Version upgrade instructions

## Exception Handling

### Exception Hierarchy
```python
TCSError (base)
├── TCSValidationError       # Document validation failures
├── TCSVersionError          # Version-related errors
│   └── TCSCompatibilityError  # Incompatible schema versions
├── TCSMigrationError        # Migration failures
└── TCSParseError            # Parsing failures
```

### Usage
- Always inherit from `TCSError` for library-specific exceptions
- Provide clear error messages with context
- Include validation errors in `TCSValidationError`

## Important Validation Rules

1. **Emissions Values**: Must be non-negative floats (>= 0)
2. **Date Ranges**: `to_date` must be >= `from_date`
3. **Auditor Link**: Required when `verification == "independently verified"`
4. **Schema Compatibility**: Nested schema versions must be compatible
5. **URL Formats**: Must be valid URIs using Pydantic's HttpUrl

## Emissions Categories

### Structure
```
TCS Document
├── Upstream Emissions (Embodied Carbon)
│   ├── software, employee_hardware, network_hardware, server_hardware
│   └── foundation_models, content_and_data (added in v0.1.0)
├── Direct Emissions (On-site Operations)
│   ├── onsite_employee_hardware, networking, servers (Scope 2)
│   └── generators (Scope 1, no method field)
├── Indirect Emissions (External Services)
│   └── offsite_employee_hardware, cloud_services, saas, managed_services
└── Downstream Emissions (Customer Impact)
    └── customer_devices, network_data_transfer, downstream_infrastructure
```

### Scope 2 Methods
Direct emissions (except generators) support optional Scope 2 methodology:
- `location-based`: Based on grid average emissions
- `market-based`: Based on purchased energy attributes
- `mixed-methods`: Combination of both
- `other`: Alternative methodology

## CLI Development

### CLI Framework
- Use **Click** for command-line interface
- Use **Rich** for formatted output (tables, colors)
- Provide helpful error messages
- Support common workflows: validate, migrate, totals, fetch

### Entry Point
Configure in `pyproject.toml`:
```toml
[project.scripts]
tcs = "pytcsschemahelper.cli.commands:cli"
```

## Migration Guidelines

### Version Migration
- Document all breaking changes between versions
- Provide migration functions for common upgrade paths
- Support field renames (e.g., `end_user_devices` → `customer_devices` in v0.1.0)
- Maintain backward compatibility where possible

### Migration Example
```python
from pytcsschemahelper.migration import migrate_document

migrated = migrate_document(
    document=old_doc,
    target_tcs_version=TCSVersion.V0_1_0
)
```

## License

This project uses **CC0 1.0 Universal (Public Domain Dedication)**. All code is dedicated to the public domain with no rights reserved.

## CI/CD

### GitHub Actions
- Run tests on all supported Python versions (3.9-3.13)
- Run linting (ruff) and type checking (mypy)
- Generate coverage reports
- Publish to PyPI on tagged releases

### Pre-commit Hooks
- ruff (linting + formatting)
- mypy (type checking)
- pytest (run tests before commit if desired)

## Common Tasks

### Adding a New Emission Field
1. Add field to appropriate model (`UpstreamEmissions`, `DirectEmissions`, etc.)
2. Update builder methods to support the new field
3. Add tests for the new field
4. Update documentation
5. Consider migration impact if changing existing fields

### Adding a New Schema Version
1. Add version to appropriate enum (`TCSVersion`, `EmissionsReportVersion`, etc.)
2. Create model variants if structure changes significantly
3. Update compatibility matrix
4. Add migration logic if needed
5. Update tests and documentation

### Creating Utility Functions
- Place in `utils.py`
- Ensure type hints and docstrings
- Add comprehensive tests
- Consider edge cases (empty reports, missing data)

## Resources

- **TCS Official Website**: https://www.techcarbonstandard.org/
- **TCS JSON Schemas**: https://www.techcarbonstandard.org/schemas/
- **Project Spec**: See `docs/pytcsschemahelper-spec.md`
- **Project Plan**: See `docs/pytcsschemahelper-project-plan.md`

## Best Practices

1. **Always validate** documents against JSON schemas before saving
2. **Use the builder** for most document creation tasks
3. **Provide helpful notes** in emission fields to explain methodology
4. **Test roundtrip serialization** to ensure data integrity
5. **Check version compatibility** when mixing schema versions
6. **Document examples** in docstrings for complex features
7. **Handle optional fields** gracefully with proper defaults
8. **Maintain backward compatibility** unless major version bump
9. **Write focused tests** that test one thing at a time
10. **Update CHANGELOG.md** for all user-facing changes
