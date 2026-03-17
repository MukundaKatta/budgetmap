"""Trend analysis and forecasting for budget data."""

from __future__ import annotations

import numpy as np

from budgetmap.models import Budget


class TrendAnalyzer:
    """Analyze spending trends across multiple budget years."""

    def __init__(self, budgets: dict[int, Budget] | list[Budget]) -> None:
        if isinstance(budgets, list):
            self.budgets = {b.fiscal_year: b for b in budgets}
        else:
            self.budgets = dict(budgets)

    @property
    def years(self) -> list[int]:
        return sorted(self.budgets.keys())

    @property
    def totals(self) -> list[float]:
        """Total spending per year, in order."""
        return [self.budgets[y].total_spending for y in self.years]

    # ── Growth rates ──────────────────────────────────────────────────────

    def compute_growth_rates(self) -> dict[int, float]:
        """Year-over-year growth rate (%) for total spending.

        Returns {year: pct_change} starting from the second year.
        """
        yrs = self.years
        totals = self.totals
        rates: dict[int, float] = {}
        for i in range(1, len(yrs)):
            if totals[i - 1] != 0:
                rates[yrs[i]] = ((totals[i] - totals[i - 1]) / totals[i - 1]) * 100
        return rates

    def compound_annual_growth_rate(self) -> float:
        """CAGR across the full time range (%)."""
        totals = self.totals
        if len(totals) < 2 or totals[0] == 0:
            return 0.0
        n = len(totals) - 1
        return ((totals[-1] / totals[0]) ** (1 / n) - 1) * 100

    def category_growth_rates(self) -> dict[str, dict[int, float]]:
        """Year-over-year growth rates per category.

        Returns {category: {year: pct_change}}.
        """
        cat_by_year: dict[str, dict[int, float]] = {}
        for yr in self.years:
            for cat, total in self.budgets[yr].category_totals().items():
                cat_by_year.setdefault(cat, {})[yr] = total

        result: dict[str, dict[int, float]] = {}
        for cat, yr_totals in cat_by_year.items():
            yrs = sorted(yr_totals.keys())
            rates: dict[int, float] = {}
            for i in range(1, len(yrs)):
                prev = yr_totals[yrs[i - 1]]
                curr = yr_totals[yrs[i]]
                if prev != 0:
                    rates[yrs[i]] = ((curr - prev) / prev) * 100
            result[cat] = rates

        return result

    # ── Forecasting ───────────────────────────────────────────────────────

    def forecast_total(self, years_ahead: int = 3) -> dict[int, float]:
        """Simple linear regression forecast for total spending.

        Returns {year: predicted_spending_billions} for future years.
        """
        yrs = np.array(self.years, dtype=float)
        vals = np.array(self.totals, dtype=float)

        if len(yrs) < 2:
            return {}

        # Linear fit: spending = slope * year + intercept
        coeffs = np.polyfit(yrs, vals, 1)
        slope, intercept = coeffs

        last_year = int(yrs[-1])
        predictions: dict[int, float] = {}
        for i in range(1, years_ahead + 1):
            future_yr = last_year + i
            predicted = slope * future_yr + intercept
            predictions[future_yr] = round(float(predicted), 1)

        return predictions

    def forecast_category(
        self, category: str, years_ahead: int = 3
    ) -> dict[int, float]:
        """Linear forecast for a specific category."""
        cat_by_year: dict[int, float] = {}
        for yr in self.years:
            totals = self.budgets[yr].category_totals()
            if category in totals:
                cat_by_year[yr] = totals[category]

        if len(cat_by_year) < 2:
            return {}

        yrs = np.array(sorted(cat_by_year.keys()), dtype=float)
        vals = np.array([cat_by_year[int(y)] for y in yrs], dtype=float)

        coeffs = np.polyfit(yrs, vals, 1)
        slope, intercept = coeffs

        last_year = int(yrs[-1])
        predictions: dict[int, float] = {}
        for i in range(1, years_ahead + 1):
            future_yr = last_year + i
            predicted = slope * future_yr + intercept
            predictions[future_yr] = round(float(predicted), 1)

        return predictions

    # ── Summary statistics ────────────────────────────────────────────────

    def average_annual_spending(self) -> float:
        """Mean total spending across all years (billions)."""
        return float(np.mean(self.totals))

    def spending_volatility(self) -> float:
        """Standard deviation of total spending (billions)."""
        return float(np.std(self.totals))
