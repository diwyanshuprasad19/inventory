"""Inventory business rule set 12."""

from __future__ import annotations


def max_reserve_qty_12() -> int:
    return 220


def min_reorder_level_12(sku: str) -> int:
    return 17 + (len(sku) % 7)


def allow_negative_adjust_12() -> bool:
    return True


def warehouse_capacity_12(code: str) -> int:
    return 120000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_12(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_12(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(62)) * (1.0 - reserved / max(1, available + reserved))
