"""
Unit tests for the versions module.

Tests version enums, compatibility matrices, and helper functions.
"""

from pytcsschemahelper.versions import (
    DEFAULT_EMISSIONS_REPORT_VERSION,
    DEFAULT_REPORTING_ORG_VERSION,
    DEFAULT_TCS_VERSION,
    EMISSIONS_REPORT_COMPATIBILITY,
    REPORTING_ORG_COMPATIBILITY,
    ROUTER_SCHEMA_URL,
    EmissionsReportVersion,
    ReportingOrgVersion,
    TCSVersion,
    is_emissions_report_compatible,
    is_tcs_compatible,
)


class TestVersionEnums:
    """Test version enum definitions."""

    def test_reporting_org_version_values(self):
        """Test that ReportingOrgVersion enum has correct values."""
        assert ReportingOrgVersion.V0_0_1 == "0.0.1"
        assert ReportingOrgVersion.V0_1_0 == "0.1.0"
        assert ReportingOrgVersion.V0_1_1 == "0.1.1"
        assert ReportingOrgVersion.V0_1_2 == "0.1.2"

    def test_emissions_report_version_values(self):
        """Test that EmissionsReportVersion enum has correct values."""
        assert EmissionsReportVersion.V0_0_1 == "0.0.1"
        assert EmissionsReportVersion.V0_0_2 == "0.0.2"
        assert EmissionsReportVersion.V0_0_3 == "0.0.3"

    def test_tcs_version_values(self):
        """Test that TCSVersion enum has correct values."""
        assert TCSVersion.V0_0_1 == "0.0.1"
        assert TCSVersion.V0_0_2 == "0.0.2"
        assert TCSVersion.V0_1_0 == "0.1.0"

    def test_enums_are_string_enums(self):
        """Test that version enums inherit from str for easy comparison."""
        assert isinstance(ReportingOrgVersion.V0_1_2, str)
        assert isinstance(EmissionsReportVersion.V0_0_3, str)
        assert isinstance(TCSVersion.V0_1_0, str)

    def test_reporting_org_version_count(self):
        """Test that ReportingOrgVersion has exactly 4 versions."""
        assert len(ReportingOrgVersion) == 4

    def test_emissions_report_version_count(self):
        """Test that EmissionsReportVersion has exactly 3 versions."""
        assert len(EmissionsReportVersion) == 3

    def test_tcs_version_count(self):
        """Test that TCSVersion has exactly 3 versions."""
        assert len(TCSVersion) == 3


class TestDefaultConstants:
    """Test default version constants."""

    def test_default_reporting_org_version(self):
        """Test that default Reporting Org version is the latest."""
        assert DEFAULT_REPORTING_ORG_VERSION == ReportingOrgVersion.V0_1_2
        assert DEFAULT_REPORTING_ORG_VERSION == "0.1.2"

    def test_default_emissions_report_version(self):
        """Test that default Emissions Report version is the latest."""
        assert DEFAULT_EMISSIONS_REPORT_VERSION == EmissionsReportVersion.V0_0_3
        assert DEFAULT_EMISSIONS_REPORT_VERSION == "0.0.3"

    def test_default_tcs_version(self):
        """Test that default TCS version is the latest."""
        assert DEFAULT_TCS_VERSION == TCSVersion.V0_1_0
        assert DEFAULT_TCS_VERSION == "0.1.0"

    def test_router_schema_url(self):
        """Test that Router schema URL is correct."""
        assert ROUTER_SCHEMA_URL == "https://techcarbonstandard.org/schemas/index.json"


class TestReportingOrgCompatibility:
    """Test Reporting Org to Emissions Report compatibility matrix."""

    def test_v0_1_2_compatibility(self):
        """Test ReportingOrgVersion.V0_1_2 compatibility."""
        compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_1_2]
        assert EmissionsReportVersion.V0_0_1 in compatible
        assert EmissionsReportVersion.V0_0_2 in compatible
        assert EmissionsReportVersion.V0_0_3 in compatible
        assert len(compatible) == 3

    def test_v0_1_1_compatibility(self):
        """Test ReportingOrgVersion.V0_1_1 compatibility."""
        compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_1_1]
        assert EmissionsReportVersion.V0_0_1 in compatible
        assert EmissionsReportVersion.V0_0_2 in compatible
        assert EmissionsReportVersion.V0_0_3 in compatible
        assert len(compatible) == 3

    def test_v0_1_0_compatibility(self):
        """Test ReportingOrgVersion.V0_1_0 compatibility."""
        compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_1_0]
        assert EmissionsReportVersion.V0_0_1 in compatible
        assert EmissionsReportVersion.V0_0_2 in compatible
        assert EmissionsReportVersion.V0_0_3 not in compatible
        assert len(compatible) == 2

    def test_v0_0_1_compatibility(self):
        """Test ReportingOrgVersion.V0_0_1 compatibility."""
        compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_0_1]
        assert EmissionsReportVersion.V0_0_1 in compatible
        assert EmissionsReportVersion.V0_0_2 not in compatible
        assert EmissionsReportVersion.V0_0_3 not in compatible
        assert len(compatible) == 1

    def test_all_versions_have_compatibility_entries(self):
        """Test that all Reporting Org versions have compatibility entries."""
        for version in ReportingOrgVersion:
            assert version in REPORTING_ORG_COMPATIBILITY
            assert isinstance(REPORTING_ORG_COMPATIBILITY[version], list)
            assert len(REPORTING_ORG_COMPATIBILITY[version]) > 0


