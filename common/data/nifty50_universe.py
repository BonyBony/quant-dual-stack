"""
NIFTY50 Universe Definition
---------------------------

Provides current NIFTY50 constituents with Yahoo Finance tickers.

TODO: Add point-in-time membership tracking to handle survivorship bias.
For MVP, we start with current constituents (as of Jan 2025).

Source: NSE India official NIFTY50 list
https://www.nseindia.com/market-data/live-equity-market
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass(frozen=True)
class Stock:
    """Stock metadata for universe construction."""
    symbol: str          # Yahoo Finance ticker (e.g., "RELIANCE.NS")
    name: str            # Company name
    sector: str          # GICS sector
    added_date: Optional[str] = None   # Date added to NIFTY50 (ISO format)
    removed_date: Optional[str] = None  # Date removed from NIFTY50 (ISO format)


# Current NIFTY50 constituents (January 2025)
# Note: This is a snapshot. For production, use point-in-time membership.
NIFTY50_CURRENT = [
    # Financials
    Stock("HDFCBANK.NS", "HDFC Bank", "Financials"),
    Stock("ICICIBANK.NS", "ICICI Bank", "Financials"),
    Stock("SBIN.NS", "State Bank of India", "Financials"),
    Stock("KOTAKBANK.NS", "Kotak Mahindra Bank", "Financials"),
    Stock("AXISBANK.NS", "Axis Bank", "Financials"),
    Stock("BAJFINANCE.NS", "Bajaj Finance", "Financials"),
    Stock("HDFCLIFE.NS", "HDFC Life Insurance", "Financials"),
    Stock("SBILIFE.NS", "SBI Life Insurance", "Financials"),
    Stock("BAJAJFINSV.NS", "Bajaj Finserv", "Financials"),

    # IT
    Stock("TCS.NS", "Tata Consultancy Services", "Information Technology"),
    Stock("INFY.NS", "Infosys", "Information Technology"),
    Stock("WIPRO.NS", "Wipro", "Information Technology"),
    Stock("HCLTECH.NS", "HCL Technologies", "Information Technology"),
    Stock("TECHM.NS", "Tech Mahindra", "Information Technology"),
    Stock("LTI.NS", "LTIMindtree", "Information Technology"),

    # Consumer
    Stock("RELIANCE.NS", "Reliance Industries", "Energy"),
    Stock("BHARTIARTL.NS", "Bharti Airtel", "Communication Services"),
    Stock("HINDUNILVR.NS", "Hindustan Unilever", "Consumer Staples"),
    Stock("ITC.NS", "ITC Limited", "Consumer Staples"),
    Stock("ASIANPAINT.NS", "Asian Paints", "Materials"),
    Stock("MARUTI.NS", "Maruti Suzuki", "Consumer Discretionary"),
    Stock("TITAN.NS", "Titan Company", "Consumer Discretionary"),
    Stock("NESTLEIND.NS", "Nestle India", "Consumer Staples"),
    Stock("BRITANNIA.NS", "Britannia Industries", "Consumer Staples"),

    # Industrials
    Stock("LT.NS", "Larsen & Toubro", "Industrials"),
    Stock("ULTRACEMCO.NS", "UltraTech Cement", "Materials"),
    Stock("ADANIENT.NS", "Adani Enterprises", "Industrials"),
    Stock("ADANIPORTS.NS", "Adani Ports", "Industrials"),
    Stock("POWERGRID.NS", "Power Grid Corp", "Utilities"),
    Stock("NTPC.NS", "NTPC Limited", "Utilities"),

    # Pharma & Healthcare
    Stock("SUNPHARMA.NS", "Sun Pharmaceutical", "Health Care"),
    Stock("DRREDDY.NS", "Dr. Reddy's Laboratories", "Health Care"),
    Stock("CIPLA.NS", "Cipla", "Health Care"),
    Stock("APOLLOHOSP.NS", "Apollo Hospitals", "Health Care"),

    # Metals & Mining
    Stock("HINDALCO.NS", "Hindalco Industries", "Materials"),
    Stock("TATASTEEL.NS", "Tata Steel", "Materials"),
    Stock("JSWSTEEL.NS", "JSW Steel", "Materials"),
    Stock("COALINDIA.NS", "Coal India", "Materials"),

    # Auto
    Stock("M&M.NS", "Mahindra & Mahindra", "Consumer Discretionary"),
    Stock("BAJAJ-AUTO.NS", "Bajaj Auto", "Consumer Discretionary"),
    Stock("EICHERMOT.NS", "Eicher Motors", "Consumer Discretionary"),
    Stock("HEROMOTOCO.NS", "Hero MotoCorp", "Consumer Discretionary"),

    # Oil & Gas
    Stock("ONGC.NS", "Oil and Natural Gas Corp", "Energy"),
    Stock("BPCL.NS", "Bharat Petroleum", "Energy"),

    # Others
    Stock("TATACONSUM.NS", "Tata Consumer Products", "Consumer Staples"),
    Stock("GRASIM.NS", "Grasim Industries", "Materials"),
    Stock("DIVISLAB.NS", "Divi's Laboratories", "Health Care"),
    Stock("INDUSINDBK.NS", "IndusInd Bank", "Financials"),
    Stock("TATAMOTORS.NS", "Tata Motors", "Consumer Discretionary"),
]


def get_nifty50_universe(as_of_date: Optional[str] = None) -> List[Stock]:
    """
    Get NIFTY50 constituents as of a specific date.

    Parameters
    ----------
    as_of_date : str, optional
        ISO format date (YYYY-MM-DD). If None, returns current constituents.

    Returns
    -------
    List[Stock]
        List of Stock objects in the index at that date.

    Notes
    -----
    For MVP, this returns the current list regardless of date.
    TODO: Implement point-in-time membership once we have historical data.

    Survivorship Bias Warning
    -------------------------
    Using current constituents for historical backtests introduces survivorship
    bias (we're only looking at "winners" that made it into the index). This
    will overstate historical performance. For production, track additions/removals.
    """
    if as_of_date is not None:
        # TODO: Filter by added_date/removed_date
        # For now, return current list with a warning
        import logging
        logging.warning(
            f"Point-in-time universe for {as_of_date} not implemented. "
            "Returning current constituents (survivorship bias present)."
        )

    return NIFTY50_CURRENT


def get_nifty50_symbols(as_of_date: Optional[str] = None) -> List[str]:
    """Get Yahoo Finance ticker symbols for NIFTY50."""
    return [stock.symbol for stock in get_nifty50_universe(as_of_date)]


def get_nifty50_by_sector() -> dict[str, List[Stock]]:
    """Group NIFTY50 stocks by sector for sector-neutral strategies."""
    from collections import defaultdict
    sectors = defaultdict(list)
    for stock in NIFTY50_CURRENT:
        sectors[stock.sector].append(stock)
    return dict(sectors)


# Quick reference subsets for testing/MVP
NIFTY50_TOP10_LIQUID = [
    "RELIANCE.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "INFY.NS",
    "TCS.NS",
    "HINDUNILVR.NS",
    "ITC.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "KOTAKBANK.NS",
]

NIFTY50_TEST_SET = [
    "HDFCBANK.NS",
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "ICICIBANK.NS",
]
