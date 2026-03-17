"""Year-over-year budget comparison."""

from __future__ import annotations

from budgetmap.models import Budget, BudgetComparison


class YearOverYearComparator:
    """Compare budgets across fiscal years."""

    def __init__(self, budgets: dict[int, Budget] | list[Budget]) -> None:
        if isinstance(budgets, list):
            self.budgets = {b.fiscal_year: b for b in budgets}
        else:
            self.budgets = dict(budgets)

    @property
    def years(self) -> list[int]:
        return sorted(self.budgets.keys())

    def compare(self, year_a: int, year_b: int) -> BudgetComparison:
        """Compare two budget years and return a BudgetComparison."""
        ba = self.budgets[year_a]
        bb = self.budgets[year_b]

        # Department-level changes
        dept_totals_a: dict[str, float] = {}
        for dept in ba.departments:
            dept_totals_a[dept.name] = dept.total

        dept_totals_b: dict[str, float] = {}
        for dept in bb.departments:
            dept_totals_b[dept.name] = dept.total

        all_depts = set(dept_totals_a) | set(dept_totals_b)
        dept_changes = {
            name: dept_totals_b.get(name, 0.0) - dept_totals_a.get(name, 0.0)
            for name in all_depts
        }

        # Category-level changes
        cat_a = ba.category_totals()
        cat_b = bb.category_totals()
        all_cats = set(cat_a) | set(cat_b)
        cat_changes = {
            cat: cat_b.get(cat, 0.0) - cat_a.get(cat, 0.0)
            for cat in all_cats
        }

        return BudgetComparison(
            year_a=year_a,
            year_b=year_b,
            budget_a_total=ba.total_spending,
            budget_b_total=bb.total_spending,
            department_changes=dept_changes,
            category_changes=cat_changes,
        )

    def compare_consecutive(self) -> list[BudgetComparison]:
        """Compare each consecutive pair of years."""
        yrs = self.years
        return [self.compare(yrs[i], yrs[i + 1]) for i in range(len(yrs) - 1)]

    def spending_by_department_over_time(self) -> dict[str, dict[int, float]]:
        """Return {department_name: {year: total}} for all years."""
        result: dict[str, dict[int, float]] = {}
        for yr, budget in sorted(self.budgets.items()):
            for dept in budget.departments:
                result.setdefault(dept.name, {})[yr] = dept.total
        return result

    def spending_by_category_over_time(self) -> dict[str, dict[int, float]]:
        """Return {category: {year: total}} for all years."""
        result: dict[str, dict[int, float]] = {}
        for yr, budget in sorted(self.budgets.items()):
            for cat, total in budget.category_totals().items():
                result.setdefault(cat, {})[yr] = total
        return result

    def fastest_growing_departments(self, top_n: int = 5) -> list[tuple[str, float]]:
        """Return the top-N departments by total absolute growth across all years.

        Returns list of (dept_name, total_growth_billions).
        """
        if len(self.years) < 2:
            return []
        first_yr = self.years[0]
        last_yr = self.years[-1]
        comp = self.compare(first_yr, last_yr)
        sorted_depts = sorted(
            comp.department_changes.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_depts[:top_n]