class TestEmissionsReportCompatibility:
    """Test Emissions Report to TCS compatibility matrix."""

    def test_v0_0_3_compatibility(self):
        """Test EmissionsReportVersion.V0_0_3 compatibility."""
        compatible = EMISSIONS_REPORT_COMPATIBILITY[EmissionsReportVersion.V0_0_3]
        assert TCSVersion.V0_0_1 in compatible
        assert TCSVersion.V0_0_2 in compatible
        assert TCSVersion.V0_1_0 in compatible
        assert len(compatible) == 3

    def test_v0_0_2_compatibility(self):
        """Test EmissionsReportVersion.V0_0_2 compatibility."""
        compatible = EMISSIONS_REPORT_COMPATIBILITY[EmissionsReportVersion.V0_0_2]
        assert TCSVersion.V0_0_1 in compatible
        assert TCSVersion.V0_0_2 in compatible
        assert TCSVersion.V0_1_0 not in compatible
        assert len(compatible) == 2

    def test_v0_0_1_compatibility(self):
        """Test EmissionsReportVersion.V0_0_1 compatibility."""
        compatible = EMISSIONS_REPORT_COMPATIBILITY[EmissionsReportVersion.V0_0_1]
        assert TCSVersion.V0_0_1 in compatible
        assert TCSVersion.V0_0_2 not in compatible
        assert TCSVersion.V0_1_0 not in compatible
        assert len(compatible) == 1

    def test_all_versions_have_compatibility_entries(self):
        """Test that all Emissions Report versions have compatibility entries."""
        for version in EmissionsReportVersion:
            assert version in EMISSIONS_REPORT_COMPATIBILITY
            assert isinstance(EMISSIONS_REPORT_COMPATIBILITY[version], list)
            assert len(EMISSIONS_REPORT_COMPATIBILITY[version]) > 0


class TestIsEmissionsReportCompatible:
    """Test is_emissions_report_compatible helper function."""

    def test_v0_1_2_with_v0_0_3_compatible(self):
        """Test that Reporting Org 0.1.2 is compatible with Emissions Report 0.0.3."""
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_1_2,
            EmissionsReportVersion.V0_0_3
        ) is True

    def test_v0_1_2_with_v0_0_2_compatible(self):
        """Test that Reporting Org 0.1.2 is compatible with Emissions Report 0.0.2."""
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_1_2,
            EmissionsReportVersion.V0_0_2
        ) is True

    def test_v0_1_2_with_v0_0_1_compatible(self):
        """Test that Reporting Org 0.1.2 is compatible with Emissions Report 0.0.1."""
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_1_2,
            EmissionsReportVersion.V0_0_1
        ) is True

    def test_v0_1_0_with_v0_0_3_incompatible(self):
        """Test that Reporting Org 0.1.0 is not compatible with Emissions Report 0.0.3."""
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_1_0,
            EmissionsReportVersion.V0_0_3
        ) is False

    def test_v0_0_1_with_v0_0_2_incompatible(self):
        """Test that Reporting Org 0.0.1 is not compatible with Emissions Report 0.0.2."""
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_0_1,
            EmissionsReportVersion.V0_0_2
        ) is False

    def test_v0_0_1_with_v0_0_3_incompatible(self):
        """Test that Reporting Org 0.0.1 is not compatible with Emissions Report 0.0.3."""
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_0_1,
            EmissionsReportVersion.V0_0_3
        ) is False

    def test_all_documented_compatibilities(self):
        """Test all documented compatibility relationships."""
        # V0_1_2 compatible with all Emissions Report versions
        for emissions_version in EmissionsReportVersion:
            assert is_emissions_report_compatible(
                ReportingOrgVersion.V0_1_2,
                emissions_version
            ) is True

        # V0_1_1 compatible with all Emissions Report versions
        for emissions_version in EmissionsReportVersion:
            assert is_emissions_report_compatible(
                ReportingOrgVersion.V0_1_1,
                emissions_version
            ) is True

        # V0_1_0 compatible with V0_0_1 and V0_0_2 only
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_1_0,
            EmissionsReportVersion.V0_0_1
        ) is True
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_1_0,
            EmissionsReportVersion.V0_0_2
        ) is True

        # V0_0_1 compatible with V0_0_1 only
        assert is_emissions_report_compatible(
            ReportingOrgVersion.V0_0_1,
            EmissionsReportVersion.V0_0_1
        ) is True


