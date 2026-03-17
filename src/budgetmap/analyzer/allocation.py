"""Allocation analysis — per-capita, GDP ratios, and proportional breakdowns."""

from __future__ import annotations

from budgetmap.models import Budget


class AllocationAnalyzer:
    """Compute allocation metrics for budgets."""

    def __init__(self, budget: Budget) -> None:
        self.budget = budget

    # ── Per-capita ────────────────────────────────────────────────────────

    def per_capita_total(self) -> float | None:
        """Total federal spending per person (dollars)."""
        return self.budget.per_capita

    def per_capita_by_department(self) -> dict[str, float]:
        """Per-capita spending by department (dollars).

        Returns empty dict if population is not set.
        """
        if not self.budget.population or self.budget.population == 0:
            return {}
        pop = self.budget.population
        return {
            dept.name: round((dept.total * 1_000_000_000) / pop, 2)
            for dept in self.budget.departments
        }

    def per_capita_by_category(self) -> dict[str, float]:
        """Per-capita spending by category (dollars)."""
        if not self.budget.population or self.budget.population == 0:
            return {}
        pop = self.budget.population
        return {
            cat: round((total * 1_000_000_000) / pop, 2)
            for cat, total in self.budget.category_totals().items()
        }

    # ── GDP ratios ────────────────────────────────────────────────────────

    def gdp_ratio_total(self) -> float | None:
        """Total spending as a fraction of GDP."""
        return self.budget.gdp_ratio

    def gdp_ratio_by_department(self) -> dict[str, float]:
        """Each department's spending as a fraction of GDP.

        Returns empty dict if GDP is not set.
        """
        if not self.budget.gdp or self.budget.gdp == 0:
            return {}
        gdp_billions = self.budget.gdp * 1000
        return {
            dept.name: round(dept.total / gdp_billions, 6)
            for dept in self.budget.departments
        }

    def gdp_ratio_by_category(self) -> dict[str, float]:
        """Each category's spending as a fraction of GDP."""
        if not self.budget.gdp or self.budget.gdp == 0:
            return {}
        gdp_billions = self.budget.gdp * 1000
        return {
            cat: round(total / gdp_billions, 6)
            for cat, total in self.budget.category_totals().items()
        }

    # ── Proportional breakdown ────────────────────────────────────────────

    def proportions_by_department(self) -> dict[str, float]:
        """Each department's share of total spending (0-1)."""
        total = self.budget.total_spending
        if total == 0:
            return {}
        return {
            dept.name: round(dept.total / total, 6)
            for dept in self.budget.departments
        }

    def proportions_by_category(self) -> dict[str, float]:
        """Each category's share of total spending (0-1)."""
        total = self.budget.total_spending
        if total == 0:
            return {}
        return {
            cat: round(cat_total / total, 6)
            for cat, cat_total in self.budget.category_totals().items()
        }

    def top_departments(self, n: int = 5) -> list[tuple[str, float, float]]:
        """Top N departments by spending.

        Returns list of (name, amount_billions, pct_of_total).
        """
        total = self.budget.total_spending
        depts = sorted(
            self.budget.departments, key=lambda d: d.total, reverse=True
        )
        return [
            (d.name, round(d.total, 2), round(d.total / total * 100, 2) if total else 0)
            for d in depts[:n]
        ]
