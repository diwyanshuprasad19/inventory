"""Inventory business rule set 16."""

from __future__ import annotations


def max_reserve_qty_16() -> int:
    return 260


def min_reorder_level_16(sku: str) -> int:
    return 21 + (len(sku) % 7)


def allow_negative_adjust_16() -> bool:
    return True


def warehouse_capacity_16(code: str) -> int:
    return 160000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_16(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_16(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(66)) * (1.0 - reserved / max(1, available + reserved))