class TestIsTCSCompatible:
    """Test is_tcs_compatible helper function."""

    def test_v0_0_3_with_v0_1_0_compatible(self):
        """Test that Emissions Report 0.0.3 is compatible with TCS 0.1.0."""
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_3,
            TCSVersion.V0_1_0
        ) is True

    def test_v0_0_3_with_v0_0_2_compatible(self):
        """Test that Emissions Report 0.0.3 is compatible with TCS 0.0.2."""
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_3,
            TCSVersion.V0_0_2
        ) is True

    def test_v0_0_3_with_v0_0_1_compatible(self):
        """Test that Emissions Report 0.0.3 is compatible with TCS 0.0.1."""
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_3,
            TCSVersion.V0_0_1
        ) is True

    def test_v0_0_2_with_v0_1_0_incompatible(self):
        """Test that Emissions Report 0.0.2 is not compatible with TCS 0.1.0."""
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_2,
            TCSVersion.V0_1_0
        ) is False

    def test_v0_0_1_with_v0_0_2_incompatible(self):
        """Test that Emissions Report 0.0.1 is not compatible with TCS 0.0.2."""
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_1,
            TCSVersion.V0_0_2
        ) is False

    def test_v0_0_1_with_v0_1_0_incompatible(self):
        """Test that Emissions Report 0.0.1 is not compatible with TCS 0.1.0."""
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_1,
            TCSVersion.V0_1_0
        ) is False

    def test_all_documented_compatibilities(self):
        """Test all documented compatibility relationships."""
        # V0_0_3 compatible with all TCS versions
        for tcs_version in TCSVersion:
            assert is_tcs_compatible(
                EmissionsReportVersion.V0_0_3,
                tcs_version
            ) is True

        # V0_0_2 compatible with V0_0_1 and V0_0_2 only
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_2,
            TCSVersion.V0_0_1
        ) is True
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_2,
            TCSVersion.V0_0_2
        ) is True

        # V0_0_1 compatible with V0_0_1 only
        assert is_tcs_compatible(
            EmissionsReportVersion.V0_0_1,
            TCSVersion.V0_0_1
        ) is True


class TestCompatibilityEdgeCases:
    """Test edge cases and error handling for compatibility functions."""

    def test_returns_boolean_type(self):
        """Test that compatibility functions return actual boolean types."""
        result_true = is_emissions_report_compatible(
            ReportingOrgVersion.V0_1_2,
            EmissionsReportVersion.V0_0_3
        )
        result_false = is_emissions_report_compatible(
            ReportingOrgVersion.V0_0_1,
            EmissionsReportVersion.V0_0_3
        )
        assert isinstance(result_true, bool)
        assert isinstance(result_false, bool)

        result_true = is_tcs_compatible(
            EmissionsReportVersion.V0_0_3,
            TCSVersion.V0_1_0
        )
        result_false = is_tcs_compatible(
            EmissionsReportVersion.V0_0_1,
            TCSVersion.V0_1_0
        )
        assert isinstance(result_true, bool)
        assert isinstance(result_false, bool)


class TestVersionProgression:
    """Test that version progressions maintain backwards compatibility where expected."""

    def test_newer_reporting_org_versions_support_more_or_equal_emissions_versions(self):
        """Test that newer Reporting Org versions don't lose compatibility."""
        v0_0_1_compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_0_1]
        v0_1_0_compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_1_0]
        v0_1_1_compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_1_1]
        v0_1_2_compatible = REPORTING_ORG_COMPATIBILITY[ReportingOrgVersion.V0_1_2]

        # Each version should support at least as many as the previous
        assert len(v0_1_0_compatible) >= len(v0_0_1_compatible)
        assert len(v0_1_1_compatible) >= len(v0_1_0_compatible)
        assert len(v0_1_2_compatible) >= len(v0_1_1_compatible)

    def test_newer_emissions_versions_support_more_or_equal_tcs_versions(self):
        """Test that newer Emissions Report versions don't lose compatibility."""
        v0_0_1_compatible = EMISSIONS_REPORT_COMPATIBILITY[EmissionsReportVersion.V0_0_1]
        v0_0_2_compatible = EMISSIONS_REPORT_COMPATIBILITY[EmissionsReportVersion.V0_0_2]
        v0_0_3_compatible = EMISSIONS_REPORT_COMPATIBILITY[EmissionsReportVersion.V0_0_3]

        # Each version should support at least as many as the previous
        assert len(v0_0_2_compatible) >= len(v0_0_1_compatible)
        assert len(v0_0_3_compatible) >= len(v0_0_2_compatible)
