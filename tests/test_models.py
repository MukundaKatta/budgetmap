"""Tests for budget models."""

import pytest

from budgetmap.models import (
    Budget,
    BudgetCategoryType,
    BudgetComparison,
    Department,
    LineItem,
)


class TestLineItem:
    def test_creation(self):
        item = LineItem(name="Test Item", amount=50.0, category="test")
        assert item.name == "Test Item"
        assert item.amount == 50.0

    def test_amount_millions(self):
        item = LineItem(name="Test", amount=1.5, category="test")
        assert item.amount_millions == 1500.0

    def test_amount_raw(self):
        item = LineItem(name="Test", amount=1.0, category="test")
        assert item.amount_raw == 1_000_000_000.0


class TestDepartment:
    def test_total(self):
        dept = Department(
            name="Test Dept",
            category=BudgetCategoryType.DEFENSE,
            line_items=[
                LineItem(name="A", amount=10.0, category="Test Dept"),
                LineItem(name="B", amount=20.0, category="Test Dept"),
            ],
        )
        assert dept.total == 30.0

    def test_add_item(self):
        dept = Department(name="Dept", category=BudgetCategoryType.EDUCATION)
        dept.add_item("Grants", 5.0)
        assert len(dept.line_items) == 1
        assert dept.total == 5.0

    def test_empty_total(self):
        dept = Department(name="Empty", category=BudgetCategoryType.OTHER)
        assert dept.total == 0.0


class TestBudget:
    @pytest.fixture
    def sample_budget(self):
        return Budget(
            fiscal_year=2024,
            gdp=28.78,
            population=336_000_000,
            departments=[
                Department(
                    name="Defense",
                    category=BudgetCategoryType.DEFENSE,
                    line_items=[
                        LineItem(name="Personnel", amount=170.0, category="Defense"),
                        LineItem(name="Procurement", amount=150.0, category="Defense"),
                    ],
                ),
                Department(
                    name="Education",
                    category=BudgetCategoryType.EDUCATION,
                    line_items=[
                        LineItem(name="Grants", amount=80.0, category="Education"),
                    ],
                ),
            ],
        )

    def test_total_spending(self, sample_budget):
        assert sample_budget.total_spending == 400.0

    def test_per_capita(self, sample_budget):
        pc = sample_budget.per_capita
        assert pc is not None
        expected = (400.0 * 1e9) / 336_000_000
        assert abs(pc - expected) < 0.01

    def test_gdp_ratio(self, sample_budget):
        ratio = sample_budget.gdp_ratio
        assert ratio is not None
        expected = 400.0 / (28.78 * 1000)
        assert abs(ratio - expected) < 0.0001

    def test_get_department(self, sample_budget):
        dept = sample_budget.get_department("defense")
        assert dept is not None
        assert dept.name == "Defense"

    def test_get_department_missing(self, sample_budget):
        assert sample_budget.get_department("nonexistent") is None

    def test_category_totals(self, sample_budget):
        totals = sample_budget.category_totals()
        assert totals["defense"] == 320.0
        assert totals["education"] == 80.0

    def test_per_capita_no_population(self):
        budget = Budget(fiscal_year=2024)
        assert budget.per_capita is None

    def test_gdp_ratio_no_gdp(self):
        budget = Budget(fiscal_year=2024)
        assert budget.gdp_ratio is None


class TestBudgetComparison:
    def test_total_change(self):
        comp = BudgetComparison(
            year_a=2020, year_b=2024,
            budget_a_total=4000.0, budget_b_total=5000.0,
            department_changes={"Defense": 100.0, "Education": -20.0},
        )
        assert comp.total_change == 1000.0
        assert abs(comp.total_change_pct - 25.0) < 0.01

    def test_biggest_increase(self):
        comp = BudgetComparison(
            year_a=2020, year_b=2024,
            budget_a_total=4000.0, budget_b_total=5000.0,
            department_changes={"Defense": 100.0, "Education": 50.0},
        )
        name, val = comp.biggest_increase
        assert name == "Defense"
        assert val == 100.0

    def test_biggest_decrease(self):
        comp = BudgetComparison(
            year_a=2020, year_b=2024,
            budget_a_total=4000.0, budget_b_total=5000.0,
            department_changes={"Defense": 100.0, "Education": -20.0},
        )
        name, val = comp.biggest_decrease
        assert name == "Education"
        assert val == -20.0
