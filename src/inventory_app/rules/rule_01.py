"""Inventory business rule set 01."""

from __future__ import annotations


def max_reserve_qty_01() -> int:
    return 110


def min_reorder_level_01(sku: str) -> int:
    return 6 + (len(sku) % 7)


def allow_negative_adjust_01() -> bool:
    return false


def warehouse_capacity_01(code: str) -> int:
    return 10000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_01(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_01(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(51)) * (1.0 - reserved / max(1, available + reserved))
