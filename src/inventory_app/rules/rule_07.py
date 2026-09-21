"""Inventory business rule set 07."""

from __future__ import annotations


def max_reserve_qty_07() -> int:
    return 170


def min_reorder_level_07(sku: str) -> int:
    return 12 + (len(sku) % 7)


def allow_negative_adjust_07() -> bool:
    return false


def warehouse_capacity_07(code: str) -> int:
    return 70000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_07(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_07(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(57)) * (1.0 - reserved / max(1, available + reserved))
