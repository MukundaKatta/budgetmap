"""Sample US federal budget data 2020-2024.

Amounts are in billions of USD. Data is approximate and based on publicly
available US federal budget summaries. Figures reflect total outlays
(mandatory + discretionary) per major function.
"""

from __future__ import annotations

from budgetmap.models import Budget, BudgetCategoryType, Department, LineItem


def _make_department(
    name: str,
    category: BudgetCategoryType,
    items: list[tuple[str, float]],
) -> Department:
    """Helper to build a Department with line items."""
    return Department(
        name=name,
        category=category,
        line_items=[
            LineItem(name=n, amount=a, category=name) for n, a in items
        ],
    )


# ── US population estimates (millions → int) ────────────────────────────
_US_POP = {
    2020: 331_000_000,
    2021: 332_000_000,
    2022: 333_000_000,
    2023: 335_000_000,
    2024: 336_000_000,
}

# ── US GDP estimates (trillions) ─────────────────────────────────────────
_US_GDP = {
    2020: 21.06,
    2021: 23.32,
    2022: 25.46,
    2023: 27.36,
    2024: 28.78,
}


def _build_fy2020() -> Budget:
    """FY2020 — includes COVID CARES Act spike."""
    return Budget(
        fiscal_year=2020,
        gdp=_US_GDP[2020],
        population=_US_POP[2020],
        departments=[
            _make_department("Department of Defense", BudgetCategoryType.DEFENSE, [
                ("Military Personnel", 155.8),
                ("Operations & Maintenance", 287.5),
                ("Procurement", 137.9),
                ("Research & Development", 99.5),
                ("Military Construction", 12.3),
            ]),
            _make_department("Social Security Administration", BudgetCategoryType.SOCIAL_SECURITY, [
                ("Old-Age & Survivors Insurance", 853.0),
                ("Disability Insurance", 148.0),
                ("Supplemental Security Income", 57.0),
            ]),
            _make_department("Department of Health & Human Services", BudgetCategoryType.HEALTHCARE, [
                ("Medicare", 776.0),
                ("Medicaid", 458.0),
                ("Children's Health Insurance", 17.3),
                ("NIH", 42.9),
                ("CDC", 12.7),
                ("FDA", 5.9),
            ]),
            _make_department("Department of Education", BudgetCategoryType.EDUCATION, [
                ("K-12 Education Grants", 40.2),
                ("Pell Grants", 28.8),
                ("Student Loans Administration", 25.1),
                ("Special Education", 13.9),
            ]),
            _make_department("Department of Veterans Affairs", BudgetCategoryType.VETERANS_AFFAIRS, [
                ("VA Healthcare", 86.6),
                ("Disability Compensation", 105.0),
                ("Education Benefits (GI Bill)", 12.5),
                ("VA Housing Programs", 3.2),
            ]),
            _make_department("Department of Transportation", BudgetCategoryType.INFRASTRUCTURE, [
                ("Federal Highway Administration", 49.7),
                ("Federal Aviation Administration", 17.4),
                ("Federal Transit Administration", 13.6),
                ("Federal Railroad Administration", 2.9),
            ]),
            _make_department("Department of Energy", BudgetCategoryType.ENERGY, [
                ("National Nuclear Security Admin", 19.8),
                ("Energy Programs", 10.2),
                ("Environmental Cleanup", 6.9),
            ]),
            _make_department("NASA & Science", BudgetCategoryType.SCIENCE_TECHNOLOGY, [
                ("NASA", 22.6),
                ("National Science Foundation", 8.3),
            ]),
            _make_department("Department of Agriculture", BudgetCategoryType.AGRICULTURE, [
                ("SNAP (Food Stamps)", 79.1),
                ("Farm Subsidies", 46.1),
                ("Forest Service", 7.4),
            ]),
            _make_department("Department of Justice", BudgetCategoryType.JUSTICE, [
                ("FBI", 9.8),
                ("Federal Bureau of Prisons", 8.0),
                ("DEA", 3.1),
                ("ATF", 1.4),
            ]),
            _make_department("State Department & USAID", BudgetCategoryType.INTERNATIONAL_AFFAIRS, [
                ("Diplomatic Programs", 15.2),
                ("Foreign Aid (USAID)", 23.1),
                ("International Organizations", 4.2),
            ]),
            _make_department("Interest on Federal Debt", BudgetCategoryType.INTEREST_ON_DEBT, [
                ("Net Interest", 345.0),
            ]),
        ],
    )


