"""SKU catalog partition 25 — reference data for seed / validation."""

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


ITEMS_25: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT25-SKU-{j:03d}",
        name=f"Catalog 25 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][25 % 5],
        unit_cost_cents=100 + 25 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-25", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_25(sku: str) -> CatalogItem | None:
    for item in ITEMS_25:
        if item.sku == sku:
            return item
    return None


def all_skus_25() -> list[str]:
    return [x.sku for x in ITEMS_25]


def validate_cost_25(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_25() -> dict:
    return {
        "partition": 25,
        "count": len(ITEMS_25),
        "categories": sorted({x.category for x in ITEMS_25}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_25) // max(1, len(ITEMS_25)),
    }
