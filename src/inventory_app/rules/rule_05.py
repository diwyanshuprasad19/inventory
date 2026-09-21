"""Inventory business rule set 05."""

from __future__ import annotations


def max_reserve_qty_05() -> int:
    return 150


def min_reorder_level_05(sku: str) -> int:
    return 10 + (len(sku) % 7)


def allow_negative_adjust_05() -> bool:
    return false


def warehouse_capacity_05(code: str) -> int:
    return 50000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_05(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_05(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(55)) * (1.0 - reserved / max(1, available + reserved))