def _build_fy2021() -> Budget:
    """FY2021 — continued pandemic spending."""
    return Budget(
        fiscal_year=2021,
        gdp=_US_GDP[2021],
        population=_US_POP[2021],
        departments=[
            _make_department("Department of Defense", BudgetCategoryType.DEFENSE, [
                ("Military Personnel", 158.1),
                ("Operations & Maintenance", 293.0),
                ("Procurement", 142.3),
                ("Research & Development", 106.6),
                ("Military Construction", 10.5),
            ]),
            _make_department("Social Security Administration", BudgetCategoryType.SOCIAL_SECURITY, [
                ("Old-Age & Survivors Insurance", 895.0),
                ("Disability Insurance", 150.0),
                ("Supplemental Security Income", 59.0),
            ]),
            _make_department("Department of Health & Human Services", BudgetCategoryType.HEALTHCARE, [
                ("Medicare", 829.0),
                ("Medicaid", 521.0),
                ("Children's Health Insurance", 17.8),
                ("NIH", 45.2),
                ("CDC", 16.3),
                ("FDA", 6.1),
            ]),
            _make_department("Department of Education", BudgetCategoryType.EDUCATION, [
                ("K-12 Education Grants", 76.4),
                ("Pell Grants", 26.7),
                ("Student Loans Administration", 24.0),
                ("Special Education", 14.3),
            ]),
            _make_department("Department of Veterans Affairs", BudgetCategoryType.VETERANS_AFFAIRS, [
                ("VA Healthcare", 93.1),
                ("Disability Compensation", 115.0),
                ("Education Benefits (GI Bill)", 12.9),
                ("VA Housing Programs", 3.5),
            ]),
            _make_department("Department of Transportation", BudgetCategoryType.INFRASTRUCTURE, [
                ("Federal Highway Administration", 52.0),
                ("Federal Aviation Administration", 17.9),
                ("Federal Transit Administration", 17.5),
                ("Federal Railroad Administration", 3.1),
            ]),
            _make_department("Department of Energy", BudgetCategoryType.ENERGY, [
                ("National Nuclear Security Admin", 20.5),
                ("Energy Programs", 22.1),
                ("Environmental Cleanup", 7.3),
            ]),
            _make_department("NASA & Science", BudgetCategoryType.SCIENCE_TECHNOLOGY, [
                ("NASA", 23.3),
                ("National Science Foundation", 8.5),
            ]),
            _make_department("Department of Agriculture", BudgetCategoryType.AGRICULTURE, [
                ("SNAP (Food Stamps)", 114.0),
                ("Farm Subsidies", 26.3),
                ("Forest Service", 8.1),
            ]),
            _make_department("Department of Justice", BudgetCategoryType.JUSTICE, [
                ("FBI", 10.0),
                ("Federal Bureau of Prisons", 8.2),
                ("DEA", 3.2),
                ("ATF", 1.5),
            ]),
            _make_department("State Department & USAID", BudgetCategoryType.INTERNATIONAL_AFFAIRS, [
                ("Diplomatic Programs", 15.8),
                ("Foreign Aid (USAID)", 33.8),
                ("International Organizations", 4.5),
            ]),
            _make_department("Interest on Federal Debt", BudgetCategoryType.INTEREST_ON_DEBT, [
                ("Net Interest", 352.0),
            ]),
        ],
    )


