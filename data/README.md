# Data

## `raw/` — original files, never edited by hand
Downloaded from Indra Group investor relations (https://www.indragroup.com/en/investor-relations). Spanish versions prevail legally; English versions are used here.

| File | Content | Source URL | Downloaded |
|---|---|---|---|
| `pg_bs_cf_fy19_eng_web-envio.xls` | FY2019 P&L, balance sheet, cash flow | https://www.indragroup.com/cms-content/2025/08/pg_bs_cf_fy19_eng_web-envio.xls | |
| `pg_bs_cf_fy20_eng_web-envio.xls` | FY2020 P&L, BS, CF | https://www.indragroup.com/cms-content/2025/08/pg_bs_cf_fy20_eng_web-envio.xls | |
| `pg_bs_cf_fy21_eng_web.xls` | FY2021 P&L, BS, CF | https://www.indragroup.com/cms-content/2025/08/pg_bs_cf_fy21_eng_web.xls | |
| `pg_bs_cf_fy23_eng.xls` | FY2023 P&L, BS, CF (incl. 2022 comparatives) | https://www.indragroup.com/cms-content/2025/08/pg_bs_cf_fy23_eng.xls | |
| `pg_bs_cf_2024_eng.xls` | FY2024 P&L, BS, CF | https://www.indragroup.com/cms-content/2025/08/pg_bs_cf_2024_eng.xls | |
| `PG_BS_CF_2025_eng.xls` | FY2025 P&L, BS, CF | https://www.indragroup.com/cms-content/2026/02/PG_BS_CF_2025_eng.xls | |
| `PG_BS_CF_9M26_eng.xls` | 9M2026 P&L, BS, CF | https://www.indragroup.com/cms-content/2025/07/PG_BS_CF_9M26_eng.xls | |
| `Rdos-9M26_eng.pdf` | 9M2026 quarterly report (segments, backlog, order intake, guidance) | https://www.indragroup.com/cms-content/2025/07/Rdos-9M26_eng.pdf | |
| `Memoria-Consolidado-2025_EN-2026-04-27-17-24.pdf` | Audited consolidated annual accounts 2025 (notes: leases, minorities, segments) | https://www.indragroup.com/cms-content/2026/04/Memoria-Consolidado-2025_EN-2026-04-27-17-24.pdf | |

Note: the FY2022 "Excel" link on the IR page points to a PDF, so FY2022 figures are taken from the FY2023 file (prior-year comparatives).
When a later report restates a prior year, the most recent version is used.

## `processed/` — clean, tidy CSVs read by the model
Long format: `year | metric | value | unit | source`. Every value must be traceable to a file (and sheet/page) in `raw/`.
