"""
TCS Schema Version Management

This module defines version enums and compatibility utilities for the Technology
Carbon Standard (TCS) schema system.

The TCS uses a four-schema modular architecture:
- Router Schema (unversioned): Entry point that routes to appropriate schema versions
- Reporting Organisation Schema (versioned): Root document structure
- Emissions Report Schema (versioned): Individual report structure
- Tech Carbon Standard Schema (versioned): Emissions data structure

Each versioned schema evolves independently but maintains compatibility with specific
versions of other schemas. The Router schema (index.json) is unversioned and routes
documents based on their root `schema_version` field to the appropriate Reporting
Organisation schema version.
"""

from enum import Enum


class ReportingOrgVersion(str, Enum):
    """
    Enum for Reporting Organisation schema versions.

    The Reporting Organisation schema defines the root document structure for
    organizations reporting their technology carbon emissions.
    """
    V0_0_1 = "0.0.1"
    V0_1_0 = "0.1.0"
    V0_1_1 = "0.1.1"
    V0_1_2 = "0.1.2"


class EmissionsReportVersion(str, Enum):
    """
    Enum for Emissions Report schema versions.

    The Emissions Report schema defines the structure for individual emissions
    reports within a reporting organisation's document.
    """
    V0_0_1 = "0.0.1"
    V0_0_2 = "0.0.2"
    V0_0_3 = "0.0.3"


class TCSVersion(str, Enum):
    """
    Enum for Tech Carbon Standard (TCS) schema versions.

    The TCS schema defines the structure for actual emissions data within
    emissions reports.
    """
    V0_0_1 = "0.0.1"
    V0_0_2 = "0.0.2"
    V0_1_0 = "0.1.0"


# Default version constants pointing to the latest stable versions
DEFAULT_REPORTING_ORG_VERSION = ReportingOrgVersion.V0_1_2
DEFAULT_EMISSIONS_REPORT_VERSION = EmissionsReportVersion.V0_0_3
DEFAULT_TCS_VERSION = TCSVersion.V0_1_0

# Router schema URL (unversioned entry point)
ROUTER_SCHEMA_URL = "https://techcarbonstandard.org/schemas/index.json"

# Version compatibility matrices
REPORTING_ORG_COMPATIBILITY: dict[ReportingOrgVersion, list[EmissionsReportVersion]] = {
    ReportingOrgVersion.V0_1_2: [
        EmissionsReportVersion.V0_0_1,
        EmissionsReportVersion.V0_0_2,
        EmissionsReportVersion.V0_0_3,
    ],
    ReportingOrgVersion.V0_1_1: [
        EmissionsReportVersion.V0_0_1,
        EmissionsReportVersion.V0_0_2,
        EmissionsReportVersion.V0_0_3,
    ],
    ReportingOrgVersion.V0_1_0: [
        EmissionsReportVersion.V0_0_1,
        EmissionsReportVersion.V0_0_2,
    ],
    ReportingOrgVersion.V0_0_1: [
        EmissionsReportVersion.V0_0_1,
    ],
}

EMISSIONS_REPORT_COMPATIBILITY: dict[EmissionsReportVersion, list[TCSVersion]] = {
    EmissionsReportVersion.V0_0_3: [
        TCSVersion.V0_0_1,
        TCSVersion.V0_0_2,
        TCSVersion.V0_1_0,
    ],
    EmissionsReportVersion.V0_0_2: [
        TCSVersion.V0_0_1,
        TCSVersion.V0_0_2,
    ],
    EmissionsReportVersion.V0_0_1: [
        TCSVersion.V0_0_1,
    ],
}


def is_emissions_report_compatible(
    reporting_org_version: ReportingOrgVersion,
    emissions_report_version: EmissionsReportVersion
) -> bool:
    """
    Check if an Emissions Report version is compatible with a Reporting Org version.

    Args:
        reporting_org_version: The Reporting Organisation schema version
        emissions_report_version: The Emissions Report schema version to check

    Returns:
        True if the versions are compatible, False otherwise

    Example:
        >>> is_emissions_report_compatible(
        ...     ReportingOrgVersion.V0_1_2,
        ...     EmissionsReportVersion.V0_0_3
        ... )
        True
        >>> is_emissions_report_compatible(
        ...     ReportingOrgVersion.V0_0_1,
        ...     EmissionsReportVersion.V0_0_3
        ... )
        False
    """
    compatible_versions = REPORTING_ORG_COMPATIBILITY.get(reporting_org_version, [])
    return emissions_report_version in compatible_versions


def is_tcs_compatible(
    emissions_report_version: EmissionsReportVersion,
    tcs_version: TCSVersion
) -> bool:
    """
    Check if a TCS schema version is compatible with an Emissions Report version.

    Args:
        emissions_report_version: The Emissions Report schema version
        tcs_version: The TCS schema version to check

    Returns:
        True if the versions are compatible, False otherwise

    Example:
        >>> is_tcs_compatible(
        ...     EmissionsReportVersion.V0_0_3,
        ...     TCSVersion.V0_1_0
        ... )
        True
        >>> is_tcs_compatible(
        ...     EmissionsReportVersion.V0_0_1,
        ...     TCSVersion.V0_1_0
        ... )
        False
    """
    compatible_versions = EMISSIONS_REPORT_COMPATIBILITY.get(emissions_report_version, [])
    return tcs_version in compatible_versions
