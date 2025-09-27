"""Thin Upstox client wrapper.

This module intentionally avoids making real API calls. It provides a
structured placeholder that logs intended actions so the live loop can be
wired to Upstox without rewriting business logic.

Real integration steps (TODO):
    • Obtain API key/secret and redirect URI from Upstox developer portal.
    • Exchange credentials for an access token using the official SDK.
    • Replace stub methods with calls to place/modify/cancel orders.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Optional


logger = logging.getLogger(__name__)


@dataclass
class OrderRequest:
    symbol: str
    side: str  # "BUY" or "SELL"
    quantity: float
    product: str = "MIS"
    order_type: str = "MARKET"
    validity: str = "DAY"
    price: Optional[float] = None


class UpstoxClient:
    """Placeholder client that logs orders instead of sending them."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("UPSTOX_API_KEY", "")
        self.api_secret = api_secret or os.getenv("UPSTOX_API_SECRET", "")
        self.access_token = access_token or os.getenv("UPSTOX_ACCESS_TOKEN", "")
        self.connected = False

    # ------------------------------------------------------------------ #
    # Connection lifecycle (stubbed)
    # ------------------------------------------------------------------ #
    def connect(self) -> None:
        """Simulate connection establishment."""
        if not (self.api_key and self.access_token):
            logger.warning("Upstox credentials missing; running in dry mode")
        self.connected = True
        logger.info("Upstox client ready (dry-run)")

    # ------------------------------------------------------------------ #
    # Order interface
    # ------------------------------------------------------------------ #
    def place_order(self, request: OrderRequest) -> str:
        if not self.connected:
            self.connect()
        logger.info("[UPSTOX] %s %s qty=%.4f (%s) price=%s", request.side, request.symbol, request.quantity, request.order_type, request.price)
        return "SIM-ORDER-ID"

    def close_position(self, symbol: str) -> None:
        logger.info("[UPSTOX] Close position request for %s (dry mode)", symbol)

    # ------------------------------------------------------------------ #
    # Portfolio snapshot (placeholder)
    # ------------------------------------------------------------------ #
    def current_position(self, symbol: str) -> float:
        """Return current quantity; always zero in dry run."""
        return 0.0

