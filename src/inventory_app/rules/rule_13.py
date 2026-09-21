"""Inventory business rule set 13."""

from __future__ import annotations


def max_reserve_qty_13() -> int:
    return 230


def min_reorder_level_13(sku: str) -> int:
    return 18 + (len(sku) % 7)


def allow_negative_adjust_13() -> bool:
    return False


def warehouse_capacity_13(code: str) -> int:
    return 130000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_13(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_13(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(63)) * (1.0 - reserved / max(1, available + reserved))
