"""Inventory business rule set 08."""

from __future__ import annotations


def max_reserve_qty_08() -> int:
    return 180


def min_reorder_level_08(sku: str) -> int:
    return 13 + (len(sku) % 7)


def allow_negative_adjust_08() -> bool:
    return True


def warehouse_capacity_08(code: str) -> int:
    return 80000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_08(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_08(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(58)) * (1.0 - reserved / max(1, available + reserved))
