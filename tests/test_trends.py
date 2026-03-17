"""Tests for TrendAnalyzer."""

import pytest

from budgetmap.analyzer.trends import TrendAnalyzer
from budgetmap.data.us_budget import get_all_us_budgets


class TestTrendAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return TrendAnalyzer(get_all_us_budgets())

    def test_years(self, analyzer):
        assert analyzer.years == [2020, 2021, 2022, 2023, 2024]

    def test_totals_length(self, analyzer):
        assert len(analyzer.totals) == 5

    def test_growth_rates(self, analyzer):
        rates = analyzer.compute_growth_rates()
        # Should have rates for years 2021-2024
        assert len(rates) == 4
        assert 2021 in rates

    def test_cagr(self, analyzer):
        cagr = analyzer.compound_annual_growth_rate()
        assert cagr > 0  # spending has increased over time

    def test_category_growth_rates(self, analyzer):
        cat_rates = analyzer.category_growth_rates()
        assert "defense" in cat_rates
        assert "healthcare" in cat_rates

    def test_forecast_total(self, analyzer):
        forecast = analyzer.forecast_total(3)
        assert len(forecast) == 3
        assert 2025 in forecast
        assert 2026 in forecast
        assert 2027 in forecast
        # Forecasted spending should be positive
        assert all(v > 0 for v in forecast.values())

    def test_forecast_category(self, analyzer):
        forecast = analyzer.forecast_category("defense", 2)
        assert len(forecast) == 2
        assert all(v > 0 for v in forecast.values())

    def test_average_annual_spending(self, analyzer):
        avg = analyzer.average_annual_spending()
        assert avg > 3000  # at least $3T

    def test_spending_volatility(self, analyzer):
        vol = analyzer.spending_volatility()
        assert vol > 0
