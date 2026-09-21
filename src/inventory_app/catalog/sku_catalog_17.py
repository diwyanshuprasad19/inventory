"""SKU catalog partition 17 — reference data for seed / validation."""

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


ITEMS_17: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT17-SKU-{j:03d}",
        name=f"Catalog 17 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][17 % 5],
        unit_cost_cents=100 + 17 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-17", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_17(sku: str) -> CatalogItem | None:
    for item in ITEMS_17:
        if item.sku == sku:
            return item
    return None


def all_skus_17() -> list[str]:
    return [x.sku for x in ITEMS_17]


def validate_cost_17(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_17() -> dict:
    return {
        "partition": 17,
        "count": len(ITEMS_17),
        "categories": sorted({x.category for x in ITEMS_17}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_17) // max(1, len(ITEMS_17)),
    }
