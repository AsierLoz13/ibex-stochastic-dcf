"""Load Indra's reported financial statements from the investor-relations Excel files.

Indra publishes one Excel file per period (``PG_BS_CF_<period>``) with the P&L,
balance sheet and cash-flow statement. Each file only contains its own period,
labels change slightly across years, and the sign convention for net debt was
flipped in 2024. This module turns those files into one tidy table and a clean
table of key metrics with consistent names and signs.
"""
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

# Period label -> file name in data/raw. FY2022 has no Excel file (see data/README.md).
FILES = {
    "2019": "pg_bs_cf_fy19_eng_web-envio.xls",
    "2020": "pg_bs_cf_fy20_eng_web-envio.xls",
    "2021": "pg_bs_cf_fy21_eng_web.xls",
    "2023": "pg_bs_cf_fy23_eng.xls",
    "2024": "pg_bs_cf_2024_eng.xls",
    "2025": "PG_BS_CF_2025_eng.xls",
    "9M2026": "PG_BS_CF_9M26_eng.xls",
}

# Statement code -> sheet name (note the leading space in " P&L").
SHEETS = {"PL": " P&L", "BS": "BS", "CF": "Cash Flow"}

# Canonical metric name -> (statement, list of labels Indra has used for it over the years).
METRIC_MAP = {
    "revenue": ("PL", ["Revenue"]),
    "ebitda": ("PL", ["Gross Operating Profit (EBITDA)", "Gross Operating Result (EBITDA)"]),
    "d_and_a": ("PL", ["Depreciation and amortisation charge"]),
    "ebit": ("PL", ["Profit (Loss) from operations (EBIT)", "Operating Result (EBIT)"]),
    "profit_before_tax": ("PL", ["Profit (Loss) before tax"]),
    "income_tax": ("PL", ["Income tax"]),
    "minorities_profit": ("PL", ["Profit (Loss) attributable to non-controlling interests"]),
    "net_profit": ("PL", ["Profit (Loss) attributable to the Parent"]),
    "change_receivables": ("CF", ["Changes in trade receivables and other items"]),
    "change_inventories": ("CF", ["Changes in inventories"]),
    "change_payables": ("CF", ["Changes in trade payables and other items"]),
    "capex": ("CF", ["Capex"]),
    "interest_paid": ("CF", ["Interest paid and received"]),
    "income_tax_paid": ("CF", ["Income tax paid"]),
    "fcf_reported": ("CF", ["Free Cash Flow"]),
    "net_debt": ("CF", ["Final Net Debt"]),
    "cash": ("BS", ["Cash and cash equivalents"]),
    "gross_financial_debt": ("BS", ["Gross financial debt"]),
    "minorities_bs": ("BS", ["Non-controlling interests"]),
    "equity_parent": ("BS", ["Equity attributable to parent company"]),
}

# Until FY2023 Indra reported net debt and gross debt as negative numbers;
# from FY2024 onwards they are positive ("Net Debt (+) / Net Cash (-)").
# We use the modern convention everywhere: positive = debt.
SIGN_FLIP_METRICS = ["net_debt", "gross_financial_debt"]
SIGN_FLIP_PERIODS = ["2019", "2020", "2021", "2023"]


def read_statement(path, sheet):
    """Read one sheet and return a two-column table: line_item, value.

    The label column is the first column that contains text; the value for the
    period sits in the column immediately to its right.
    """
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    has_text = raw.map(lambda cell: isinstance(cell, str))
    label_col = has_text.any().idxmax()

    table = raw[[label_col, label_col + 1]].copy()
    table.columns = ["line_item", "value"]
    table["value"] = pd.to_numeric(table["value"], errors="coerce")
    table = table.dropna()
    table["line_item"] = table["line_item"].str.strip()
    return table


def load_long(raw_dir=RAW_DIR):
    """All line items of all periods in tidy (long) format."""
    pieces = []
    for period, file_name in FILES.items():
        for statement, sheet in SHEETS.items():
            table = read_statement(Path(raw_dir) / file_name, sheet)
            table["period"] = period
            table["statement"] = statement
            table["source"] = file_name
            pieces.append(table)
    long = pd.concat(pieces, ignore_index=True)
    long["unit"] = "EUR m"
    return long[["period", "statement", "line_item", "value", "unit", "source"]]


def key_metrics(long):
    """Wide table (one row per period) of canonical metrics with consistent signs."""
    rows = []
    for metric, (statement, labels) in METRIC_MAP.items():
        match = long[(long["statement"] == statement) & (long["line_item"].isin(labels))]
        match = match.drop_duplicates(subset="period", keep="first")
        rows.append(match.assign(metric=metric)[["period", "metric", "value"]])
    tidy = pd.concat(rows, ignore_index=True)

    flip = tidy["metric"].isin(SIGN_FLIP_METRICS) & tidy["period"].isin(SIGN_FLIP_PERIODS)
    tidy.loc[flip, "value"] = -tidy.loc[flip, "value"]

    wide = tidy.pivot(index="period", columns="metric", values="value")
    wide = wide.reindex(index=list(FILES), columns=list(METRIC_MAP))
    wide["is_full_year"] = ~wide.index.str.startswith("9M")
    return wide
