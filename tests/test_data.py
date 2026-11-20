"""Sanity checks on the loaded financial data (run with: pytest)."""
import numpy as np
import pytest

from src.data import key_metrics, load_long


@pytest.fixture(scope="module")
def metrics():
    return key_metrics(load_long())


def test_no_missing_core_metrics(metrics):
    core = ["revenue", "ebitda", "d_and_a", "ebit", "capex", "fcf_reported", "net_debt"]
    assert not metrics[core].isna().any().any()


def test_ebitda_minus_da_equals_ebit(metrics):
    # D&A is reported as a negative number in the P&L.
    np.testing.assert_allclose(metrics["ebitda"] + metrics["d_and_a"], metrics["ebit"], atol=1.0)


def test_net_debt_matches_published_fy2025(metrics):
    # Indra's FY2025 press release: net debt of EUR 583m (net cash of EUR 86m in 2024).
    assert metrics.loc["2025", "net_debt"] == pytest.approx(583, abs=1)
    assert metrics.loc["2024", "net_debt"] == pytest.approx(-86, abs=1)
