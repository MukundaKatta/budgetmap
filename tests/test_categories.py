"""Tests for budget categories."""

from budgetmap.budget.categories import (
    ALL_CATEGORIES,
    CATEGORY_MAP,
    DEFENSE,
    HEALTHCARE,
    get_all_subcategories,
    get_category,
)
from budgetmap.models import BudgetCategoryType


class TestCategories:
    def test_all_categories_populated(self):
        assert len(ALL_CATEGORIES) >= 12

    def test_defense_subcategories(self):
        assert "Military Personnel" in DEFENSE.subcategories
        assert "Procurement" in DEFENSE.subcategories

    def test_healthcare_subcategories(self):
        assert "Medicare" in HEALTHCARE.subcategories
        assert "Medicaid" in HEALTHCARE.subcategories

    def test_get_category(self):
        cat = get_category(BudgetCategoryType.DEFENSE)
        assert cat.name == "National Defense"

    def test_category_map_complete(self):
        for cat_type in BudgetCategoryType:
            if cat_type != BudgetCategoryType.OTHER:
                assert cat_type in CATEGORY_MAP

    def test_is_top_level(self):
        assert DEFENSE.is_top_level is True

    def test_has_subcategory(self):
        assert DEFENSE.has_subcategory("military personnel") is True
        assert DEFENSE.has_subcategory("nonexistent") is False

    def test_get_all_subcategories(self):
        subs = get_all_subcategories()
        assert len(subs) > 30
        assert "Medicare" in subs
        assert "NASA" in subs
