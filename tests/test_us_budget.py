"""Tests for US budget sample data."""

import pytest

from budgetmap.data.us_budget import (
    AVAILABLE_YEARS,
    get_all_us_budgets,
    get_us_budget,
)


class TestUSBudgetData:
    def test_available_years(self):
        assert AVAILABLE_YEARS == [2020, 2021, 2022, 2023, 2024]

    def test_get_budget_valid(self):
        budget = get_us_budget(2024)
        assert budget.fiscal_year == 2024
        assert budget.country == "United States"
        assert len(budget.departments) > 0

    def test_get_budget_invalid(self):
        with pytest.raises(ValueError, match="No data for FY1900"):
            get_us_budget(1900)

    def test_all_budgets(self):
        budgets = get_all_us_budgets()
        assert len(budgets) == 5
        assert all(yr in budgets for yr in AVAILABLE_YEARS)

    @pytest.mark.parametrize("year", AVAILABLE_YEARS)
    def test_budget_has_departments(self, year):
        budget = get_us_budget(year)
        assert len(budget.departments) >= 10

    @pytest.mark.parametrize("year", AVAILABLE_YEARS)
    def test_budget_has_gdp_and_population(self, year):
        budget = get_us_budget(year)
        assert budget.gdp is not None
        assert budget.gdp > 0
        assert budget.population is not None
        assert budget.population > 0

    @pytest.mark.parametrize("year", AVAILABLE_YEARS)
    def test_total_spending_reasonable(self, year):
        budget = get_us_budget(year)
        total = budget.total_spending
        # US federal budget is roughly 4-7 trillion
        assert 3000 < total < 8000, f"FY{year} total {total}B seems off"

    def test_spending_generally_increases(self):
        budgets = get_all_us_budgets()
        totals = [budgets[yr].total_spending for yr in sorted(budgets)]
        # Overall trend should be upward (first < last)
        assert totals[-1] > totals[0]

    def test_defense_department_present(self):
        budget = get_us_budget(2024)
        dept = budget.get_department("Department of Defense")
        assert dept is not None
        assert dept.total > 500  # > $500B

    def test_social_security_present(self):
        budget = get_us_budget(2024)
        dept = budget.get_department("Social Security Administration")
        assert dept is not None
        assert dept.total > 1000  # > $1T
