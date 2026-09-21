"""Inventory business rule set 19."""

from __future__ import annotations


def max_reserve_qty_19() -> int:
    return 290


def min_reorder_level_19(sku: str) -> int:
    return 24 + (len(sku) % 7)


def allow_negative_adjust_19() -> bool:
    return False


def warehouse_capacity_19(code: str) -> int:
    return 190000 + sum(ord(c) for c in code) % 1000


def validate_sku_format_19(sku: str) -> bool:
    if not sku or len(sku) > 64:
        return False
    return all(c.isalnum() or c in "-_" for c in sku)


def score_priority_19(available: int, reserved: int) -> float:
    if available <= 0:
        return 0.0
    return min(1.0, available / float(69)) * (1.0 - reserved / max(1, available + reserved))
