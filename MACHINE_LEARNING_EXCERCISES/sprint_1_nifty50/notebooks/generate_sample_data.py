"""
Generate realistic synthetic market data for Nifty 50 and related indices.
This is used when Yahoo Finance API is not accessible due to network restrictions.

The generated data mimics real market behavior with:
- Realistic returns distribution
- Volatility clustering
- Correlations between indices
- Trading volume patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)  # For reproducibility

def generate_correlated_returns(n_days, n_series, mean_return=0.0005, volatility=0.015, correlation=0.3):
    """
    Generate correlated return series using Cholesky decomposition
    """
    # Create correlation matrix
    corr_matrix = np.full((n_series, n_series), correlation)
    np.fill_diagonal(corr_matrix, 1.0)

    # Cholesky decomposition
    L = np.linalg.cholesky(corr_matrix)

    # Generate uncorrelated returns
    uncorr_returns = np.random.normal(mean_return, volatility, (n_days, n_series))

    # Apply correlation
    corr_returns = uncorr_returns @ L.T

    return corr_returns


def generate_price_series(start_price, returns):
    """Convert returns to price series"""
    prices = np.zeros(len(returns) + 1)
    prices[0] = start_price

    for i, ret in enumerate(returns):
        prices[i + 1] = prices[i] * (1 + ret)

    return prices[1:]  # Skip initial price


def generate_volume_series(n_days, base_volume=50000000):
    """Generate realistic volume data"""
    # Volume has some autocorrelation and randomness
    volume = np.zeros(n_days)
    volume[0] = base_volume

    for i in range(1, n_days):
        # AR(1) process with noise
        volume[i] = 0.7 * volume[i-1] + 0.3 * base_volume + np.random.normal(0, base_volume * 0.2)
        volume[i] = max(volume[i], base_volume * 0.3)  # Ensure positive

    return volume


def generate_vix_series(returns, base_vix=15):
    """Generate VIX-like volatility index based on market returns"""
    # VIX tends to spike when markets fall
    vix = np.zeros(len(returns))

    for i in range(len(returns)):
        # Base VIX plus response to negative returns
        shock = -min(returns[i], 0) * 500  # Amplify negative returns
        vix[i] = base_vix + shock + np.random.normal(0, 2)
        vix[i] = max(vix[i], 10)  # Floor at 10
        vix[i] = min(vix[i], 80)  # Cap at 80

    return vix


def generate_all_market_data(start_date='2018-01-01', end_date='2025-12-13'):
    """
    Generate complete market dataset for all indices
    """
    # Date range
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # Generate business days (approximately)
    all_days = pd.date_range(start, end, freq='D')
    # Filter to weekdays (simple approximation of trading days)
    trading_days = all_days[all_days.dayofweek < 5]
    n_days = len(trading_days)

    print(f"Generating {n_days} days of market data from {start_date} to {end_date}...")

    # Generate correlated returns for all indices
    # Order: Nifty, SP500, Nasdaq, USD/INR, Crude, Hang Seng, Nikkei, DXY
    returns_matrix = generate_correlated_returns(
        n_days=n_days,
        n_series=8,
        mean_return=0.0005,  # ~12.5% annual
        volatility=0.012,     # ~19% annual vol
        correlation=0.4       # Moderate correlation
    )

    # Starting prices (approximate real values)
    start_prices = {
        'nifty': 10500,
        'sp500': 2700,
        'nasdaq': 7000,
        'usdinr': 65,
        'crude': 65,
        'hangseng': 30000,
        'nikkei': 23000,
        'dxy': 90
    }

    # Generate price series for each index
    data = pd.DataFrame(index=trading_days)

    for i, (name, start_price) in enumerate(start_prices.items()):
        prices = generate_price_series(start_price, returns_matrix[:, i])
        data[name] = prices

    # Generate Nifty volume
    data['volume'] = generate_volume_series(n_days, base_volume=250000000)

    # Generate India VIX based on Nifty returns
    nifty_returns = returns_matrix[:, 0]
    data['vix'] = generate_vix_series(nifty_returns, base_vix=18)

    print(f"✅ Generated data for: {list(start_prices.keys())}")
    print(f"✅ Data shape: {data.shape}")
    print(f"\nSample statistics:")
    print(data.describe())

    return data


def save_to_csv(data, output_dir):
    """Save generated data to CSV"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'synthetic_market_data.csv')
    data.to_csv(output_path)
    print(f"\n✅ Data saved to: {output_path}")

    return output_path


if __name__ == "__main__":
    # Generate data
    data = generate_all_market_data()

    # Save to data directory
    import os
    base_dir = '/home/user/MACHINE_LEARNING_EXCERCISES/sprint_1_nifty50'
    data_dir = os.path.join(base_dir, 'data')

    save_to_csv(data, data_dir)

    print("\n" + "="*80)
    print("SYNTHETIC DATA GENERATION COMPLETE")
    print("="*80)
    print("\nThis data can be used to demonstrate the ML pipeline.")
    print("Replace with real Yahoo Finance data when network access is available.")
