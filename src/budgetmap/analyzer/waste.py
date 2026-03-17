"""Waste detection — flag unusual spending patterns and anomalies."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from budgetmap.models import Budget


@dataclass
class SpendingAnomaly:
    """An anomalous spending pattern."""

    department: str
    item_name: str | None
    description: str
    severity: str  # "low", "medium", "high"
    amount_billions: float
    context: str = ""


class WasteDetector:
    """Flag unusual spending patterns across budget years."""

    def __init__(
        self,
        budgets: dict[int, Budget] | list[Budget],
        *,
        spike_threshold: float = 50.0,
        z_score_threshold: float = 2.0,
    ) -> None:
        if isinstance(budgets, list):
            self.budgets = {b.fiscal_year: b for b in budgets}
        else:
            self.budgets = dict(budgets)
        self.spike_threshold = spike_threshold  # % change that counts as a spike
        self.z_score_threshold = z_score_threshold

    @property
    def years(self) -> list[int]:
        return sorted(self.budgets.keys())

    def detect_all(self) -> list[SpendingAnomaly]:
        """Run all anomaly detectors and return combined results."""
        anomalies: list[SpendingAnomaly] = []
        anomalies.extend(self.detect_spending_spikes())
        anomalies.extend(self.detect_category_outliers())
        anomalies.extend(self.detect_disproportionate_items())
        return anomalies

    def detect_spending_spikes(self) -> list[SpendingAnomaly]:
        """Find departments with year-over-year spending increases above threshold."""
        anomalies: list[SpendingAnomaly] = []
        yrs = self.years
        if len(yrs) < 2:
            return anomalies

        for i in range(1, len(yrs)):
            prev_budget = self.budgets[yrs[i - 1]]
            curr_budget = self.budgets[yrs[i]]

            prev_totals = {d.name: d.total for d in prev_budget.departments}
            for dept in curr_budget.departments:
                prev = prev_totals.get(dept.name, 0)
                if prev == 0:
                    continue
                pct_change = ((dept.total - prev) / prev) * 100
                if abs(pct_change) >= self.spike_threshold:
                    direction = "increase" if pct_change > 0 else "decrease"
                    severity = "high" if abs(pct_change) >= 100 else "medium"
                    anomalies.append(SpendingAnomaly(
                        department=dept.name,
                        item_name=None,
                        description=(
                            f"{abs(pct_change):.1f}% {direction} in "
                            f"{dept.name} from FY{yrs[i-1]} to FY{yrs[i]}"
                        ),
                        severity=severity,
                        amount_billions=dept.total - prev,
                        context=f"FY{yrs[i-1]}: ${prev:.1f}B -> FY{yrs[i]}: ${dept.total:.1f}B",
                    ))

        return anomalies

    def detect_category_outliers(self) -> list[SpendingAnomaly]:
        """Use z-scores to find categories that deviate from their historical mean."""
        anomalies: list[SpendingAnomaly] = []
        if len(self.years) < 3:
            return anomalies

        cat_history: dict[str, list[float]] = {}
        cat_by_year: dict[str, dict[int, float]] = {}
        for yr in self.years:
            for cat, total in self.budgets[yr].category_totals().items():
                cat_history.setdefault(cat, []).append(total)
                cat_by_year.setdefault(cat, {})[yr] = total

        for cat, values in cat_history.items():
            arr = np.array(values)
            mean = float(np.mean(arr))
            std = float(np.std(arr))
            if std == 0:
                continue
            for idx, val in enumerate(values):
                z = (val - mean) / std
                if abs(z) >= self.z_score_threshold:
                    yr = self.years[idx]
                    direction = "above" if z > 0 else "below"
                    anomalies.append(SpendingAnomaly(
                        department=cat,
                        item_name=None,
                        description=(
                            f"{cat} spending in FY{yr} is {abs(z):.1f} std devs "
                            f"{direction} the historical mean"
                        ),
                        severity="high" if abs(z) >= 3 else "medium",
                        amount_billions=val,
                        context=f"Mean: ${mean:.1f}B, Std: ${std:.1f}B, FY{yr}: ${val:.1f}B",
                    ))

        return anomalies

    def detect_disproportionate_items(self) -> list[SpendingAnomaly]:
        """Flag individual line items that dominate their department's budget (>80%)."""
        anomalies: list[SpendingAnomaly] = []
        # Only check the latest year
        if not self.years:
            return anomalies

        budget = self.budgets[self.years[-1]]
        for dept in budget.departments:
            if len(dept.line_items) < 2:
                continue
            dept_total = dept.total
            if dept_total == 0:
                continue
            for item in dept.line_items:
                ratio = item.amount / dept_total
                if ratio > 0.80:
                    anomalies.append(SpendingAnomaly(
                        department=dept.name,
                        item_name=item.name,
                        description=(
                            f"'{item.name}' accounts for {ratio*100:.1f}% of "
                            f"{dept.name}'s budget"
                        ),
                        severity="low",
                        amount_billions=item.amount,
                        context=f"Item: ${item.amount:.1f}B / Dept total: ${dept_total:.1f}B",
                    ))

        return anomalies
