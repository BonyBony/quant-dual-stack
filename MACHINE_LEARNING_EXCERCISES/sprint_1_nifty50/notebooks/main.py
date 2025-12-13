"""
Nifty 50 Short-Term Trading Model
Machine Learning based prediction of 5-day forward returns

Author: ML Trading Exercises
Date: 2025-12-13
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import logging
import warnings
import pickle
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV, ElasticNetCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Suppress warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

# Paths
BASE_DIR = '/home/user/MACHINE_LEARNING_EXCERCISES/sprint_1_nifty50'
DATA_DIR = os.path.join(BASE_DIR, 'data')
FEATURES_DIR = os.path.join(BASE_DIR, 'features')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')

# Create directories if they don't exist
for directory in [DATA_DIR, FEATURES_DIR, MODELS_DIR, OUTPUTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Trading Parameters
INITIAL_CAPITAL = 100000  # ₹1,00,000
TRANSACTION_COST = 0.15   # 0.15% per trade
HOLDING_PERIOD = 5        # 5 days

# Date Ranges
DATA_START = '2018-01-01'  # Extra data for feature calculation
DATA_END = '2025-12-13'

TRAIN_START = '2019-01-01'
TRAIN_END = '2021-12-31'

VAL_START = '2022-01-01'
VAL_END = '2022-12-31'

TEST_START = '2023-01-01'
TEST_END = '2025-12-13'

# Tickers
TICKERS = {
    'nifty': '^NSEI',       # Nifty 50
    'vix': '^INDIAVIX',     # India VIX
    'sp500': '^GSPC',       # S&P 500
    'nasdaq': '^IXIC',      # Nasdaq
    'usdinr': 'INR=X',      # USD/INR
    'crude': 'BZ=F',        # Brent Crude
    'hangseng': '^HSI',     # Hang Seng
    'nikkei': '^N225',      # Nikkei 225
    'dxy': 'DX-Y.NYB'       # US Dollar Index
}

# =============================================================================
# LOGGING SETUP
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(OUTPUTS_DIR, 'execution.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# DATA COLLECTION
# =============================================================================

def download_ticker_data(ticker, name, start_date, end_date):
    """Download data for a single ticker with error handling"""
    try:
        logger.info(f"Downloading {name} ({ticker})...")
        # Disable curl_cffi to avoid proxy issues
        import os
        os.environ['YF_USE_CURL'] = '0'
        data = yf.download(ticker, start=start_date, end=end_date, progress=False, proxy=None)

        if data.empty:
            logger.warning(f"  ⚠️  No data returned for {name}")
            return None

        # Use Adj Close if available, else Close
        if 'Adj Close' in data.columns:
            price_data = data[['Adj Close']].copy()
            price_data.columns = [name]
        else:
            price_data = data[['Close']].copy()
            price_data.columns = [name]

        # Also get volume if available
        volume_data = None
        if 'Volume' in data.columns and name == 'nifty':
            volume_data = data[['Volume']].copy()
            volume_data.columns = ['volume']

        logger.info(f"  ✅ {name}: {len(price_data)} rows downloaded")
        return price_data, volume_data

    except Exception as e:
        logger.error(f"  ❌ Failed to download {name}: {str(e)}")
        return None, None


def load_synthetic_data():
    """Load or generate synthetic data as fallback"""
    logger.warning("\n⚠️  Yahoo Finance not accessible - using synthetic data")
    logger.info("   This demonstrates the full ML pipeline with realistic synthetic data")
    logger.info("   Replace with real data when network access is available\n")

    synthetic_path = os.path.join(DATA_DIR, 'synthetic_market_data.csv')

    # Generate if doesn't exist
    if not os.path.exists(synthetic_path):
        logger.info("Generating synthetic market data...")
        from generate_sample_data import generate_all_market_data, save_to_csv
        data = generate_all_market_data(DATA_START, DATA_END)
        save_to_csv(data, DATA_DIR)
    else:
        logger.info(f"Loading existing synthetic data from {synthetic_path}")
        data = pd.read_csv(synthetic_path, index_col=0, parse_dates=True)

    # Split into individual dataframes to match expected format
    all_data = {}
    for col in ['nifty', 'vix', 'sp500', 'nasdaq', 'usdinr', 'crude', 'hangseng', 'nikkei', 'dxy']:
        if col in data.columns:
            all_data[col] = pd.DataFrame(data[col])
            all_data[col].columns = [col]

    volume_data = pd.DataFrame(data['volume']) if 'volume' in data.columns else None
    if volume_data is not None:
        volume_data.columns = ['volume']

    logger.info(f"✅ Loaded synthetic data: {list(all_data.keys())}")

    return all_data, volume_data


def collect_all_data():
    """Collect data from all sources"""
    logger.info("="*80)
    logger.info("STARTING DATA COLLECTION")
    logger.info("="*80)

    all_data = {}
    volume_data = None

    # Try Yahoo Finance first
    use_synthetic = False

    for key, ticker in TICKERS.items():
        result = download_ticker_data(ticker, key, DATA_START, DATA_END)

        if result is not None:
            price_data, vol_data = result
            if price_data is not None:
                all_data[key] = price_data
            if vol_data is not None:
                volume_data = vol_data

        # If Nifty 50 failed, use synthetic data
        if key == 'nifty' and (result is None or result[0] is None):
            logger.warning("❌ Failed to download Nifty 50 from Yahoo Finance")
            use_synthetic = True
            break

    # Fallback to synthetic data
    if use_synthetic:
        return load_synthetic_data()

    logger.info(f"\n✅ Successfully downloaded {len(all_data)} data sources")
    logger.info(f"   Available sources: {list(all_data.keys())}")

    return all_data, volume_data


def align_and_clean_data(all_data, volume_data):
    """Align all data sources on common dates and handle missing values"""
    logger.info("\n" + "="*80)
    logger.info("ALIGNING AND CLEANING DATA")
    logger.info("="*80)

    # Start with Nifty 50 as base
    df = all_data['nifty'].copy()
    df.columns = ['close']

    # Add volume if available
    if volume_data is not None:
        df = df.join(volume_data, how='left')
        logger.info("✅ Volume data added")
    else:
        logger.warning("⚠️  No volume data available")

    # Add other data sources
    for key, data in all_data.items():
        if key != 'nifty':
            df = df.join(data, how='left')
            logger.info(f"  Joined {key}")

    logger.info(f"\nData shape before cleaning: {df.shape}")
    logger.info(f"Missing values:\n{df.isnull().sum()}")

    # Forward fill missing values (up to 5 days)
    df = df.fillna(method='ffill', limit=5)

    # Drop any remaining NaN
    df = df.dropna()

    logger.info(f"\nData shape after cleaning: {df.shape}")
    logger.info(f"Date range: {df.index[0]} to {df.index[-1]}")

    return df


# =============================================================================
# FEATURE ENGINEERING
# =============================================================================

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def engineer_features(df):
    """Create all features with proper lagging to prevent data leakage"""
    logger.info("\n" + "="*80)
    logger.info("ENGINEERING FEATURES")
    logger.info("="*80)

    features = pd.DataFrame(index=df.index)
    close = df['close']

    # 1. Returns (Momentum/Mean Reversion)
    logger.info("Calculating returns features...")
    features['returns_1d'] = (close / close.shift(1) - 1) * 100
    features['returns_5d'] = (close / close.shift(5) - 1) * 100
    features['returns_20d'] = (close / close.shift(20) - 1) * 100
    features['returns_60d'] = (close / close.shift(60) - 1) * 100

    # 2. Volatility
    logger.info("Calculating volatility features...")
    features['vol_20d'] = features['returns_1d'].rolling(20).std() * np.sqrt(252)
    features['vol_60d'] = features['returns_1d'].rolling(60).std() * np.sqrt(252)
    features['vol_ratio'] = features['vol_20d'] / features['vol_60d']

    # India VIX (if available)
    if 'vix' in df.columns:
        features['india_vix'] = df['vix']
        logger.info("  ✅ India VIX added")
    else:
        logger.warning("  ⚠️  India VIX not available, skipping")

    # 3. Technical Indicators
    logger.info("Calculating technical indicators...")
    features['rsi_14'] = calculate_rsi(close, 14)
    features['rsi_20'] = calculate_rsi(close, 20)

    # MACD
    ema_12 = close.ewm(span=12).mean()
    ema_26 = close.ewm(span=26).mean()
    macd = ema_12 - ema_26
    macd_signal = macd.ewm(span=9).mean()

    features['macd'] = macd
    features['macd_signal'] = macd_signal
    features['macd_diff'] = macd - macd_signal

    # Price vs Moving Averages
    ma_20 = close.rolling(20).mean()
    ma_50 = close.rolling(50).mean()
    ma_200 = close.rolling(200).mean()

    features['price_vs_ma20'] = (close / ma_20 - 1) * 100
    features['price_vs_ma50'] = (close / ma_50 - 1) * 100
    features['price_vs_ma200'] = (close / ma_200 - 1) * 100

    # Volume ratio (if available)
    if 'volume' in df.columns:
        features['volume_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
        logger.info("  ✅ Volume ratio added")
    else:
        logger.warning("  ⚠️  Volume not available, skipping volume_ratio")

    # 4. Global Market Features
    logger.info("Calculating global market features...")

    if 'sp500' in df.columns:
        features['sp500_ret_1d'] = (df['sp500'] / df['sp500'].shift(1) - 1) * 100

    if 'nasdaq' in df.columns:
        features['nasdaq_ret_1d'] = (df['nasdaq'] / df['nasdaq'].shift(1) - 1) * 100

    if 'usdinr' in df.columns:
        features['usdinr_change_1d'] = (df['usdinr'] / df['usdinr'].shift(1) - 1) * 100
        features['usdinr_change_5d'] = (df['usdinr'] / df['usdinr'].shift(5) - 1) * 100

    if 'crude' in df.columns:
        features['crude_change_1d'] = (df['crude'] / df['crude'].shift(1) - 1) * 100
        features['crude_change_5d'] = (df['crude'] / df['crude'].shift(5) - 1) * 100

    # Asian markets composite
    if 'hangseng' in df.columns and 'nikkei' in df.columns:
        hangseng_ret = (df['hangseng'] / df['hangseng'].shift(1) - 1) * 100
        nikkei_ret = (df['nikkei'] / df['nikkei'].shift(1) - 1) * 100
        features['asian_markets_ret'] = (hangseng_ret + nikkei_ret) / 2

    if 'dxy' in df.columns:
        features['dxy_change_1d'] = (df['dxy'] / df['dxy'].shift(1) - 1) * 100

    # 5. Time-based Features
    logger.info("Calculating time-based features...")
    features['day_of_week'] = df.index.dayofweek
    features['month'] = df.index.month
    features['is_month_end'] = (df.index.is_month_end |
                                 df.index.shift(-1, freq='D').is_month_end |
                                 df.index.shift(-2, freq='D').is_month_end).astype(int)

    # TARGET VARIABLE (Forward 5-day return)
    logger.info("Calculating target variable (forward 5-day return)...")
    features['target'] = (close.shift(-5) / close - 1) * 100

    logger.info(f"\n✅ Feature engineering complete!")
    logger.info(f"   Total features created: {len(features.columns) - 1} (+ 1 target)")
    logger.info(f"   Features: {[col for col in features.columns if col != 'target']}")

    return features


# =============================================================================
# TRAIN/VAL/TEST SPLIT
# =============================================================================

def split_data(features):
    """Split data into train/validation/test sets"""
    logger.info("\n" + "="*80)
    logger.info("SPLITTING DATA (TIME-SERIES SPLIT)")
    logger.info("="*80)

    # Drop NaN (from lagged features and forward target)
    features_clean = features.dropna()
    logger.info(f"Data after dropping NaN: {len(features_clean)} rows")

    # Split by date
    train_data = features_clean[(features_clean.index >= TRAIN_START) &
                                (features_clean.index <= TRAIN_END)]
    val_data = features_clean[(features_clean.index >= VAL_START) &
                              (features_clean.index <= VAL_END)]
    test_data = features_clean[(features_clean.index >= TEST_START) &
                               (features_clean.index <= TEST_END)]

    logger.info(f"\nTrain: {TRAIN_START} to {TRAIN_END} ({len(train_data)} rows)")
    logger.info(f"Val:   {VAL_START} to {VAL_END} ({len(val_data)} rows)")
    logger.info(f"Test:  {TEST_START} to {TEST_END} ({len(test_data)} rows)")

    # Separate features and target
    feature_columns = [col for col in features_clean.columns if col != 'target']

    X_train = train_data[feature_columns]
    y_train = train_data['target']

    X_val = val_data[feature_columns]
    y_val = val_data['target']

    X_test = test_data[feature_columns]
    y_test = test_data['target']

    logger.info(f"\n✅ Data split complete")
    logger.info(f"   Features: {len(feature_columns)}")

    return X_train, y_train, X_val, y_val, X_test, y_test, feature_columns, test_data


def scale_features(X_train, X_val, X_test):
    """Scale features using StandardScaler (fit on train only)"""
    logger.info("\n" + "="*80)
    logger.info("SCALING FEATURES")
    logger.info("="*80)

    scaler = StandardScaler()

    # Fit on training data ONLY
    X_train_scaled = scaler.fit_transform(X_train)
    logger.info("✅ Scaler fitted on training data")

    # Transform val and test using same scaler
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    logger.info("✅ Val and test data scaled")

    return X_train_scaled, X_val_scaled, X_test_scaled, scaler


# =============================================================================
# MODEL TRAINING
# =============================================================================

def train_models(X_train_scaled, y_train, X_val_scaled, y_val, X_test_scaled, y_test):
    """Train all 4 models"""
    logger.info("\n" + "="*80)
    logger.info("TRAINING MODELS")
    logger.info("="*80)

    models = {}
    predictions = {}

    # 1. Linear Regression (Baseline)
    logger.info("\n1. Training Linear Regression (Baseline)...")
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)

    predictions['Linear Regression'] = {
        'train': lr_model.predict(X_train_scaled),
        'val': lr_model.predict(X_val_scaled),
        'test': lr_model.predict(X_test_scaled)
    }
    models['Linear Regression'] = lr_model

    train_mse = mean_squared_error(y_train, predictions['Linear Regression']['train'])
    test_mse = mean_squared_error(y_test, predictions['Linear Regression']['test'])
    logger.info(f"   Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

    # 2. Lasso (L1 Regularization)
    logger.info("\n2. Training Lasso (L1 - Feature Selection)...")
    lasso_model = LassoCV(
        alphas=np.logspace(-4, 1, 100),
        cv=5,
        max_iter=10000,
        random_state=42,
        n_jobs=-1
    )
    lasso_model.fit(X_train_scaled, y_train)
    logger.info(f"   Optimal alpha: {lasso_model.alpha_:.6f}")

    predictions['Lasso'] = {
        'train': lasso_model.predict(X_train_scaled),
        'val': lasso_model.predict(X_val_scaled),
        'test': lasso_model.predict(X_test_scaled)
    }
    models['Lasso'] = lasso_model

    train_mse = mean_squared_error(y_train, predictions['Lasso']['train'])
    test_mse = mean_squared_error(y_test, predictions['Lasso']['test'])
    logger.info(f"   Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

    # 3. Ridge (L2 Regularization)
    logger.info("\n3. Training Ridge (L2 - General Shrinkage)...")
    ridge_model = RidgeCV(
        alphas=np.logspace(-4, 4, 100),
        cv=5
    )
    ridge_model.fit(X_train_scaled, y_train)
    logger.info(f"   Optimal alpha: {ridge_model.alpha_:.6f}")

    predictions['Ridge'] = {
        'train': ridge_model.predict(X_train_scaled),
        'val': ridge_model.predict(X_val_scaled),
        'test': ridge_model.predict(X_test_scaled)
    }
    models['Ridge'] = ridge_model

    train_mse = mean_squared_error(y_train, predictions['Ridge']['train'])
    test_mse = mean_squared_error(y_test, predictions['Ridge']['test'])
    logger.info(f"   Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

    # 4. Elastic Net (L1 + L2)
    logger.info("\n4. Training Elastic Net (L1 + L2)...")
    elastic_model = ElasticNetCV(
        l1_ratio=[.1, .5, .7, .9, .95, .99, 1],
        alphas=np.logspace(-4, 1, 50),
        cv=5,
        max_iter=10000,
        random_state=42,
        n_jobs=-1
    )
    elastic_model.fit(X_train_scaled, y_train)
    logger.info(f"   Optimal alpha: {elastic_model.alpha_:.6f}")
    logger.info(f"   Optimal l1_ratio: {elastic_model.l1_ratio_:.4f}")

    predictions['Elastic Net'] = {
        'train': elastic_model.predict(X_train_scaled),
        'val': elastic_model.predict(X_val_scaled),
        'test': elastic_model.predict(X_test_scaled)
    }
    models['Elastic Net'] = elastic_model

    train_mse = mean_squared_error(y_train, predictions['Elastic Net']['train'])
    test_mse = mean_squared_error(y_test, predictions['Elastic Net']['test'])
    logger.info(f"   Train MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")

    logger.info("\n✅ All models trained successfully!")

    return models, predictions


def save_models(models, scaler):
    """Save all trained models"""
    logger.info("\n" + "="*80)
    logger.info("SAVING MODELS")
    logger.info("="*80)

    # Save scaler
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    logger.info(f"✅ Scaler saved to {scaler_path}")

    # Save each model
    for model_name, model in models.items():
        filename = model_name.lower().replace(' ', '_') + '.pkl'
        model_path = os.path.join(MODELS_DIR, filename)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"✅ {model_name} saved to {model_path}")


# =============================================================================
# BACKTESTING
# =============================================================================

def generate_signals(predictions):
    """Convert predictions to trading signals (1=long, 0=no position)"""
    return np.where(predictions > 0, 1, 0)


def calculate_strategy_returns(actual_returns, signals, transaction_cost=TRANSACTION_COST):
    """Calculate strategy returns including transaction costs"""
    strategy_returns = []
    previous_signal = 0
    trades = 0

    for i in range(len(signals)):
        current_signal = signals[i]
        actual_return = actual_returns.iloc[i]

        # Check if position changed
        if current_signal != previous_signal:
            trades += 1
            cost = transaction_cost
        else:
            cost = 0

        # Apply return if in position, minus costs
        if current_signal == 1:
            net_return = actual_return - cost
        else:
            net_return = -cost if cost > 0 else 0

        strategy_returns.append(net_return)
        previous_signal = current_signal

    return pd.Series(strategy_returns, index=actual_returns.index), trades


# =============================================================================
# PERFORMANCE METRICS
# =============================================================================

def calculate_metrics(returns, name="Strategy", num_trades=None):
    """Calculate comprehensive performance metrics"""
    if len(returns) == 0:
        return {}

    # Basic stats
    total_return = (1 + returns/100).prod() - 1
    annual_return = (1 + total_return) ** (252/len(returns)) - 1

    # Volatility
    volatility = returns.std() * np.sqrt(252/HOLDING_PERIOD)

    # Sharpe Ratio (5% risk-free rate)
    risk_free = 0.05
    sharpe = (annual_return - risk_free) / volatility if volatility > 0 else 0

    # Drawdown
    cumulative = (1 + returns/100).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    # Win rate
    win_rate = (returns > 0).sum() / len(returns) if len(returns) > 0 else 0

    # Profit factor
    gross_profit = returns[returns > 0].sum()
    gross_loss = abs(returns[returns < 0].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

    # Calmar ratio
    calmar = annual_return / abs(max_drawdown) if max_drawdown != 0 else np.inf

    metrics = {
        'Strategy': name,
        'Total Return (%)': total_return * 100,
        'Annual Return (%)': annual_return * 100,
        'Volatility (%)': volatility * 100,
        'Sharpe Ratio': sharpe,
        'Max Drawdown (%)': max_drawdown * 100,
        'Win Rate (%)': win_rate * 100,
        'Profit Factor': profit_factor,
        'Calmar Ratio': calmar,
        'Number of Trades': num_trades if num_trades is not None else len(returns)
    }

    return metrics


def evaluate_all_models(predictions, y_test):
    """Evaluate all models with backtesting"""
    logger.info("\n" + "="*80)
    logger.info("BACKTESTING & PERFORMANCE EVALUATION")
    logger.info("="*80)

    results = []
    strategy_returns_dict = {}
    signals_dict = {}

    for model_name in predictions.keys():
        logger.info(f"\nEvaluating {model_name}...")

        # Generate signals
        signals = generate_signals(predictions[model_name]['test'])
        signals_dict[model_name] = signals

        # Calculate strategy returns with costs
        strategy_returns, trades = calculate_strategy_returns(y_test, signals)
        strategy_returns_dict[model_name] = strategy_returns

        # Calculate metrics
        metrics = calculate_metrics(strategy_returns, model_name, trades)
        results.append(metrics)

        logger.info(f"  Sharpe: {metrics['Sharpe Ratio']:.2f}, "
                   f"Annual Return: {metrics['Annual Return (%)']:.2f}%, "
                   f"Trades: {trades}")

    # Buy and Hold baseline
    logger.info("\nEvaluating Buy & Hold baseline...")
    buy_hold_metrics = calculate_metrics(y_test, 'Buy & Hold')
    results.append(buy_hold_metrics)

    results_df = pd.DataFrame(results)

    logger.info("\n" + "="*80)
    logger.info("PERFORMANCE COMPARISON")
    logger.info("="*80)
    print("\n" + results_df.to_string(index=False))

    # Save results
    results_path = os.path.join(OUTPUTS_DIR, 'performance_results.csv')
    results_df.to_csv(results_path, index=False)
    logger.info(f"\n✅ Results saved to {results_path}")

    return results_df, strategy_returns_dict, signals_dict


# =============================================================================
# VISUALIZATIONS
# =============================================================================

def plot_equity_curves(y_test, strategy_returns_dict):
    """Plot equity curves for all models vs buy & hold"""
    logger.info("\n" + "="*80)
    logger.info("GENERATING EQUITY CURVES")
    logger.info("="*80)

    fig, ax = plt.subplots(figsize=(15, 8))

    # Buy & Hold
    buy_hold_equity = INITIAL_CAPITAL * (1 + y_test/100).cumprod()
    ax.plot(buy_hold_equity.index, buy_hold_equity.values,
            label='Buy & Hold', linewidth=2, linestyle='--', alpha=0.7, color='black')

    # Each model
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    for i, (model_name, returns) in enumerate(strategy_returns_dict.items()):
        equity = INITIAL_CAPITAL * (1 + returns/100).cumprod()
        ax.plot(equity.index, equity.values, label=model_name,
                linewidth=2, color=colors[i % len(colors)])

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Portfolio Value (₹)', fontsize=12)
    ax.set_title(f'Equity Curves: ML Models vs Buy & Hold\n(Initial Capital: ₹{INITIAL_CAPITAL:,})',
                fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=INITIAL_CAPITAL, color='gray', linestyle=':', alpha=0.5)

    # Format y-axis with commas
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))

    plt.tight_layout()

    save_path = os.path.join(OUTPUTS_DIR, 'equity_curves.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    logger.info(f"✅ Equity curve saved to {save_path}")


def plot_drawdowns(strategy_returns_dict):
    """Plot drawdown curves for all models"""
    logger.info("\n" + "="*80)
    logger.info("GENERATING DRAWDOWN ANALYSIS")
    logger.info("="*80)

    fig, ax = plt.subplots(figsize=(15, 6))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    for i, (model_name, returns) in enumerate(strategy_returns_dict.items()):
        cumulative = (1 + returns/100).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100

        ax.plot(drawdown.index, drawdown.values, label=model_name,
                linewidth=2, color=colors[i % len(colors)])

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Drawdown (%)', fontsize=12)
    ax.set_title('Drawdown Analysis', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    plt.tight_layout()

    save_path = os.path.join(OUTPUTS_DIR, 'drawdown_analysis.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    logger.info(f"✅ Drawdown plot saved to {save_path}")


def plot_feature_importance(model, feature_names, model_name, top_n=15):
    """Plot top N most important features"""
    if not hasattr(model, 'coef_'):
        return

    importance = pd.Series(model.coef_, index=feature_names)
    importance_abs = importance.abs().sort_values(ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))
    importance_abs.sort_values().plot(kind='barh', ax=ax)
    ax.set_xlabel('Absolute Coefficient Value', fontsize=12)
    ax.set_title(f'Top {top_n} Most Important Features - {model_name}',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()

    filename = f"feature_importance_{model_name.lower().replace(' ', '_')}.png"
    save_path = os.path.join(OUTPUTS_DIR, filename)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    logger.info(f"✅ Feature importance saved to {save_path}")


def generate_all_visualizations(models, feature_columns, y_test, strategy_returns_dict):
    """Generate all visualization plots"""
    logger.info("\n" + "="*80)
    logger.info("GENERATING VISUALIZATIONS")
    logger.info("="*80)

    # Equity curves
    plot_equity_curves(y_test, strategy_returns_dict)

    # Drawdowns
    plot_drawdowns(strategy_returns_dict)

    # Feature importance for each model
    for model_name, model in models.items():
        plot_feature_importance(model, feature_columns, model_name)


# =============================================================================
# ANALYSIS
# =============================================================================

def overfitting_analysis(models, predictions, X_train_scaled, y_train,
                        X_val_scaled, y_val, X_test_scaled, y_test):
    """Analyze overfitting by comparing performance across datasets"""
    logger.info("\n" + "="*80)
    logger.info("OVERFITTING ANALYSIS")
    logger.info("="*80)

    comparison = []

    for model_name in predictions.keys():
        train_pred = predictions[model_name]['train']
        val_pred = predictions[model_name]['val']
        test_pred = predictions[model_name]['test']

        comparison.append({
            'Model': model_name,
            'Train MSE': mean_squared_error(y_train, train_pred),
            'Val MSE': mean_squared_error(y_val, val_pred),
            'Test MSE': mean_squared_error(y_test, test_pred),
            'Train R²': r2_score(y_train, train_pred),
            'Val R²': r2_score(y_val, val_pred),
            'Test R²': r2_score(y_test, test_pred)
        })

    comp_df = pd.DataFrame(comparison)
    print("\n" + comp_df.to_string(index=False))

    print("\nInterpretation:")
    print("- If Train >> Val/Test: Model is overfitting")
    print("- If Train ≈ Val ≈ Test: Model generalizes well")
    print("- If all are poor: Model is underfitting or signal is weak")

    # Save
    save_path = os.path.join(OUTPUTS_DIR, 'overfitting_analysis.csv')
    comp_df.to_csv(save_path, index=False)
    logger.info(f"\n✅ Overfitting analysis saved to {save_path}")

    return comp_df


def regime_analysis(test_data, strategy_returns_dict):
    """Analyze performance by market regime"""
    logger.info("\n" + "="*80)
    logger.info("REGIME ANALYSIS")
    logger.info("="*80)

    # Define regimes based on 60-day returns
    test_data_copy = test_data.copy()
    test_data_copy['regime'] = pd.cut(
        test_data_copy['returns_60d'],
        bins=[-np.inf, -10, 10, np.inf],
        labels=['Bear', 'Sideways', 'Bull']
    )

    regime_results = []

    for model_name, returns in strategy_returns_dict.items():
        test_data_copy['strategy_returns'] = returns.values

        regime_perf = test_data_copy.groupby('regime').agg({
            'strategy_returns': ['mean', 'std', 'count']
        })

        print(f"\n{model_name}:")
        print(regime_perf)

        # Save regime performance
        for regime in ['Bear', 'Sideways', 'Bull']:
            if regime in regime_perf.index:
                regime_results.append({
                    'Model': model_name,
                    'Regime': regime,
                    'Mean Return': regime_perf.loc[regime, ('strategy_returns', 'mean')],
                    'Std Return': regime_perf.loc[regime, ('strategy_returns', 'std')],
                    'Count': regime_perf.loc[regime, ('strategy_returns', 'count')]
                })

    regime_df = pd.DataFrame(regime_results)
    save_path = os.path.join(OUTPUTS_DIR, 'regime_analysis.csv')
    regime_df.to_csv(save_path, index=False)
    logger.info(f"\n✅ Regime analysis saved to {save_path}")


# =============================================================================
# FINAL REPORT
# =============================================================================

def generate_final_report(results_df, overfitting_df):
    """Generate comprehensive final report"""
    logger.info("\n" + "="*80)
    logger.info("GENERATING FINAL REPORT")
    logger.info("="*80)

    report = []
    report.append("="*80)
    report.append("NIFTY 50 SHORT-TERM TRADING MODEL - FINAL REPORT")
    report.append("="*80)
    report.append(f"\nExperiment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\nCapital: ₹{INITIAL_CAPITAL:,}")
    report.append(f"Holding Period: {HOLDING_PERIOD} days")
    report.append(f"Transaction Cost: {TRANSACTION_COST}% per trade")
    report.append(f"\nData Period:")
    report.append(f"  Training:   {TRAIN_START} to {TRAIN_END}")
    report.append(f"  Validation: {VAL_START} to {VAL_END}")
    report.append(f"  Test:       {TEST_START} to {TEST_END}")

    report.append("\n" + "="*80)
    report.append("PERFORMANCE SUMMARY")
    report.append("="*80)
    report.append("\n" + results_df.to_string(index=False))

    report.append("\n" + "="*80)
    report.append("OVERFITTING ANALYSIS")
    report.append("="*80)
    report.append("\n" + overfitting_df.to_string(index=False))

    report.append("\n" + "="*80)
    report.append("KEY INSIGHTS")
    report.append("="*80)

    # Best model
    model_results = results_df[results_df['Strategy'] != 'Buy & Hold']
    best_idx = model_results['Sharpe Ratio'].idxmax()
    best_model = model_results.loc[best_idx]

    report.append(f"\nBest Model: {best_model['Strategy']}")
    report.append(f"  - Sharpe Ratio: {best_model['Sharpe Ratio']:.2f}")
    report.append(f"  - Annual Return: {best_model['Annual Return (%)']:.2f}%")
    report.append(f"  - Max Drawdown: {best_model['Max Drawdown (%)']:.2f}%")
    report.append(f"  - Win Rate: {best_model['Win Rate (%)']:.2f}%")
    report.append(f"  - Number of Trades: {int(best_model['Number of Trades'])}")

    # vs Buy & Hold
    bh = results_df[results_df['Strategy'] == 'Buy & Hold'].iloc[0]
    outperformance = best_model['Annual Return (%)'] - bh['Annual Return (%)']

    report.append(f"\nVs Buy & Hold:")
    report.append(f"  - Outperformance: {outperformance:+.2f}%")
    report.append(f"  - Better Sharpe: {best_model['Sharpe Ratio'] > bh['Sharpe Ratio']}")
    report.append(f"  - Lower Drawdown: {abs(best_model['Max Drawdown (%)']) < abs(bh['Max Drawdown (%)'])}")

    report.append("\n" + "="*80)
    report.append("CONCLUSION")
    report.append("="*80)

    if best_model['Sharpe Ratio'] > 1.5 and outperformance > 5:
        report.append("\n✅ Model shows STRONG PROMISE:")
        report.append("   - Sharpe ratio > 1.5 indicates good risk-adjusted returns")
        report.append("   - Outperforms buy-and-hold significantly")
        report.append("   - Ready for further optimization and walk-forward testing")
    elif best_model['Sharpe Ratio'] > 1.0 and outperformance > 0:
        report.append("\n⚠️  Model shows MODERATE PROMISE:")
        report.append("   - Positive Sharpe ratio indicates some edge")
        report.append("   - Beats buy-and-hold but margin is small")
        report.append("   - Consider feature engineering improvements")
    else:
        report.append("\n❌ Model shows WEAK SIGNAL:")
        report.append("   - Limited predictive power")
        report.append("   - May not beat transaction costs consistently")
        report.append("   - Recommend trying non-linear models or different features")

    report.append("\n" + "="*80)
    report.append("NEXT STEPS")
    report.append("="*80)
    report.append("\n1. Review feature importance - which features matter most?")
    report.append("2. Check for data leakage - verify all features are truly lagged")
    report.append("3. Test non-linear models (Random Forest, XGBoost)")
    report.append("4. Implement walk-forward validation with quarterly retraining")
    report.append("5. Add FII/DII flow data if available")
    report.append("6. Consider regime-specific models")
    report.append("7. Optimize position sizing based on prediction confidence")

    report_text = "\n".join(report)

    # Save to file
    report_path = os.path.join(OUTPUTS_DIR, 'final_report.txt')
    with open(report_path, 'w') as f:
        f.write(report_text)

    print("\n" + report_text)
    logger.info(f"\n✅ Final report saved to {report_path}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function"""
    logger.info("\n" + "="*80)
    logger.info("NIFTY 50 SHORT-TERM TRADING MODEL")
    logger.info("ML-based prediction of 5-day forward returns")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # 1. Data Collection
        all_data, volume_data = collect_all_data()

        # 2. Data Cleaning & Alignment
        df = align_and_clean_data(all_data, volume_data)

        # Save raw data
        raw_data_path = os.path.join(DATA_DIR, 'raw_data.csv')
        df.to_csv(raw_data_path)
        logger.info(f"✅ Raw data saved to {raw_data_path}")

        # 3. Feature Engineering
        features = engineer_features(df)

        # Save features
        features_path = os.path.join(FEATURES_DIR, 'features.csv')
        features.to_csv(features_path)
        logger.info(f"✅ Features saved to {features_path}")

        # 4. Train/Val/Test Split
        X_train, y_train, X_val, y_val, X_test, y_test, feature_columns, test_data = split_data(features)

        # 5. Feature Scaling
        X_train_scaled, X_val_scaled, X_test_scaled, scaler = scale_features(X_train, X_val, X_test)

        # 6. Model Training
        models, predictions = train_models(X_train_scaled, y_train, X_val_scaled, y_val, X_test_scaled, y_test)

        # 7. Save Models
        save_models(models, scaler)

        # 8. Backtesting & Performance Evaluation
        results_df, strategy_returns_dict, signals_dict = evaluate_all_models(predictions, y_test)

        # 9. Visualizations
        generate_all_visualizations(models, feature_columns, y_test, strategy_returns_dict)

        # 10. Overfitting Analysis
        overfitting_df = overfitting_analysis(models, predictions, X_train_scaled, y_train,
                                             X_val_scaled, y_val, X_test_scaled, y_test)

        # 11. Regime Analysis
        regime_analysis(test_data, strategy_returns_dict)

        # 12. Final Report
        generate_final_report(results_df, overfitting_df)

        logger.info("\n" + "="*80)
        logger.info("EXECUTION COMPLETE!")
        logger.info("="*80)
        logger.info(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"\nAll outputs saved to: {OUTPUTS_DIR}")
        logger.info(f"All models saved to: {MODELS_DIR}")

    except Exception as e:
        logger.error(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
