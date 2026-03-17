"""Budget category hierarchy for government spending."""

from __future__ import annotations

from dataclasses import dataclass, field

from budgetmap.models import BudgetCategoryType


@dataclass
class BudgetCategory:
    """A node in the budget category hierarchy."""

    name: str
    category_type: BudgetCategoryType
    subcategories: list[str] = field(default_factory=list)
    parent: str | None = None
    description: str = ""

    @property
    def is_top_level(self) -> bool:
        return self.parent is None

    def has_subcategory(self, name: str) -> bool:
        return name.lower() in [s.lower() for s in self.subcategories]


# ── US Federal Budget Category Hierarchy ─────────────────────────────────

DEFENSE = BudgetCategory(
    name="National Defense",
    category_type=BudgetCategoryType.DEFENSE,
    subcategories=[
        "Military Personnel",
        "Operations & Maintenance",
        "Procurement",
        "Research & Development",
        "Military Construction",
        "Atomic Energy Defense",
        "Defense-Related Activities",
    ],
    description="Department of Defense and related military spending",
)

SOCIAL_SECURITY = BudgetCategory(
    name="Social Security",
    category_type=BudgetCategoryType.SOCIAL_SECURITY,
    subcategories=[
        "Old-Age & Survivors Insurance",
        "Disability Insurance",
        "Supplemental Security Income",
    ],
    description="Social Security Administration programs",
)

HEALTHCARE = BudgetCategory(
    name="Healthcare",
    category_type=BudgetCategoryType.HEALTHCARE,
    subcategories=[
        "Medicare",
        "Medicaid",
        "Children's Health Insurance",
        "NIH",
        "CDC",
        "FDA",
        "Indian Health Service",
        "Substance Abuse & Mental Health",
    ],
    description="HHS and healthcare-related spending",
)

EDUCATION = BudgetCategory(
    name="Education",
    category_type=BudgetCategoryType.EDUCATION,
    subcategories=[
        "K-12 Education Grants",
        "Pell Grants",
        "Student Loans Administration",
        "Special Education",
        "Head Start",
        "Career & Technical Education",
    ],
    description="Department of Education programs",
)

VETERANS_AFFAIRS = BudgetCategory(
    name="Veterans Affairs",
    category_type=BudgetCategoryType.VETERANS_AFFAIRS,
    subcategories=[
        "VA Healthcare",
        "Disability Compensation",
        "Education Benefits (GI Bill)",
        "VA Housing Programs",
        "Veterans Pensions",
    ],
    description="Department of Veterans Affairs programs",
)

INFRASTRUCTURE = BudgetCategory(
    name="Infrastructure & Transportation",
    category_type=BudgetCategoryType.INFRASTRUCTURE,
    subcategories=[
        "Federal Highway Administration",
        "Federal Aviation Administration",
        "Federal Transit Administration",
        "Federal Railroad Administration",
        "Army Corps of Engineers",
        "Broadband Infrastructure",
    ],
    description="Department of Transportation and infrastructure investment",
)

ENERGY = BudgetCategory(
    name="Energy",
    category_type=BudgetCategoryType.ENERGY,
    subcategories=[
        "National Nuclear Security Admin",
        "Energy Programs",
        "Environmental Cleanup",
        "Renewable Energy",
        "Strategic Petroleum Reserve",
    ],
    description="Department of Energy programs",
)

SCIENCE_TECHNOLOGY = BudgetCategory(
    name="Science & Technology",
    category_type=BudgetCategoryType.SCIENCE_TECHNOLOGY,
    subcategories=[
        "NASA",
        "National Science Foundation",
        "NOAA",
        "USGS",
    ],
    description="Science, space, and technology agencies",
)

AGRICULTURE = BudgetCategory(
    name="Agriculture",
    category_type=BudgetCategoryType.AGRICULTURE,
    subcategories=[
        "SNAP (Food Stamps)",
        "Farm Subsidies",
        "Forest Service",
        "Crop Insurance",
        "Rural Development",
    ],
    description="Department of Agriculture and food programs",
)

JUSTICE = BudgetCategory(
    name="Justice & Law Enforcement",
    category_type=BudgetCategoryType.JUSTICE,
    subcategories=[
        "FBI",
        "Federal Bureau of Prisons",
        "DEA",
        "ATF",
        "US Marshals Service",
        "Immigration Courts",
    ],
    description="Department of Justice and law enforcement",
)

INTERNATIONAL_AFFAIRS = BudgetCategory(
    name="International Affairs",
    category_type=BudgetCategoryType.INTERNATIONAL_AFFAIRS,
    subcategories=[
        "Diplomatic Programs",
        "Foreign Aid (USAID)",
        "International Organizations",
        "Peace Corps",
    ],
    description="State Department, USAID, and international engagement",
)

INTEREST_ON_DEBT = BudgetCategory(
    name="Interest on Federal Debt",
    category_type=BudgetCategoryType.INTEREST_ON_DEBT,
    subcategories=[
        "Net Interest",
    ],
    description="Interest payments on the national debt",
)

GENERAL_GOVERNMENT = BudgetCategory(
    name="General Government",
    category_type=BudgetCategoryType.GENERAL_GOVERNMENT,
    subcategories=[
        "Legislative Branch",
        "Executive Office of the President",
        "Treasury Department Administration",
        "IRS",
        "GSA",
        "OPM",
    ],
    description="General government operations and overhead",
)


# ── Registry ─────────────────────────────────────────────────────────────

ALL_CATEGORIES: list[BudgetCategory] = [
    DEFENSE,
    SOCIAL_SECURITY,
    HEALTHCARE,
    EDUCATION,
    VETERANS_AFFAIRS,
    INFRASTRUCTURE,
    ENERGY,
    SCIENCE_TECHNOLOGY,
    AGRICULTURE,
    JUSTICE,
    INTERNATIONAL_AFFAIRS,
    INTEREST_ON_DEBT,
    GENERAL_GOVERNMENT,
]

CATEGORY_MAP: dict[BudgetCategoryType, BudgetCategory] = {
    c.category_type: c for c in ALL_CATEGORIES
}


def get_category(category_type: BudgetCategoryType) -> BudgetCategory:
    """Look up a category by its enum type."""
    return CATEGORY_MAP[category_type]


def get_all_subcategories() -> list[str]:
    """Return a flat list of every subcategory across all top-level categories."""
    subs: list[str] = []
    for cat in ALL_CATEGORIES:
        subs.extend(cat.subcategories)
    return subs
