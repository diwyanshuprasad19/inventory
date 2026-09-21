"""Inventory business rule set 20."""

from __future__ import annotations


def max_reserve_qty_20() -> int:
    return 300


def min_reorder_level_20(sku: str) -> int:
    return 25 + (len(sku) % 7)


def allow_negative_adjust_20() -> bool:
    return True


def warehouse_capacity_20(code: str) -> int:
    return 200000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_20(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_20(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(70)) * (1.0 - reserved / max(1, available + reserved))
