"""SKU catalog partition 24 — reference data for seed / validation."""

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


ITEMS_24: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT24-SKU-{j:03d}",
        name=f"Catalog 24 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][24 % 5],
        unit_cost_cents=100 + 24 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-24", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_24(sku: str) -> CatalogItem | None:
    for item in ITEMS_24:
        if item.sku == sku:
            return item
    return None


def all_skus_24() -> list[str]:
    return [x.sku for x in ITEMS_24]


def validate_cost_24(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_24() -> dict:
    return {
        "partition": 24,
        "count": len(ITEMS_24),
        "categories": sorted({x.category for x in ITEMS_24}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_24) // max(1, len(ITEMS_24)),
    }
