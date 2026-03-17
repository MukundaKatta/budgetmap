# BudgetMap - Government Budget Visualizer

BudgetMap is a Python tool for parsing, analyzing, and visualizing government budget data. It provides insights into spending patterns, trends, and allocations across departments and fiscal years.

## Features

- **Budget Parsing**: Read budget data from CSV and JSON formats
- **Category Hierarchy**: Organized budget categories (Defense, Education, Healthcare, etc.)
- **Year-over-Year Comparison**: Track spending changes across fiscal years
- **Trend Analysis**: Growth rates, forecasting, and trend detection
- **Allocation Analysis**: Per-capita and GDP-ratio computations
- **Waste Detection**: Flag unusual spending patterns and anomalies
- **Visualizations**: Treemap, sunburst, bar, and line charts via matplotlib
- **Rich Tables**: Formatted terminal output using rich

## Installation

```bash
pip install -e .
```

## Usage

### CLI

```bash
# Show summary of US federal budget
budgetmap summary --year 2024

# Compare two fiscal years
budgetmap compare --year1 2022 --year2 2024

# Analyze trends across years
budgetmap trends --start 2020 --end 2024

# Detect potential waste
budgetmap waste --year 2024

# Generate charts
budgetmap chart --type treemap --year 2024
```

### Python API

```python
from budgetmap.budget.parser import BudgetParser
from budgetmap.analyzer.trends import TrendAnalyzer
from budgetmap.visualizer.charts import BudgetCharts

parser = BudgetParser()
budgets = parser.parse_json("budget_data.json")

analyzer = TrendAnalyzer(budgets)
trends = analyzer.compute_growth_rates()

charts = BudgetCharts()
charts.treemap(budgets[2024])
```

## Dependencies

- numpy
- matplotlib
- pydantic
- click
- rich

## License

MIT
