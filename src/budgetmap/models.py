"""Pydantic models for budget data."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BudgetCategoryType(str, Enum):
    """Top-level budget category types."""

    DEFENSE = "defense"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    INFRASTRUCTURE = "infrastructure"
    SOCIAL_SECURITY = "social_security"
    VETERANS_AFFAIRS = "veterans_affairs"
    SCIENCE_TECHNOLOGY = "science_technology"
    AGRICULTURE = "agriculture"
    ENERGY = "energy"
    JUSTICE = "justice"
    INTERNATIONAL_AFFAIRS = "international_affairs"
    GENERAL_GOVERNMENT = "general_government"
    INTEREST_ON_DEBT = "interest_on_debt"
    OTHER = "other"


class LineItem(BaseModel):
    """A single budget line item."""

    name: str
    amount: float = Field(description="Amount in billions of USD")
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None

    @property
    def amount_millions(self) -> float:
        """Return amount in millions."""
        return self.amount * 1000.0

    @property
    def amount_raw(self) -> float:
        """Return amount in raw dollars."""
        return self.amount * 1_000_000_000.0


class Department(BaseModel):
    """A government department with its budget."""

    name: str
    category: BudgetCategoryType
    line_items: list[LineItem] = Field(default_factory=list)

    @property
    def total(self) -> float:
        """Total spending in billions."""
        return sum(item.amount for item in self.line_items)

    def add_item(self, name: str, amount: float, subcategory: str | None = None,
                 description: str | None = None) -> None:
        """Add a line item to this department."""
        self.line_items.append(LineItem(
            name=name,
            amount=amount,
            category=self.name,
            subcategory=subcategory,
            description=description,
        ))


class Budget(BaseModel):
    """A complete government budget for a fiscal year."""

    fiscal_year: int
    country: str = "United States"
    departments: list[Department] = Field(default_factory=list)
    gdp: Optional[float] = Field(None, description="GDP in trillions of USD")
    population: Optional[int] = Field(None, description="Population count")

    @property
    def total_spending(self) -> float:
        """Total spending in billions."""
        return sum(dept.total for dept in self.departments)

    @property
    def per_capita(self) -> float | None:
        """Spending per capita in dollars."""
        if self.population and self.population > 0:
            return (self.total_spending * 1_000_000_000) / self.population
        return None

    @property
    def gdp_ratio(self) -> float | None:
        """Total spending as a ratio of GDP."""
        if self.gdp and self.gdp > 0:
            return self.total_spending / (self.gdp * 1000)  # gdp in trillions -> billions
        return None

    def get_department(self, name: str) -> Department | None:
        """Find a department by name."""
        for dept in self.departments:
            if dept.name.lower() == name.lower():
                return dept
        return None

    def get_by_category(self, category: BudgetCategoryType) -> list[Department]:
        """Get all departments in a given category."""
        return [d for d in self.departments if d.category == category]

    def category_totals(self) -> dict[str, float]:
        """Get total spending per category."""
        totals: dict[str, float] = {}
        for dept in self.departments:
            key = dept.category.value
            totals[key] = totals.get(key, 0) + dept.total
        return totals


class BudgetComparison(BaseModel):
    """Comparison between two budget years."""

    year_a: int
    year_b: int
    budget_a_total: float = Field(description="Total spending year A in billions")
    budget_b_total: float = Field(description="Total spending year B in billions")
    department_changes: dict[str, float] = Field(
        default_factory=dict,
        description="Change in spending per department (billions)",
    )
    category_changes: dict[str, float] = Field(
        default_factory=dict,
        description="Change in spending per category (billions)",
    )

    @property
    def total_change(self) -> float:
        """Absolute change in total spending (billions)."""
        return self.budget_b_total - self.budget_a_total

    @property
    def total_change_pct(self) -> float:
        """Percentage change in total spending."""
        if self.budget_a_total == 0:
            return 0.0
        return (self.total_change / self.budget_a_total) * 100

    @property
    def biggest_increase(self) -> tuple[str, float] | None:
        """Department with largest spending increase."""
        if not self.department_changes:
            return None
        name = max(self.department_changes, key=self.department_changes.get)  # type: ignore[arg-type]
        return name, self.department_changes[name]

    @property
    def biggest_decrease(self) -> tuple[str, float] | None:
        """Department with largest spending decrease."""
        if not self.department_changes:
            return None
        name = min(self.department_changes, key=self.department_changes.get)  # type: ignore[arg-type]
        return name, self.department_changes[name]
