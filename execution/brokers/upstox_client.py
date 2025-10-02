"""Minimal Upstox REST client based on the public OpenAPI documentation.

The client requires a pre-generated access token (OAuth) and optionally the
instrument-token mapping supplied via environment variables.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

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


@dataclass
class Instrument:
    """Represents a single entry from the Upstox instrument master dump."""

    instrument_key: str
    trading_symbol: str
    segment: Optional[str] = None
    exchange: Optional[str] = None
    name: Optional[str] = None
    isin: Optional[str] = None
    instrument_type: Optional[str] = None
    lot_size: Optional[float] = None
    freeze_quantity: Optional[float] = None
    exchange_token: Optional[str] = None
    tick_size: Optional[float] = None
    short_name: Optional[str] = None
    security_type: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> Optional[Instrument]:
        instrument_key = payload.get("instrument_key")
        trading_symbol = payload.get("trading_symbol")
        if not instrument_key or not trading_symbol:
            return None

        def _to_float(value: Any) -> Optional[float]:
            if value in (None, ""):
                return None
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        return cls(
            instrument_key=instrument_key,
            trading_symbol=str(trading_symbol),
            segment=payload.get("segment"),
            exchange=payload.get("exchange"),
            name=payload.get("name"),
            isin=payload.get("isin"),
            instrument_type=payload.get("instrument_type"),
            lot_size=_to_float(payload.get("lot_size")),
            freeze_quantity=_to_float(payload.get("freeze_quantity")),
            exchange_token=str(payload.get("exchange_token")) if payload.get("exchange_token") else None,
            tick_size=_to_float(payload.get("tick_size")),
            short_name=payload.get("short_name"),
            security_type=payload.get("security_type"),
            raw=payload,
        )

    def index_keys(self) -> List[str]:
        """Return candidate lookup keys derived from the instrument metadata."""

        keys: List[str] = []
        if self.trading_symbol:
            keys.append(self.trading_symbol)

        exch = (self.exchange or "").upper()
        symbol = (self.trading_symbol or "").upper()
        if symbol and exch:
            keys.append(f"{symbol}.{exch}")
            if exch == "NSE":
                keys.append(f"{symbol}.NS")
            elif exch == "BSE":
                keys.append(f"{symbol}.BO")

        if self.name:
            keys.append(self.name)

        if self.isin:
            keys.append(self.isin)

        # Allow looking up by the canonical instrument key as well.
        keys.append(self.instrument_key)
        return keys

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation preserving unknown fields."""

        data = dict(self.raw)
        data.setdefault("instrument_key", self.instrument_key)
        data.setdefault("trading_symbol", self.trading_symbol)
        if self.segment is not None:
            data.setdefault("segment", self.segment)
        if self.exchange is not None:
            data.setdefault("exchange", self.exchange)
        if self.name is not None:
            data.setdefault("name", self.name)
        if self.isin is not None:
            data.setdefault("isin", self.isin)
        if self.instrument_type is not None:
            data.setdefault("instrument_type", self.instrument_type)
        if self.lot_size is not None:
            data.setdefault("lot_size", self.lot_size)
        if self.freeze_quantity is not None:
            data.setdefault("freeze_quantity", self.freeze_quantity)
        if self.exchange_token is not None:
            data.setdefault("exchange_token", self.exchange_token)
        if self.tick_size is not None:
            data.setdefault("tick_size", self.tick_size)
        if self.short_name is not None:
            data.setdefault("short_name", self.short_name)
        if self.security_type is not None:
            data.setdefault("security_type", self.security_type)
        return data


