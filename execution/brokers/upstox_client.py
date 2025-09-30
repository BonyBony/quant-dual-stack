"""Minimal Upstox REST client based on the public OpenAPI documentation.

The client requires a pre-generated access token (OAuth) and optionally the
instrument-token mapping supplied via environment variables.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests


logger = logging.getLogger(__name__)


@dataclass
class OrderRequest:
    """Lightweight order descriptor passed to :meth:`UpstoxClient.place_order`."""

    symbol: str
    side: str  # "BUY" or "SELL"
    quantity: float
    product: str = "D"  # delivery (Upstox uses "I" for intraday)
    order_type: str = "MARKET"
    validity: str = "DAY"
    price: Optional[float] = None
    instrument_token: Optional[str] = None
    disclosed_quantity: int = 0
    trigger_price: Optional[float] = None
    is_amo: bool = False
    tag: Optional[str] = None


class UpstoxClient:
    """Thin REST client using requests."""

    BASE_URL_DEFAULT = "https://api-sandbox.upstox.com/v2"

    def __init__(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        instrument_map: Optional[Dict[str, str]] = None,
    ) -> None:
        token = access_token or os.getenv("UPSTOX_ACCESS_TOKEN", "")
        if not token:
            raise RuntimeError("UPSTOX_ACCESS_TOKEN missing; please set it in .env")

        self.api_key = api_key or os.getenv("UPSTOX_API_KEY", "")
        env_base = base_url or os.getenv("UPSTOX_BASE_URL")
        self.base_url = env_base.rstrip("/") if env_base else self.BASE_URL_DEFAULT

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Api-Version": "2.0",
            }
        )
        if self.api_key:
            self.session.headers["x-api-key"] = self.api_key

        self.instrument_map = instrument_map or self._parse_instrument_env()

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _parse_instrument_env(self) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        raw = os.getenv("UPSTOX_INSTRUMENT_TOKENS", "")
        for entry in raw.split(","):
            if not entry:
                continue
            if ":" not in entry:
                continue
            sym, token = entry.split(":", 1)
            mapping[sym.strip()] = token.strip()
        return mapping

    def _resolve_instrument(self, request: OrderRequest) -> str:
        if request.instrument_token:
            return request.instrument_token
        token = self.instrument_map.get(request.symbol)
        if not token:
            raise ValueError(
                "Instrument token for {sym} not found. Set UPSTOX_INSTRUMENT_TOKENS "
                "with entries like 'HDFCBANK.NS:NSE_EQ|INE040A01015'."
                .format(sym=request.symbol)
            )
        return token

    # ------------------------------------------------------------------ #
    # Order API
    # ------------------------------------------------------------------ #
    def place_order(self, request: OrderRequest) -> str:
        instrument_token = self._resolve_instrument(request)
        order_type = request.order_type.upper()
        payload = {
            "instrument_token": instrument_token,
            "quantity": int(round(request.quantity)),
            "transaction_type": request.side,
            "order_type": order_type,
            "product": request.product,
            "validity": request.validity,
            "disclosed_quantity": int(request.disclosed_quantity or 0),
            "is_amo": bool(request.is_amo),
        }

        # Upstox expects price to be omitted for MARKET and SL-M orders.
        needs_price = order_type not in {"MARKET", "SL-M"}
        if needs_price:
            if request.price is None:
                raise ValueError("price is required for non-market orders")
            payload["price"] = float(request.price)
        elif request.price is not None:
            payload["price"] = float(request.price)

        needs_trigger = order_type in {"SL", "SL-M"}
        if request.trigger_price is not None:
            payload["trigger_price"] = float(request.trigger_price)
        elif needs_trigger:
            raise ValueError("trigger_price is required for stop-loss orders")
        if request.tag:
            payload["tag"] = request.tag

        url = f"{self.base_url}/order/place"
        try:
            resp = self.session.post(url, json=payload, timeout=10)
        except requests.exceptions.RequestException as exc:  # network/DNS issues
            raise RuntimeError(f"Upstox order request failed: {exc}") from exc

        if resp.status_code >= 400:
            raise RuntimeError(f"Upstox order failed ({resp.status_code}): {resp.text}")

        data = resp.json()
        order_id = data.get("data", {}).get("order_id") or data.get("order_id", "")
        logger.info("Upstox order placed: %s", order_id or data)
        return order_id

    def close_position(self, symbol: str) -> None:
        logger.info("close_position for %s not implemented yet", symbol)

    def current_position(self, symbol: str) -> float:
        # TODO: call /portfolio/positions once we know the desired behaviour
        logger.info("current_position for %s not implemented; returning 0", symbol)
        return 0.0
