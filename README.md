# Stochastic DCF — IBEX 35

> 🚧 Work in progress

A discounted cash flow (DCF) valuation of an IBEX 35 company, extended with a **stochastic layer**: value drivers are modelled as dependent random variables and propagated through Monte Carlo simulation, producing a **distribution** of the intrinsic value per share instead of a single price target.

## Problem
A classic DCF outputs one number, but its inputs (revenue growth, margins, capex, WACC, terminal growth) are uncertain, and the value is highly non-linear in them (e.g. the terminal value near $WACC = g$). This project quantifies that uncertainty.

## Methodology (planned)
1. **Deterministic DCF** — FCFF, CAPM/WACC, terminal value, bridge from enterprise value to equity value.
2. **Stochastic layer** — driver distributions calibrated on historical and consensus data, dependence via a Gaussian copula, mean-reverting margins, Monte Carlo with convergence diagnostics.
3. **Analysis** — global sensitivity (Sobol indices), reverse DCF (market-implied expectations), trading comparables.
4. **Stock pitch** — investment thesis, valuation distribution, risks and catalysts.

## Results
_Coming soon._

## Project structure
```
├── data/
│   ├── raw/          # original data (annual reports, market data)
│   └── processed/    # cleaned data ready for the model
├── notebooks/        # exploration and narrative
├── reports/figures/  # final charts and pitch material
├── src/              # model code (functions/classes)
├── tests/            # unit tests (pytest)
├── requirements.txt
└── LICENSE
```

## How to run
```bash
git clone https://github.com/AsierLoz13/ibex-stochastic-dcf.git
cd ibex-stochastic-dcf
python -m venv .venv
source .venv/bin/activate        # Windows (Git Bash): source .venv/Scripts/activate
pip install -r requirements.txt
```

## Author
Asier Lozano Nebreda — Mathematical Engineering, Universidad Francisco de Vitoria (Madrid).

## License
MIT
