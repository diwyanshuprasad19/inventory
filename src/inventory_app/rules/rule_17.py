"""Inventory business rule set 17."""

from __future__ import annotations


def max_reserve_qty_17() -> int:
    return 270


def min_reorder_level_17(sku: str) -> int:
    return 22 + (len(sku) % 7)


def allow_negative_adjust_17() -> bool:
    return false


def warehouse_capacity_17(code: str) -> int:
    return 170000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_17(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_17(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(67)) * (1.0 - reserved / max(1, available + reserved))
