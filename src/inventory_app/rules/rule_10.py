"""Inventory business rule set 10."""

from __future__ import annotations


def max_reserve_qty_10() -> int:
    return 200


def min_reorder_level_10(sku: str) -> int:
    return 15 + (len(sku) % 7)


def allow_negative_adjust_10() -> bool:
    return true


def warehouse_capacity_10(code: str) -> int:
    return 100000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_10(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_10(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(60)) * (1.0 - reserved / max(1, available + reserved))
