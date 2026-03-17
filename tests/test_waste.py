"""Tests for WasteDetector."""

import pytest

from budgetmap.analyzer.waste import WasteDetector, SpendingAnomaly
from budgetmap.data.us_budget import get_all_us_budgets, get_us_budget
from budgetmap.models import Budget, BudgetCategoryType, Department, LineItem


class TestWasteDetector:
    @pytest.fixture
    def detector(self):
        return WasteDetector(get_all_us_budgets())

    def test_detect_all_returns_list(self, detector):
        anomalies = detector.detect_all()
        assert isinstance(anomalies, list)
        assert all(isinstance(a, SpendingAnomaly) for a in anomalies)

    def test_detect_spending_spikes(self, detector):
        spikes = detector.detect_spending_spikes()
        assert isinstance(spikes, list)

    def test_detect_category_outliers(self, detector):
        outliers = detector.detect_category_outliers()
        assert isinstance(outliers, list)

    def test_detect_disproportionate_items(self, detector):
        items = detector.detect_disproportionate_items()
        assert isinstance(items, list)

    def test_anomaly_fields(self, detector):
        anomalies = detector.detect_all()
        if anomalies:
            a = anomalies[0]
            assert a.department
            assert a.description
            assert a.severity in ("low", "medium", "high")

    def test_spike_detection_with_artificial_data(self):
        """Create budgets with an obvious spike to verify detection."""
        b1 = Budget(
            fiscal_year=2020,
            departments=[
                Department(
                    name="TestDept",
                    category=BudgetCategoryType.OTHER,
                    line_items=[LineItem(name="Item", amount=100.0, category="TestDept")],
                )
            ],
        )
        b2 = Budget(
            fiscal_year=2021,
            departments=[
                Department(
                    name="TestDept",
                    category=BudgetCategoryType.OTHER,
                    line_items=[LineItem(name="Item", amount=300.0, category="TestDept")],
                )
            ],
        )
        detector = WasteDetector([b1, b2], spike_threshold=50.0)
        spikes = detector.detect_spending_spikes()
        assert len(spikes) >= 1
        assert any("TestDept" in s.department for s in spikes)

    def test_disproportionate_item_detection(self):
        """A single item that is >80% of its department should be flagged."""
        budget = Budget(
            fiscal_year=2024,
            departments=[
                Department(
                    name="BigDept",
                    category=BudgetCategoryType.OTHER,
                    line_items=[
                        LineItem(name="DominantItem", amount=900.0, category="BigDept"),
                        LineItem(name="SmallItem", amount=10.0, category="BigDept"),
                    ],
                )
            ],
        )
        detector = WasteDetector([budget])
        items = detector.detect_disproportionate_items()
        assert len(items) >= 1
        assert any("DominantItem" in i.item_name for i in items if i.item_name)
