"""BudgetMap CLI — Government Budget Visualizer."""

from __future__ import annotations

import click
from rich.console import Console

from budgetmap.data.us_budget import AVAILABLE_YEARS, get_all_us_budgets, get_us_budget
from budgetmap.report import BudgetReport

console = Console()


@click.group()
@click.version_option(package_name="budgetmap")
def cli() -> None:
    """BudgetMap — Government Budget Visualizer.

    Analyze, compare, and visualize US federal budget data.
    """


@cli.command()
@click.option("--year", "-y", type=int, default=2024,
              help=f"Fiscal year ({AVAILABLE_YEARS[0]}-{AVAILABLE_YEARS[-1]})")
def summary(year: int) -> None:
    """Show a budget summary for a fiscal year."""
    try:
        budget = get_us_budget(year)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    report = BudgetReport(console)
    report.single_year_report(budget)


@cli.command()
@click.option("--year1", type=int, required=True, help="First fiscal year")
@click.option("--year2", type=int, required=True, help="Second fiscal year")
def compare(year1: int, year2: int) -> None:
    """Compare spending between two fiscal years."""
    try:
        b1 = get_us_budget(year1)
        b2 = get_us_budget(year2)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    report = BudgetReport(console)
    report.comparison_report(b1, b2)


@cli.command()
@click.option("--start", "-s", type=int, default=None,
              help="Start year (default: earliest available)")
@click.option("--end", "-e", type=int, default=None,
              help="End year (default: latest available)")
def trends(start: int | None, end: int | None) -> None:
    """Analyze spending trends over time."""
    all_budgets = get_all_us_budgets()
    if start:
        all_budgets = {y: b for y, b in all_budgets.items() if y >= start}
    if end:
        all_budgets = {y: b for y, b in all_budgets.items() if y <= end}

    if len(all_budgets) < 2:
        console.print("[red]Need at least 2 years for trend analysis.[/red]")
        raise SystemExit(1)

    report = BudgetReport(console)
    report.trend_report(all_budgets)


@cli.command()
@click.option("--year", "-y", type=int, default=None,
              help="Focus year (default: all years)")
def waste(year: int | None) -> None:
    """Detect unusual spending patterns."""
    if year:
        try:
            budgets = {year: get_us_budget(year)}
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise SystemExit(1)
    else:
        budgets = get_all_us_budgets()

    report = BudgetReport(console)
    report.waste_report(budgets)


@cli.command()
@click.option("--type", "chart_type", type=click.Choice(
    ["treemap", "sunburst", "bar", "line", "comparison"]),
    default="bar", help="Chart type")
@click.option("--year", "-y", type=int, default=2024, help="Fiscal year")
@click.option("--output", "-o", type=str, default=None,
              help="Output file path (e.g., chart.png)")
def chart(chart_type: str, year: int, output: str | None) -> None:
    """Generate a budget chart."""
    from budgetmap.visualizer.charts import BudgetCharts

    charts = BudgetCharts()

    try:
        budget = get_us_budget(year)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    if output is None:
        output = f"budget_{chart_type}_fy{year}.png"

    if chart_type == "treemap":
        charts.treemap(budget, output=output)
    elif chart_type == "sunburst":
        charts.sunburst(budget, output=output)
    elif chart_type == "bar":
        charts.bar_chart(budget, output=output)
    elif chart_type == "line":
        all_budgets = get_all_us_budgets()
        charts.line_chart(all_budgets, output=output)
    elif chart_type == "comparison":
        years = AVAILABLE_YEARS
        if len(years) >= 2:
            b1 = get_us_budget(years[0])
            b2 = get_us_budget(years[-1])
            charts.comparison_bar(b1, b2, output=output)

    console.print(f"[green]Chart saved to:[/green] {output}")


if __name__ == "__main__":
    cli()