class UpstoxClient:
    """Thin REST client using requests."""

    BASE_URL_DEFAULT = "https://api-sandbox.upstox.com/v2"

    def __init__(
        self,
        access_token: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        instrument_map: Optional[Dict[str, str]] = None,
        instrument_source: Optional[str] = None,
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

        self._instrument_catalog: List[Instrument] = []
        json_source = instrument_source or os.getenv("UPSTOX_INSTRUMENTS_JSON")
        if json_source:
            self._instrument_catalog = self._load_instrument_catalog(json_source)

        env_map = self._parse_instrument_env()
        catalog_map = self._build_instrument_index(self._instrument_catalog)
        provided_map = instrument_map or {}

        merged: Dict[str, str] = {}
        # Catalog provides the broadest coverage; user overrides take precedence.
        merged.update(catalog_map)
        merged.update(env_map)
        merged.update({self._normalize_symbol(k): v for k, v in provided_map.items()})
        self.instrument_map = merged

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalize_symbol(value: Optional[str]) -> str:
        if value is None:
            return ""
        return value.strip().upper()

    def _parse_instrument_env(self) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        raw = os.getenv("UPSTOX_INSTRUMENT_TOKENS", "")
        for entry in raw.split(","):
            if not entry or ":" not in entry:
                continue
            sym, token = entry.split(":", 1)
            normalized = self._normalize_symbol(sym)
            if not normalized:
                continue
            mapping[normalized] = token.strip()
        return mapping

    def _load_instrument_catalog(self, source: str) -> List[Instrument]:
        entries: List[Dict[str, Any]] = []
        try:
            if source.startswith(("http://", "https://")):
                resp = self.session.get(source, timeout=15)
                resp.raise_for_status()
                payload: Any = resp.json()
            else:
                with open(source, "r", encoding="utf-8") as handle:
                    payload = json.load(handle)
        except (OSError, json.JSONDecodeError, requests.exceptions.RequestException) as exc:
            logger.warning("Failed to load Upstox instrument catalog from %s: %s", source, exc)
            return []

        if isinstance(payload, dict):
            if isinstance(payload.get("data"), list):
                entries = payload.get("data", [])
            elif isinstance(payload.get("instruments"), list):
                entries = payload.get("instruments", [])
            else:
                # Some dumps use the exchange code as top-level key.
                for value in payload.values():
                    if isinstance(value, list):
                        entries = value
                        break
        elif isinstance(payload, list):
            entries = payload

        instruments: List[Instrument] = []
        for item in entries:
            if not isinstance(item, dict):
                continue
            instrument = Instrument.from_payload(item)
            if instrument:
                instruments.append(instrument)

        if instruments:
            logger.info("Loaded %d Upstox instruments from %s", len(instruments), source)
        else:
            logger.warning("No instrument entries parsed from %s", source)
        return instruments

    def _build_instrument_index(self, instruments: Iterable[Instrument]) -> Dict[str, str]:
        index: Dict[str, str] = {}
        for instrument in instruments:
            for key in instrument.index_keys():
                normalized = self._normalize_symbol(key)
                if not normalized or normalized in index:
                    continue
                index[normalized] = instrument.instrument_key
        return index

    # ------------------------------------------------------------------ #
    # Portfolio helpers
    # ------------------------------------------------------------------ #
    def _fetch_positions(self) -> List[Dict[str, Any]]:
        endpoints = (
            f"{self.base_url}/portfolio/short-term-positions",
            f"{self.base_url}/portfolio/long-term-holdings",
        )
        aggregated: List[Dict[str, Any]] = []

        for url in endpoints:
            try:
                resp = self.session.get(url, timeout=10)
            except requests.exceptions.RequestException as exc:
                logger.warning("Upstox positions request to %s failed: %s", url, exc)
                continue

            if resp.status_code == 404:
                logger.info("Upstox endpoint %s unavailable (404)", url)
                continue
            if resp.status_code >= 400:
                logger.warning(
                    "Upstox positions request to %s failed (%s): %s",
                    url,
                    resp.status_code,
                    resp.text,
                )
                continue

            payload = resp.json()
            entries: List[Dict[str, Any]] = []
            if isinstance(payload, dict):
                if isinstance(payload.get("data"), list):
                    entries = payload.get("data", [])
                elif isinstance(payload.get("positions"), list):
                    entries = payload.get("positions", [])
            elif isinstance(payload, list):
                entries = payload

            if entries:
                aggregated.extend(entries)

        return aggregated

    def _match_position_entry(self, symbol: str, instrument_token: Optional[str]) -> Optional[Dict[str, Any]]:
        symbol_norm = self._normalize_symbol(symbol)
        token_norm = self._normalize_symbol(instrument_token)
        positions = self._fetch_positions()

        for entry in positions:
            candidates = [
                entry.get("instrument_token"),
                entry.get("instrument_key"),
                entry.get("trading_symbol"),
                entry.get("symbol"),
            ]
            for candidate in candidates:
                candidate_norm = self._normalize_symbol(candidate)
                if not candidate_norm:
                    continue
                if token_norm and candidate_norm == token_norm:
                    return entry
                if candidate_norm == symbol_norm:
                    return entry
        return None

    @staticmethod
    def _extract_quantity(entry: Dict[str, Any]) -> Optional[float]:
        quantity_keys = (
            "net_quantity",
            "netQty",
            "net_qty",
            "quantity",
            "qty",
            "day_quantity",
            "dayQty",
        )
        for key in quantity_keys:
            if key not in entry or entry[key] in (None, ""):
                continue
            value = entry[key]
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
        return None

    def _candidate_lookup_keys(self, symbol: str) -> List[str]:
        keys: List[str] = []
        normalized = self._normalize_symbol(symbol)
        if not normalized:
            return keys

        def _add(value: Optional[str]) -> None:
            norm = self._normalize_symbol(value)
            if norm and norm not in keys:
                keys.append(norm)

        _add(normalized)

        # Allow direct usage of canonical instrument key (segment|isin etc.).
        if "|" in normalized:
            segment_part = normalized.split("|", 1)[0]
            if segment_part and "." not in segment_part:
                _add(segment_part)
            return keys

        if "." in normalized:
            base, suffix = normalized.split(".", 1)
        else:
            base, suffix = normalized, ""

        _add(base)

        if base:
            if suffix in {"NS", "NSE"}:
                _add(f"{base}.NS")
                _add(f"{base}.NSE")
                _add(f"{base}.NSE_EQ")
            elif suffix in {"BO", "BSE"}:
                _add(f"{base}.BO")
                _add(f"{base}.BSE")
                _add(f"{base}.BSE_EQ")
            elif suffix:
                _add(f"{base}.{suffix}")
            else:
                # Try a few common defaults when suffix is absent.
                _add(f"{base}.NS")
                _add(f"{base}.NSE")
                _add(f"{base}.BSE")
                _add(f"{base}.BO")

        return keys

    def _lookup_instrument_token(self, symbol: Optional[str]) -> Optional[str]:
        if not symbol:
            return None
        for key in self._candidate_lookup_keys(symbol):
            token = self.instrument_map.get(key)
            if token:
                return token
        return None

    def _resolve_instrument(self, request: OrderRequest) -> str:
        if request.instrument_token:
            return request.instrument_token

        token = self._lookup_instrument_token(request.symbol)
        if token:
            return token

        raise ValueError(
            "Instrument token for {sym} not found. Provide an explicit instrument_token, set "
            "UPSTOX_INSTRUMENT_TOKENS (e.g. 'HDFCBANK.NS:NSE_EQ|INE040A01015'), or configure "
            "UPSTOX_INSTRUMENTS_JSON with the latest instrument dump."
            .format(sym=request.symbol)
        )

    # ------------------------------------------------------------------ #
    # Instrument search helpers
    # ------------------------------------------------------------------ #
    def search_instruments(
        self,
        query: str,
        *,
        segment: Optional[str] = None,
        exchange: Optional[str] = None,
        limit: int = 20,
    ) -> List[Instrument]:
        """Search the cached instrument catalog for entries matching ``query``.

        The search is case-insensitive and attempts to match the query against the
        trading symbol, exchange-qualified symbols, instrument key, instrument
        name, short name, and ISIN. Use :meth:`Instrument.to_dict` to convert
        results to plain dictionaries when interacting with JSON-centric code.
        """

        if not self._instrument_catalog:
            logger.warning("Instrument catalog empty; set UPSTOX_INSTRUMENTS_JSON to enable search")
            return []

        query_norm = self._normalize_symbol(query)
        seg_norm = self._normalize_symbol(segment)
        exch_norm = self._normalize_symbol(exchange)

        results: List[Instrument] = []
        for instrument in self._instrument_catalog:
            if seg_norm and self._normalize_symbol(instrument.segment) != seg_norm:
                continue
            if exch_norm and self._normalize_symbol(instrument.exchange) != exch_norm:
                continue

            haystack = [
                instrument.trading_symbol,
                instrument.instrument_key,
                instrument.name,
                instrument.short_name,
                instrument.isin,
            ]
            if any(query_norm in self._normalize_symbol(candidate) for candidate in haystack if candidate):
                results.append(instrument)
                if len(results) >= limit:
                    break

        return results

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

    def close_position(
        self,
        symbol: str,
        *,
        quantity: Optional[float] = None,
        side: Optional[str] = None,
        order_type: str = "LIMIT",
        price: Optional[float] = None,
        trigger_price: Optional[float] = None,
        product: Optional[str] = None,
        validity: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> str:
        """Flatten an open position by submitting the appropriate opposite order."""

        order_type = order_type.upper()
        instrument_token = self._lookup_instrument_token(symbol)
        entry = self._match_position_entry(symbol, instrument_token)

        if instrument_token is None and entry:
            instrument_token = entry.get("instrument_token") or entry.get("instrument_key")

        net_quantity = None
        if entry:
            net_quantity = self._extract_quantity(entry)

        if quantity is None:
            if net_quantity is None:
                raise RuntimeError(f"Unable to determine quantity to close for {symbol}")
            close_quantity = abs(net_quantity)
        else:
            close_quantity = float(quantity)

        if close_quantity <= 0:
            raise ValueError("close_position quantity must be positive")

        if side is None:
            if net_quantity is None or net_quantity == 0:
                raise RuntimeError(f"Unable to infer closing side for {symbol}")
            side = "SELL" if net_quantity > 0 else "BUY"
        else:
            side = side.upper()
            if side not in {"BUY", "SELL"}:
                raise ValueError("side must be 'BUY' or 'SELL'")

        def _derive_price() -> Optional[float]:
            if entry is None:
                return None
            for key in ("last_price", "ltp", "close_price", "average_price", "avg_price"):
                if key in entry and entry[key] not in (None, ""):
                    try:
                        return float(entry[key])
                    except (TypeError, ValueError):
                        continue
            return None

        final_price: Optional[float]
        final_trigger: Optional[float]
        if order_type == "MARKET":
            final_price = None
            final_trigger = None
        elif order_type == "SL-M":
            final_price = None
            final_trigger = trigger_price or price
            if final_trigger is None:
                derived = _derive_price()
                final_trigger = derived
            if final_trigger is None:
                raise ValueError("trigger_price required for SL-M close orders")
        else:
            final_price = price if price is not None else _derive_price()
            if final_price is None:
                raise ValueError("price required for non-market close orders")
            final_trigger = trigger_price if trigger_price is not None else final_price

        request = OrderRequest(
            symbol=symbol,
            side=side,
            quantity=close_quantity,
            product=product or (entry.get("product") if entry else "D"),
            order_type=order_type,
            validity=validity or (entry.get("validity") if entry else "DAY"),
            price=final_price,
            instrument_token=instrument_token,
            trigger_price=final_trigger,
            tag=tag,
        )
        return self.place_order(request)

    def current_position(self, symbol: str) -> float:
        instrument_token = self._lookup_instrument_token(symbol)
        entry = self._match_position_entry(symbol, instrument_token)
        if not entry:
            return 0.0
        quantity = self._extract_quantity(entry)
        return float(quantity or 0.0)
