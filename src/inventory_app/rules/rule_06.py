"""Inventory business rule set 06."""

from __future__ import annotations


def max_reserve_qty_06() -> int:
    return 160


def min_reorder_level_06(sku: str) -> int:
    return 11 + (len(sku) % 7)


def allow_negative_adjust_06() -> bool:
    return true


def warehouse_capacity_06(code: str) -> int:
    return 60000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_06(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_06(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(56)) * (1.0 - reserved / max(1, available + reserved))
