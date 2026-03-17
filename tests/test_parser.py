"""Tests for BudgetParser."""

import json
import tempfile
from pathlib import Path

import pytest

from budgetmap.budget.parser import BudgetParser


class TestBudgetParser:
    @pytest.fixture
    def parser(self):
        return BudgetParser()

    def test_parse_json(self, parser, tmp_path):
        data = {
            "fiscal_year": 2024,
            "country": "United States",
            "gdp_trillions": 28.78,
            "population": 336000000,
            "departments": [
                {
                    "name": "Department of Defense",
                    "category": "defense",
                    "items": [
                        {"name": "Personnel", "amount_billions": 170.0},
                        {"name": "Procurement", "amount_billions": 150.0},
                    ],
                },
                {
                    "name": "Department of Education",
                    "category": "education",
                    "items": [
                        {"name": "Grants", "amount_billions": 80.0},
                    ],
                },
            ],
        }
        json_file = tmp_path / "budget.json"
        json_file.write_text(json.dumps(data))

        budget = parser.parse_json(json_file)
        assert budget.fiscal_year == 2024
        assert budget.country == "United States"
        assert len(budget.departments) == 2
        assert budget.total_spending == 400.0
        assert budget.gdp == 28.78
        assert budget.population == 336000000

    def test_parse_csv(self, parser, tmp_path):
        csv_content = (
            "fiscal_year,department,category,item_name,amount_billions\n"
            "2024,Defense,defense,Personnel,170.0\n"
            "2024,Defense,defense,Procurement,150.0\n"
            "2024,Education,education,Grants,80.0\n"
        )
        csv_file = tmp_path / "budget.csv"
        csv_file.write_text(csv_content)

        budget = parser.parse_csv(csv_file)
        assert budget.fiscal_year == 2024
        assert len(budget.departments) == 2
        assert budget.total_spending == 400.0

    def test_parse_csv_empty(self, parser, tmp_path):
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("fiscal_year,department,category,item_name,amount_billions\n")
        with pytest.raises(ValueError, match="empty"):
            parser.parse_csv(csv_file)

    def test_resolve_category_aliases(self, parser):
        from budgetmap.models import BudgetCategoryType
        assert parser._resolve_category("defense") == BudgetCategoryType.DEFENSE
        assert parser._resolve_category("military") == BudgetCategoryType.DEFENSE
        assert parser._resolve_category("health") == BudgetCategoryType.HEALTHCARE
        assert parser._resolve_category("unknown_thing") == BudgetCategoryType.OTHER

    def test_parse_csv_multiyear(self, parser, tmp_path):
        csv_content = (
            "fiscal_year,department,category,item_name,amount_billions\n"
            "2023,Defense,defense,Personnel,160.0\n"
            "2024,Defense,defense,Personnel,170.0\n"
        )
        csv_file = tmp_path / "multi.csv"
        csv_file.write_text(csv_content)

        budgets = parser.parse_csv_multiyear(csv_file)
        assert 2023 in budgets
        assert 2024 in budgets
        assert budgets[2023].total_spending == 160.0
        assert budgets[2024].total_spending == 170.0
