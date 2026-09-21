"""Inventory business rule set 15."""

from __future__ import annotations


def max_reserve_qty_15() -> int:
    return 250


def min_reorder_level_15(sku: str) -> int:
    return 20 + (len(sku) % 7)


def allow_negative_adjust_15() -> bool:
    return False


def warehouse_capacity_15(code: str) -> int:
    return 150000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_15(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_15(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(65)) * (1.0 - reserved / max(1, available + reserved))
