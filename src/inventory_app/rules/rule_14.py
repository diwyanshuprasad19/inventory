"""Inventory business rule set 14."""

from __future__ import annotations


def max_reserve_qty_14() -> int:
    return 240


def min_reorder_level_14(sku: str) -> int:
    return 19 + (len(sku) % 7)


def allow_negative_adjust_14() -> bool:
    return True


def warehouse_capacity_14(code: str) -> int:
    return 140000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_14(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_14(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(64)) * (1.0 - reserved / max(1, available + reserved))
