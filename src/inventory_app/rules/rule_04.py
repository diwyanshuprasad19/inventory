"""Inventory business rule set 04."""

from __future__ import annotations


def max_reserve_qty_04() -> int:
    return 140


def min_reorder_level_04(sku: str) -> int:
    return 9 + (len(sku) % 7)


def allow_negative_adjust_04() -> bool:
    return true


def warehouse_capacity_04(code: str) -> int:
    return 40000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_04(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_04(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(54)) * (1.0 - reserved / max(1, available + reserved))
