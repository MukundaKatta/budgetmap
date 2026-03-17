"""Tests for the YearOverYearComparator."""

import pytest

from budgetmap.budget.comparator import YearOverYearComparator
from budgetmap.data.us_budget import get_all_us_budgets, get_us_budget


class TestYearOverYearComparator:
    @pytest.fixture
    def comparator(self):
        return YearOverYearComparator(get_all_us_budgets())

    def test_years(self, comparator):
        assert comparator.years == [2020, 2021, 2022, 2023, 2024]

    def test_compare_two_years(self, comparator):
        comp = comparator.compare(2020, 2024)
        assert comp.year_a == 2020
        assert comp.year_b == 2024
        assert comp.total_change > 0  # spending increased

    def test_compare_department_changes(self, comparator):
        comp = comparator.compare(2020, 2024)
        assert "Department of Defense" in comp.department_changes
        assert comp.department_changes["Department of Defense"] > 0

    def test_compare_consecutive(self, comparator):
        results = comparator.compare_consecutive()
        assert len(results) == 4  # 5 years -> 4 pairs

    def test_spending_by_department_over_time(self, comparator):
        data = comparator.spending_by_department_over_time()
        assert "Department of Defense" in data
        assert len(data["Department of Defense"]) == 5

    def test_spending_by_category_over_time(self, comparator):
        data = comparator.spending_by_category_over_time()
        assert "defense" in data
        assert "healthcare" in data

    def test_fastest_growing(self, comparator):
        fastest = comparator.fastest_growing_departments(3)
        assert len(fastest) == 3
        # All should have positive growth
        assert all(change > 0 for _, change in fastest)

    def test_init_with_list(self):
        budgets = [get_us_budget(2020), get_us_budget(2024)]
        comp = YearOverYearComparator(budgets)
        assert comp.years == [2020, 2024]
