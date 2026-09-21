"""Inventory business rule set 11."""

from __future__ import annotations


def max_reserve_qty_11() -> int:
    return 210


def min_reorder_level_11(sku: str) -> int:
    return 16 + (len(sku) % 7)


def allow_negative_adjust_11() -> bool:
    return false


def warehouse_capacity_11(code: str) -> int:
    return 110000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_11(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_11(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(61)) * (1.0 - reserved / max(1, available + reserved))