def _build_fy2022() -> Budget:
    """FY2022 — post-pandemic normalization begins."""
    return Budget(
        fiscal_year=2022,
        gdp=_US_GDP[2022],
        population=_US_POP[2022],
        departments=[
            _make_department("Department of Defense", BudgetCategoryType.DEFENSE, [
                ("Military Personnel", 163.6),
                ("Operations & Maintenance", 299.7),
                ("Procurement", 144.8),
                ("Research & Development", 112.6),
                ("Military Construction", 14.1),
            ]),
            _make_department("Social Security Administration", BudgetCategoryType.SOCIAL_SECURITY, [
                ("Old-Age & Survivors Insurance", 968.0),
                ("Disability Insurance", 152.0),
                ("Supplemental Security Income", 61.0),
            ]),
            _make_department("Department of Health & Human Services", BudgetCategoryType.HEALTHCARE, [
                ("Medicare", 847.0),
                ("Medicaid", 592.0),
                ("Children's Health Insurance", 18.4),
                ("NIH", 46.1),
                ("CDC", 18.4),
                ("FDA", 6.5),
            ]),
            _make_department("Department of Education", BudgetCategoryType.EDUCATION, [
                ("K-12 Education Grants", 86.2),
                ("Pell Grants", 26.4),
                ("Student Loans Administration", 22.0),
                ("Special Education", 14.6),
            ]),
            _make_department("Department of Veterans Affairs", BudgetCategoryType.VETERANS_AFFAIRS, [
                ("VA Healthcare", 100.5),
                ("Disability Compensation", 128.0),
                ("Education Benefits (GI Bill)", 12.1),
                ("VA Housing Programs", 3.8),
            ]),
            _make_department("Department of Transportation", BudgetCategoryType.INFRASTRUCTURE, [
                ("Federal Highway Administration", 56.5),
                ("Federal Aviation Administration", 18.4),
                ("Federal Transit Administration", 19.6),
                ("Federal Railroad Administration", 4.0),
            ]),
            _make_department("Department of Energy", BudgetCategoryType.ENERGY, [
                ("National Nuclear Security Admin", 21.4),
                ("Energy Programs", 28.5),
                ("Environmental Cleanup", 7.8),
            ]),
            _make_department("NASA & Science", BudgetCategoryType.SCIENCE_TECHNOLOGY, [
                ("NASA", 24.0),
                ("National Science Foundation", 8.8),
            ]),
            _make_department("Department of Agriculture", BudgetCategoryType.AGRICULTURE, [
                ("SNAP (Food Stamps)", 119.4),
                ("Farm Subsidies", 22.5),
                ("Forest Service", 9.6),
            ]),
            _make_department("Department of Justice", BudgetCategoryType.JUSTICE, [
                ("FBI", 10.6),
                ("Federal Bureau of Prisons", 8.4),
                ("DEA", 3.3),
                ("ATF", 1.6),
            ]),
            _make_department("State Department & USAID", BudgetCategoryType.INTERNATIONAL_AFFAIRS, [
                ("Diplomatic Programs", 16.4),
                ("Foreign Aid (USAID)", 38.6),
                ("International Organizations", 4.8),
            ]),
            _make_department("Interest on Federal Debt", BudgetCategoryType.INTEREST_ON_DEBT, [
                ("Net Interest", 475.0),
            ]),
        ],
    )


def _build_fy2023() -> Budget:
    """FY2023 — rising interest costs."""
    return Budget(
        fiscal_year=2023,
        gdp=_US_GDP[2023],
        population=_US_POP[2023],
        departments=[
            _make_department("Department of Defense", BudgetCategoryType.DEFENSE, [
                ("Military Personnel", 167.3),
                ("Operations & Maintenance", 310.2),
                ("Procurement", 151.3),
                ("Research & Development", 120.3),
                ("Military Construction", 16.5),
            ]),
            _make_department("Social Security Administration", BudgetCategoryType.SOCIAL_SECURITY, [
                ("Old-Age & Survivors Insurance", 1_066.0),
                ("Disability Insurance", 155.0),
                ("Supplemental Security Income", 63.0),
            ]),
            _make_department("Department of Health & Human Services", BudgetCategoryType.HEALTHCARE, [
                ("Medicare", 1_022.0),
                ("Medicaid", 616.0),
                ("Children's Health Insurance", 19.1),
                ("NIH", 47.5),
                ("CDC", 17.8),
                ("FDA", 6.8),
            ]),
            _make_department("Department of Education", BudgetCategoryType.EDUCATION, [
                ("K-12 Education Grants", 79.8),
                ("Pell Grants", 26.6),
                ("Student Loans Administration", 58.0),
                ("Special Education", 14.9),
            ]),
            _make_department("Department of Veterans Affairs", BudgetCategoryType.VETERANS_AFFAIRS, [
                ("VA Healthcare", 112.0),
                ("Disability Compensation", 145.0),
                ("Education Benefits (GI Bill)", 12.8),
                ("VA Housing Programs", 4.1),
            ]),
            _make_department("Department of Transportation", BudgetCategoryType.INFRASTRUCTURE, [
                ("Federal Highway Administration", 63.4),
                ("Federal Aviation Administration", 19.4),
                ("Federal Transit Administration", 21.8),
                ("Federal Railroad Administration", 6.0),
            ]),
            _make_department("Department of Energy", BudgetCategoryType.ENERGY, [
                ("National Nuclear Security Admin", 22.2),
                ("Energy Programs", 32.1),
                ("Environmental Cleanup", 8.2),
            ]),
            _make_department("NASA & Science", BudgetCategoryType.SCIENCE_TECHNOLOGY, [
                ("NASA", 25.4),
                ("National Science Foundation", 9.5),
            ]),
            _make_department("Department of Agriculture", BudgetCategoryType.AGRICULTURE, [
                ("SNAP (Food Stamps)", 112.8),
                ("Farm Subsidies", 30.5),
                ("Forest Service", 10.4),
            ]),
            _make_department("Department of Justice", BudgetCategoryType.JUSTICE, [
                ("FBI", 11.0),
                ("Federal Bureau of Prisons", 8.8),
                ("DEA", 3.4),
                ("ATF", 1.7),
            ]),
            _make_department("State Department & USAID", BudgetCategoryType.INTERNATIONAL_AFFAIRS, [
                ("Diplomatic Programs", 16.9),
                ("Foreign Aid (USAID)", 41.2),
                ("International Organizations", 5.1),
            ]),
            _make_department("Interest on Federal Debt", BudgetCategoryType.INTEREST_ON_DEBT, [
                ("Net Interest", 659.0),
            ]),
        ],
    )


