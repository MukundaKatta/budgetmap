"""Chart visualizations for budget data using matplotlib."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from budgetmap.models import Budget


class BudgetCharts:
    """Generate budget visualizations."""

    # Color palette for categories
    COLORS = [
        "#2196F3", "#F44336", "#4CAF50", "#FF9800", "#9C27B0",
        "#00BCD4", "#795548", "#607D8B", "#E91E63", "#8BC34A",
        "#FF5722", "#3F51B5", "#CDDC39", "#009688",
    ]

    def __init__(self, figsize: tuple[int, int] = (14, 8)) -> None:
        self.figsize = figsize

    def _save_or_show(self, fig: plt.Figure, output: str | Path | None) -> None:
        if output:
            fig.savefig(str(output), dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ── Treemap ───────────────────────────────────────────────────────────

    def treemap(
        self,
        budget: Budget,
        output: str | Path | None = None,
    ) -> plt.Figure:
        """Render a treemap of budget allocation by department.

        Uses nested rectangles sized proportionally to spending.
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()
        ax.set_title(
            f"US Federal Budget FY{budget.fiscal_year} — Treemap "
            f"(Total: ${budget.total_spending:,.1f}B)",
            fontsize=14, fontweight="bold", pad=15,
        )

        depts = sorted(budget.departments, key=lambda d: d.total, reverse=True)
        total = budget.total_spending
        if total == 0:
            self._save_or_show(fig, output)
            return fig

        # Simple squarified-style layout: stack horizontal slices
        y = 0.0
        for i, dept in enumerate(depts):
            h = dept.total / total
            color = self.COLORS[i % len(self.COLORS)]
            rect = mpatches.FancyBboxPatch(
                (0.02, y + 0.005), 0.96, max(h - 0.01, 0.001),
                boxstyle="round,pad=0.005",
                facecolor=color, edgecolor="white", linewidth=2, alpha=0.85,
            )
            ax.add_patch(rect)
            if h > 0.03:
                pct = dept.total / total * 100
                ax.text(
                    0.5, y + h / 2,
                    f"{dept.name}\n${dept.total:,.1f}B ({pct:.1f}%)",
                    ha="center", va="center", fontsize=9,
                    fontweight="bold", color="white",
                )
            y += h

        self._save_or_show(fig, output)
        return fig

    # ── Sunburst ──────────────────────────────────────────────────────────

    def sunburst(
        self,
        budget: Budget,
        output: str | Path | None = None,
    ) -> plt.Figure:
        """Render a sunburst (nested pie) chart.

        Outer ring = departments, inner ring = categories.
        """
        fig, ax = plt.subplots(figsize=(self.figsize[0], self.figsize[0]),
                               subplot_kw={"projection": "polar"})
        ax.set_title(
            f"US Federal Budget FY{budget.fiscal_year} — Sunburst",
            fontsize=14, fontweight="bold", y=1.08,
        )

        # Fall back to a two-ring pie chart
        cat_totals = budget.category_totals()
        cats = sorted(cat_totals.keys(), key=lambda c: cat_totals[c], reverse=True)
        cat_vals = [cat_totals[c] for c in cats]
        cat_colors = [self.COLORS[i % len(self.COLORS)] for i in range(len(cats))]

        dept_vals = [d.total for d in sorted(
            budget.departments, key=lambda d: d.total, reverse=True
        )]
        dept_names = [d.name for d in sorted(
            budget.departments, key=lambda d: d.total, reverse=True
        )]

        plt.close(fig)
        fig, ax = plt.subplots(figsize=self.figsize)

        # Inner ring: categories
        inner_wedges, inner_texts = ax.pie(
            cat_vals, radius=0.7, colors=cat_colors,
            wedgeprops=dict(width=0.3, edgecolor="white"),
        )

        # Outer ring: departments
        dept_colors = [self.COLORS[i % len(self.COLORS)] for i in range(len(dept_vals))]
        outer_wedges, outer_texts = ax.pie(
            dept_vals, radius=1.0, colors=dept_colors,
            wedgeprops=dict(width=0.3, edgecolor="white"),
        )

        ax.set_title(
            f"US Federal Budget FY{budget.fiscal_year} — Sunburst\n"
            f"Inner: Categories | Outer: Departments",
            fontsize=13, fontweight="bold",
        )

        # Legend for categories
        legend_patches = [
            mpatches.Patch(color=cat_colors[i], label=f"{cats[i]} (${cat_vals[i]:,.1f}B)")
            for i in range(len(cats))
        ]
        ax.legend(handles=legend_patches, loc="center left",
                  bbox_to_anchor=(1.05, 0.5), fontsize=8)

        self._save_or_show(fig, output)
        return fig

    # ── Bar chart ─────────────────────────────────────────────────────────

    def bar_chart(
        self,
        budget: Budget,
        output: str | Path | None = None,
        top_n: int = 12,
    ) -> plt.Figure:
        """Horizontal bar chart of department spending."""
        depts = sorted(budget.departments, key=lambda d: d.total, reverse=True)[:top_n]

        fig, ax = plt.subplots(figsize=self.figsize)
        names = [d.name for d in depts]
        values = [d.total for d in depts]
        colors = [self.COLORS[i % len(self.COLORS)] for i in range(len(depts))]

        bars = ax.barh(names[::-1], values[::-1], color=colors[::-1], edgecolor="white")

        for bar, val in zip(bars, values[::-1]):
            ax.text(
                bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                f"${val:,.1f}B", va="center", fontsize=9,
            )

        ax.set_xlabel("Spending (Billions USD)", fontsize=11)
        ax.set_title(
            f"US Federal Budget FY{budget.fiscal_year} — Department Spending",
            fontsize=14, fontweight="bold",
        )
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()

        self._save_or_show(fig, output)
        return fig

    # ── Line chart ────────────────────────────────────────────────────────

    def line_chart(
        self,
        budgets: dict[int, Budget],
        output: str | Path | None = None,
        categories: list[str] | None = None,
    ) -> plt.Figure:
        """Line chart of spending over time by category."""
        years = sorted(budgets.keys())
        cat_data: dict[str, list[float]] = {}
        for yr in years:
            for cat, total in budgets[yr].category_totals().items():
                cat_data.setdefault(cat, []).append(total)

        if categories:
            cat_data = {k: v for k, v in cat_data.items() if k in categories}

        fig, ax = plt.subplots(figsize=self.figsize)
        for i, (cat, values) in enumerate(sorted(
            cat_data.items(), key=lambda x: sum(x[1]), reverse=True
        )):
            color = self.COLORS[i % len(self.COLORS)]
            ax.plot(years, values, marker="o", label=cat, color=color, linewidth=2)

        ax.set_xlabel("Fiscal Year", fontsize=11)
        ax.set_ylabel("Spending (Billions USD)", fontsize=11)
        ax.set_title(
            "US Federal Budget — Spending Trends by Category",
            fontsize=14, fontweight="bold",
        )
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xticks(years)
        fig.tight_layout()

        self._save_or_show(fig, output)
        return fig

    # ── Comparison bar chart ──────────────────────────────────────────────

    def comparison_bar(
        self,
        budget_a: Budget,
        budget_b: Budget,
        output: str | Path | None = None,
        top_n: int = 10,
    ) -> plt.Figure:
        """Side-by-side bar chart comparing two budget years."""
        all_depts = sorted(
            {d.name for d in budget_a.departments} | {d.name for d in budget_b.departments}
        )

        totals_a = {d.name: d.total for d in budget_a.departments}
        totals_b = {d.name: d.total for d in budget_b.departments}

        # Sort by year B spending
        all_depts.sort(key=lambda n: totals_b.get(n, 0), reverse=True)
        all_depts = all_depts[:top_n]

        fig, ax = plt.subplots(figsize=self.figsize)
        x = np.arange(len(all_depts))
        width = 0.35

        vals_a = [totals_a.get(n, 0) for n in all_depts]
        vals_b = [totals_b.get(n, 0) for n in all_depts]

        ax.bar(x - width / 2, vals_a, width, label=f"FY{budget_a.fiscal_year}",
               color="#2196F3", alpha=0.8)
        ax.bar(x + width / 2, vals_b, width, label=f"FY{budget_b.fiscal_year}",
               color="#F44336", alpha=0.8)

        ax.set_xticks(x)
        ax.set_xticklabels(all_depts, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Spending (Billions USD)")
        ax.set_title(
            f"Budget Comparison: FY{budget_a.fiscal_year} vs FY{budget_b.fiscal_year}",
            fontsize=14, fontweight="bold",
        )
        ax.legend()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()

        self._save_or_show(fig, output)
        return fig
