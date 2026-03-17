"""Generate comprehensive budget reports."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from budgetmap.analyzer.allocation import AllocationAnalyzer
from budgetmap.analyzer.trends import TrendAnalyzer
from budgetmap.analyzer.waste import WasteDetector
from budgetmap.budget.comparator import YearOverYearComparator
from budgetmap.models import Budget
from budgetmap.visualizer.tables import BudgetTables


class BudgetReport:
    """Generate a full budget report to the console."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()
        self.tables = BudgetTables(self.console)

    def single_year_report(self, budget: Budget) -> None:
        """Print a comprehensive report for a single fiscal year."""
        self.console.print()
        self.console.rule(f"[bold blue]BudgetMap Report — FY{budget.fiscal_year}[/bold blue]")
        self.console.print()

        # Summary
        self.console.print(self.tables.summary_table(budget))
        self.console.print()

        # Category breakdown
        self.console.print(self.tables.category_table(budget))
        self.console.print()

        # Allocation analysis
        alloc = AllocationAnalyzer(budget)
        top_depts = alloc.top_departments(5)
        if top_depts:
            self.console.print(Panel(
                "\n".join(
                    f"  {i+1}. {name}: ${amt:,.1f}B ({pct:.1f}%)"
                    for i, (name, amt, pct) in enumerate(top_depts)
                ),
                title="Top 5 Departments by Spending",
                border_style="green",
            ))
            self.console.print()

        # Per-capita
        pc = alloc.per_capita_total()
        gdp_r = alloc.gdp_ratio_total()
        if pc is not None or gdp_r is not None:
            lines = []
            if pc is not None:
                lines.append(f"  Per Capita Spending: ${pc:,.0f}")
            if gdp_r is not None:
                lines.append(f"  Spending as % of GDP: {gdp_r * 100:.1f}%")
            self.console.print(Panel(
                "\n".join(lines),
                title="Key Metrics",
                border_style="cyan",
            ))
            self.console.print()

    def comparison_report(
        self, budget_a: Budget, budget_b: Budget
    ) -> None:
        """Print a comparison report between two fiscal years."""
        self.console.print()
        self.console.rule(
            f"[bold blue]BudgetMap Comparison — "
            f"FY{budget_a.fiscal_year} vs FY{budget_b.fiscal_year}[/bold blue]"
        )
        self.console.print()

        comparator = YearOverYearComparator([budget_a, budget_b])
        comp = comparator.compare(budget_a.fiscal_year, budget_b.fiscal_year)
        self.console.print(self.tables.comparison_table(comp))
        self.console.print()

        # Fastest growing
        fastest = comparator.fastest_growing_departments(5)
        if fastest:
            self.console.print(Panel(
                "\n".join(
                    f"  {name}: +${change:,.1f}B"
                    for name, change in fastest if change > 0
                ),
                title="Fastest Growing Departments",
                border_style="green",
            ))
            self.console.print()

    def trend_report(self, budgets: dict[int, Budget]) -> None:
        """Print a trend analysis report across multiple years."""
        self.console.print()
        self.console.rule("[bold blue]BudgetMap Trend Analysis[/bold blue]")
        self.console.print()

        analyzer = TrendAnalyzer(budgets)

        # Total spending over time
        self.console.print(Panel(
            "\n".join(
                f"  FY{yr}: ${budgets[yr].total_spending:,.1f}B"
                for yr in analyzer.years
            ),
            title="Total Spending by Year",
            border_style="cyan",
        ))
        self.console.print()

        # Growth rates
        rates = analyzer.compute_growth_rates()
        if rates:
            self.console.print(Panel(
                "\n".join(
                    f"  FY{yr}: {rate:+.1f}%"
                    for yr, rate in rates.items()
                ) + f"\n  CAGR: {analyzer.compound_annual_growth_rate():.1f}%",
                title="Year-over-Year Growth",
                border_style="yellow",
            ))
            self.console.print()

        # Forecast
        forecast = analyzer.forecast_total(3)
        if forecast:
            self.console.print(Panel(
                "\n".join(
                    f"  FY{yr}: ${val:,.1f}B (projected)"
                    for yr, val in forecast.items()
                ),
                title="Spending Forecast (Linear)",
                border_style="magenta",
            ))
            self.console.print()

    def waste_report(self, budgets: dict[int, Budget]) -> None:
        """Print anomaly detection results."""
        self.console.print()
        self.console.rule("[bold red]BudgetMap Anomaly Detection[/bold red]")
        self.console.print()

        detector = WasteDetector(budgets)
        anomalies = detector.detect_all()

        if anomalies:
            self.console.print(self.tables.anomaly_table(anomalies))
        else:
            self.console.print("[green]No spending anomalies detected.[/green]")
        self.console.print()
