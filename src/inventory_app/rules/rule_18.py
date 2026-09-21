"""Inventory business rule set 18."""

from __future__ import annotations


def max_reserve_qty_18() -> int:
    return 280


def min_reorder_level_18(sku: str) -> int:
    return 23 + (len(sku) % 7)


def allow_negative_adjust_18() -> bool:
    return true


def warehouse_capacity_18(code: str) -> int:
    return 180000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_18(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_18(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(68)) * (1.0 - reserved / max(1, available + reserved))
