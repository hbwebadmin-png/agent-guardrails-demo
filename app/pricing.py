"""Tiny pricing module the demo agent maintains."""
import requests


def apply_discount(price: float, percent: float) -> float:
    """Return price after a percentage discount, rounded to cents."""
    if price < 0:
        raise ValueError("price must be non-negative")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


def fetch_exchange_rate(url: str, timeout: float = 5.0) -> float:
    """Fetch a JSON exchange rate of the form {"rate": 1.08}. Not called by tests."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return float(response.json()["rate"])
