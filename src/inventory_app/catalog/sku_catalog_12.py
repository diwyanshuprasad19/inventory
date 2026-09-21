"""SKU catalog partition 12 — reference data for seed / validation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogItem:
    sku: str
    name: str
    category: str
    unit_cost_cents: int
    default_qty: int
    tags: tuple[str, ...]


ITEMS_12: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT12-SKU-{j:03d}",
        name=f"Catalog 12 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][12 % 5],
        unit_cost_cents=100 + 12 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-12", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_12(sku: str) -> CatalogItem | None:
    for item in ITEMS_12:
        if item.sku == sku:
            return item
    return None


def all_skus_12() -> list[str]:
    return [x.sku for x in ITEMS_12]


def validate_cost_12(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_12() -> dict:
    return {
        "partition": 12,
        "count": len(ITEMS_12),
        "categories": sorted({x.category for x in ITEMS_12}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_12) // max(1, len(ITEMS_12)),
    }
