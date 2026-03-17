"""Rich-formatted table output for budget data."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from budgetmap.models import Budget, BudgetComparison


class BudgetTables:
    """Render budget data as rich formatted tables."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    # ── Budget summary ────────────────────────────────────────────────────

    def summary_table(self, budget: Budget) -> Table:
        """Render a summary table for a single budget year."""
        table = Table(
            title=f"US Federal Budget — FY{budget.fiscal_year}",
            show_header=True,
            header_style="bold cyan",
            title_style="bold white",
        )
        table.add_column("Department", style="white", min_width=35)
        table.add_column("Spending ($B)", justify="right", style="green")
        table.add_column("% of Total", justify="right", style="yellow")

        total = budget.total_spending
        depts = sorted(budget.departments, key=lambda d: d.total, reverse=True)

        for dept in depts:
            pct = (dept.total / total * 100) if total else 0
            table.add_row(
                dept.name,
                f"${dept.total:,.1f}",
                f"{pct:.1f}%",
            )

        table.add_section()
        table.add_row(
            "[bold]TOTAL[/bold]",
            f"[bold]${total:,.1f}[/bold]",
            "[bold]100.0%[/bold]",
        )

        if budget.per_capita is not None:
            table.add_row(
                "Per Capita",
                f"${budget.per_capita:,.0f}",
                "",
            )
        if budget.gdp_ratio is not None:
            table.add_row(
                "% of GDP",
                f"{budget.gdp_ratio * 100:.1f}%",
                "",
            )

        return table

    def print_summary(self, budget: Budget) -> None:
        """Print the summary table to the console."""
        self.console.print(self.summary_table(budget))

    # ── Department detail ─────────────────────────────────────────────────

    def department_detail_table(self, budget: Budget, dept_name: str) -> Table | None:
        """Render a detailed table for a specific department."""
        dept = budget.get_department(dept_name)
        if dept is None:
            return None

        table = Table(
            title=f"{dept.name} — FY{budget.fiscal_year}",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Line Item", style="white", min_width=30)
        table.add_column("Amount ($B)", justify="right", style="green")
        table.add_column("% of Dept", justify="right", style="yellow")

        dept_total = dept.total
        items = sorted(dept.line_items, key=lambda i: i.amount, reverse=True)
        for item in items:
            pct = (item.amount / dept_total * 100) if dept_total else 0
            table.add_row(item.name, f"${item.amount:,.1f}", f"{pct:.1f}%")

        table.add_section()
        table.add_row(
            "[bold]TOTAL[/bold]",
            f"[bold]${dept_total:,.1f}[/bold]",
            "[bold]100.0%[/bold]",
        )
        return table

    # ── Comparison table ──────────────────────────────────────────────────

    def comparison_table(self, comparison: BudgetComparison) -> Table:
        """Render a year-over-year comparison table."""
        table = Table(
            title=f"Budget Comparison: FY{comparison.year_a} vs FY{comparison.year_b}",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Department", style="white", min_width=35)
        table.add_column("Change ($B)", justify="right")
        table.add_column("Direction", justify="center")

        sorted_changes = sorted(
            comparison.department_changes.items(),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        for name, change in sorted_changes:
            if change > 0:
                style = "green"
                arrow = "[green]+[/green]"
            elif change < 0:
                style = "red"
                arrow = "[red]-[/red]"
            else:
                style = "dim"
                arrow = "="
            table.add_row(
                name,
                f"[{style}]${abs(change):,.1f}[/{style}]",
                arrow,
            )

        table.add_section()
        tc = comparison.total_change
        tc_style = "green" if tc >= 0 else "red"
        table.add_row(
            "[bold]NET CHANGE[/bold]",
            f"[bold {tc_style}]${abs(tc):,.1f}[/bold {tc_style}]",
            f"[bold {tc_style}]{comparison.total_change_pct:+.1f}%[/bold {tc_style}]",
        )

        return table

    def print_comparison(self, comparison: BudgetComparison) -> None:
        """Print the comparison table to the console."""
        self.console.print(self.comparison_table(comparison))

    # ── Category table ────────────────────────────────────────────────────

    def category_table(self, budget: Budget) -> Table:
        """Render spending by category."""
        table = Table(
            title=f"Spending by Category — FY{budget.fiscal_year}",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Category", style="white", min_width=25)
        table.add_column("Spending ($B)", justify="right", style="green")
        table.add_column("% of Total", justify="right", style="yellow")

        total = budget.total_spending
        cat_totals = budget.category_totals()
        for cat, amount in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
            pct = (amount / total * 100) if total else 0
            label = cat.replace("_", " ").title()
            table.add_row(label, f"${amount:,.1f}", f"{pct:.1f}%")

        return table

    # ── Anomaly table ─────────────────────────────────────────────────────

    def anomaly_table(self, anomalies: list) -> Table:
        """Render detected spending anomalies."""
        table = Table(
            title="Spending Anomalies Detected",
            show_header=True,
            header_style="bold red",
        )
        table.add_column("Severity", justify="center", min_width=8)
        table.add_column("Department", style="white", min_width=25)
        table.add_column("Description", style="white", min_width=40)
        table.add_column("Amount ($B)", justify="right", style="yellow")

        severity_style = {"high": "red", "medium": "yellow", "low": "dim"}

        for a in sorted(anomalies, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.severity, 3)):
            s = severity_style.get(a.severity, "white")
            table.add_row(
                f"[{s}]{a.severity.upper()}[/{s}]",
                a.department,
                a.description,
                f"${abs(a.amount_billions):,.1f}",
            )

        return table
