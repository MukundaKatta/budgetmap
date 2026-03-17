"""Parse budget data from CSV and JSON files."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from budgetmap.models import Budget, BudgetCategoryType, Department, LineItem


class BudgetParser:
    """Read budget data from CSV or JSON files."""

    # Map common category strings to enum values
    CATEGORY_ALIASES: dict[str, BudgetCategoryType] = {
        "defense": BudgetCategoryType.DEFENSE,
        "national defense": BudgetCategoryType.DEFENSE,
        "military": BudgetCategoryType.DEFENSE,
        "education": BudgetCategoryType.EDUCATION,
        "healthcare": BudgetCategoryType.HEALTHCARE,
        "health": BudgetCategoryType.HEALTHCARE,
        "infrastructure": BudgetCategoryType.INFRASTRUCTURE,
        "transportation": BudgetCategoryType.INFRASTRUCTURE,
        "social security": BudgetCategoryType.SOCIAL_SECURITY,
        "social_security": BudgetCategoryType.SOCIAL_SECURITY,
        "veterans": BudgetCategoryType.VETERANS_AFFAIRS,
        "veterans affairs": BudgetCategoryType.VETERANS_AFFAIRS,
        "veterans_affairs": BudgetCategoryType.VETERANS_AFFAIRS,
        "science": BudgetCategoryType.SCIENCE_TECHNOLOGY,
        "science_technology": BudgetCategoryType.SCIENCE_TECHNOLOGY,
        "agriculture": BudgetCategoryType.AGRICULTURE,
        "energy": BudgetCategoryType.ENERGY,
        "justice": BudgetCategoryType.JUSTICE,
        "international": BudgetCategoryType.INTERNATIONAL_AFFAIRS,
        "international_affairs": BudgetCategoryType.INTERNATIONAL_AFFAIRS,
        "general": BudgetCategoryType.GENERAL_GOVERNMENT,
        "general_government": BudgetCategoryType.GENERAL_GOVERNMENT,
        "interest": BudgetCategoryType.INTEREST_ON_DEBT,
        "interest_on_debt": BudgetCategoryType.INTEREST_ON_DEBT,
        "other": BudgetCategoryType.OTHER,
    }

    def _resolve_category(self, raw: str) -> BudgetCategoryType:
        """Map a raw category string to a BudgetCategoryType."""
        key = raw.strip().lower()
        if key in self.CATEGORY_ALIASES:
            return self.CATEGORY_ALIASES[key]
        # Try matching the enum value directly
        try:
            return BudgetCategoryType(key)
        except ValueError:
            return BudgetCategoryType.OTHER

    # ── CSV ───────────────────────────────────────────────────────────────

    def parse_csv(self, path: str | Path) -> Budget:
        """Parse a CSV file into a Budget.

        Expected columns: fiscal_year, department, category, item_name,
        amount_billions.  Optional: subcategory, gdp_trillions, population.
        """
        path = Path(path)
        with path.open(newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        if not rows:
            raise ValueError(f"CSV file is empty: {path}")

        fiscal_year = int(rows[0]["fiscal_year"])
        gdp = float(rows[0].get("gdp_trillions") or 0) or None
        population = int(rows[0].get("population") or 0) or None

        dept_map: dict[str, Department] = {}
        for row in rows:
            dept_name = row["department"]
            cat = self._resolve_category(row.get("category", "other"))
            if dept_name not in dept_map:
                dept_map[dept_name] = Department(name=dept_name, category=cat)
            dept_map[dept_name].line_items.append(
                LineItem(
                    name=row["item_name"],
                    amount=float(row["amount_billions"]),
                    category=dept_name,
                    subcategory=row.get("subcategory"),
                )
            )

        return Budget(
            fiscal_year=fiscal_year,
            departments=list(dept_map.values()),
            gdp=gdp,
            population=population,
        )

    # ── JSON ──────────────────────────────────────────────────────────────

    def parse_json(self, path: str | Path) -> Budget:
        """Parse a JSON file into a Budget.

        Expected structure::

            {
                "fiscal_year": 2024,
                "country": "United States",
                "gdp_trillions": 28.78,
                "population": 336000000,
                "departments": [
                    {
                        "name": "Department of Defense",
                        "category": "defense",
                        "items": [
                            {"name": "Military Personnel", "amount_billions": 172.4},
                            ...
                        ]
                    },
                    ...
                ]
            }
        """
        path = Path(path)
        with path.open() as fh:
            data = json.load(fh)

        departments: list[Department] = []
        for dept_data in data.get("departments", []):
            cat = self._resolve_category(dept_data.get("category", "other"))
            items = [
                LineItem(
                    name=it["name"],
                    amount=float(it["amount_billions"]),
                    category=dept_data["name"],
                    subcategory=it.get("subcategory"),
                    description=it.get("description"),
                )
                for it in dept_data.get("items", [])
            ]
            departments.append(Department(
                name=dept_data["name"],
                category=cat,
                line_items=items,
            ))

        return Budget(
            fiscal_year=int(data["fiscal_year"]),
            country=data.get("country", "United States"),
            departments=departments,
            gdp=data.get("gdp_trillions"),
            population=data.get("population"),
        )

    # ── Multi-year ────────────────────────────────────────────────────────

    def parse_csv_multiyear(self, path: str | Path) -> dict[int, Budget]:
        """Parse a CSV that may contain multiple fiscal years.

        Returns a dict keyed by fiscal year.
        """
        path = Path(path)
        with path.open(newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        years: dict[int, list[dict]] = {}
        for row in rows:
            yr = int(row["fiscal_year"])
            years.setdefault(yr, []).append(row)

        budgets: dict[int, Budget] = {}
        for yr, yr_rows in sorted(years.items()):
            dept_map: dict[str, Department] = {}
            gdp = float(yr_rows[0].get("gdp_trillions") or 0) or None
            population = int(yr_rows[0].get("population") or 0) or None
            for row in yr_rows:
                dept_name = row["department"]
                cat = self._resolve_category(row.get("category", "other"))
                if dept_name not in dept_map:
                    dept_map[dept_name] = Department(name=dept_name, category=cat)
                dept_map[dept_name].line_items.append(
                    LineItem(
                        name=row["item_name"],
                        amount=float(row["amount_billions"]),
                        category=dept_name,
                        subcategory=row.get("subcategory"),
                    )
                )
            budgets[yr] = Budget(
                fiscal_year=yr,
                departments=list(dept_map.values()),
                gdp=gdp,
                population=population,
            )

        return budgets