def _build_fy2024() -> Budget:
    """FY2024 — continued growth in entitlements and interest."""
    return Budget(
        fiscal_year=2024,
        gdp=_US_GDP[2024],
        population=_US_POP[2024],
        departments=[
            _make_department("Department of Defense", BudgetCategoryType.DEFENSE, [
                ("Military Personnel", 172.4),
                ("Operations & Maintenance", 318.5),
                ("Procurement", 157.6),
                ("Research & Development", 127.4),
                ("Military Construction", 17.8),
            ]),
            _make_department("Social Security Administration", BudgetCategoryType.SOCIAL_SECURITY, [
                ("Old-Age & Survivors Insurance", 1_148.0),
                ("Disability Insurance", 158.0),
                ("Supplemental Security Income", 65.0),
            ]),
            _make_department("Department of Health & Human Services", BudgetCategoryType.HEALTHCARE, [
                ("Medicare", 1_101.0),
                ("Medicaid", 618.0),
                ("Children's Health Insurance", 19.6),
                ("NIH", 48.3),
                ("CDC", 17.1),
                ("FDA", 7.1),
            ]),
            _make_department("Department of Education", BudgetCategoryType.EDUCATION, [
                ("K-12 Education Grants", 73.0),
                ("Pell Grants", 27.1),
                ("Student Loans Administration", 29.0),
                ("Special Education", 15.3),
            ]),
            _make_department("Department of Veterans Affairs", BudgetCategoryType.VETERANS_AFFAIRS, [
                ("VA Healthcare", 121.4),
                ("Disability Compensation", 160.0),
                ("Education Benefits (GI Bill)", 13.2),
                ("VA Housing Programs", 4.4),
            ]),
            _make_department("Department of Transportation", BudgetCategoryType.INFRASTRUCTURE, [
                ("Federal Highway Administration", 67.8),
                ("Federal Aviation Administration", 20.2),
                ("Federal Transit Administration", 23.4),
                ("Federal Railroad Administration", 7.8),
            ]),
            _make_department("Department of Energy", BudgetCategoryType.ENERGY, [
                ("National Nuclear Security Admin", 23.1),
                ("Energy Programs", 35.4),
                ("Environmental Cleanup", 8.7),
            ]),
            _make_department("NASA & Science", BudgetCategoryType.SCIENCE_TECHNOLOGY, [
                ("NASA", 25.0),
                ("National Science Foundation", 9.9),
            ]),
            _make_department("Department of Agriculture", BudgetCategoryType.AGRICULTURE, [
                ("SNAP (Food Stamps)", 105.2),
                ("Farm Subsidies", 28.4),
                ("Forest Service", 10.9),
            ]),
            _make_department("Department of Justice", BudgetCategoryType.JUSTICE, [
                ("FBI", 11.4),
                ("Federal Bureau of Prisons", 9.1),
                ("DEA", 3.5),
                ("ATF", 1.8),
            ]),
            _make_department("State Department & USAID", BudgetCategoryType.INTERNATIONAL_AFFAIRS, [
                ("Diplomatic Programs", 17.4),
                ("Foreign Aid (USAID)", 38.5),
                ("International Organizations", 5.3),
            ]),
            _make_department("Interest on Federal Debt", BudgetCategoryType.INTEREST_ON_DEBT, [
                ("Net Interest", 882.0),
            ]),
        ],
    )


# ── Public API ───────────────────────────────────────────────────────────

BUILDERS: dict[int, callable] = {  # type: ignore[type-arg]
    2020: _build_fy2020,
    2021: _build_fy2021,
    2022: _build_fy2022,
    2023: _build_fy2023,
    2024: _build_fy2024,
}

AVAILABLE_YEARS = sorted(BUILDERS.keys())


def get_us_budget(year: int) -> Budget:
    """Return a sample US federal budget for the given fiscal year."""
    if year not in BUILDERS:
        raise ValueError(
            f"No data for FY{year}. Available: {AVAILABLE_YEARS}"
        )
    return BUILDERS[year]()


def get_all_us_budgets() -> dict[int, Budget]:
    """Return all available US budget years."""
    return {yr: BUILDERS[yr]() for yr in AVAILABLE_YEARS}
