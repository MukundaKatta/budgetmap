"""Tests for Budgetmap."""
from src.core import Budgetmap
def test_init(): assert Budgetmap().get_stats()["ops"] == 0
def test_op(): c = Budgetmap(); c.process(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Budgetmap(); [c.process() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Budgetmap(); c.process(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Budgetmap(); r = c.process(); assert r["service"] == "budgetmap"
