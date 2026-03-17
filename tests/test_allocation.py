"""Tests for AllocationAnalyzer."""

import pytest

from budgetmap.analyzer.allocation import AllocationAnalyzer
from budgetmap.data.us_budget import get_us_budget


class TestAllocationAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return AllocationAnalyzer(get_us_budget(2024))

    def test_per_capita_total(self, analyzer):
        pc = analyzer.per_capita_total()
        assert pc is not None
        # Should be several thousand dollars per person
        assert 10_000 < pc < 50_000

    def test_per_capita_by_department(self, analyzer):
        result = analyzer.per_capita_by_department()
        assert len(result) > 0
        assert "Department of Defense" in result
        assert result["Department of Defense"] > 0

    def test_per_capita_by_category(self, analyzer):
        result = analyzer.per_capita_by_category()
        assert "defense" in result
        assert "healthcare" in result

    def test_gdp_ratio_total(self, analyzer):
        ratio = analyzer.gdp_ratio_total()
        assert ratio is not None
        # US spending is roughly 20-25% of GDP
        assert 0.10 < ratio < 0.40

    def test_gdp_ratio_by_department(self, analyzer):
        result = analyzer.gdp_ratio_by_department()
        assert len(result) > 0

    def test_proportions_by_department(self, analyzer):
        props = analyzer.proportions_by_department()
        total = sum(props.values())
        assert abs(total - 1.0) < 0.01

    def test_proportions_by_category(self, analyzer):
        props = analyzer.proportions_by_category()
        total = sum(props.values())
        assert abs(total - 1.0) < 0.01

    def test_top_departments(self, analyzer):
        top = analyzer.top_departments(3)
        assert len(top) == 3
        # Top dept should have highest spending
        assert top[0][1] >= top[1][1] >= top[2][1]
