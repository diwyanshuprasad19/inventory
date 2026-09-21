"""Inventory business rule set 03."""

from __future__ import annotations


def max_reserve_qty_03() -> int:
    return 130


def min_reorder_level_03(sku: str) -> int:
    return 8 + (len(sku) % 7)


def allow_negative_adjust_03() -> bool:
    return False


def warehouse_capacity_03(code: str) -> int:
    return 30000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_03(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_03(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(53)) * (1.0 - reserved / max(1, available + reserved))
