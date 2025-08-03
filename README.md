# Bond Portfolio Optimization & Immunization Dashboard

An interactive Streamlit dashboard for bond portfolio analysis, risk management, and immunization strategies.

## Features

- **Data Explorer**: View key rates, asset returns, durations, and convexity data
- **Analytics & Risk**: Analyze volatility, correlations, and risk-return profiles
- **Charts & Visualization**: Interactive charts for portfolio performance analysis
- **Export Capabilities**: Download filtered datasets for further analysis

## Deployment

This app is configured for deployment on Streamlit Cloud. The following files are required:

- `app.py` - Main application file
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration
- `packages.txt` - System dependencies (if needed)
- Excel data files: `KeyRates.xlsx`, `Assets.xlsx`, `durations.xlsx`, `convexity.xlsx`

## Local Development

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Requirements

The app expects the following Excel files in the root directory:
- `KeyRates.xlsx` - Key rate data
- `Assets.xlsx` - Asset price data  
- `durations.xlsx` - Duration data
- `convexity.xlsx` - Convexity data

## Author

MD Amir Khan | MS Financial Engineering | August 2025 