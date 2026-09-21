"""SKU catalog partition 48 — reference data for seed / validation."""

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


ITEMS_48: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT48-SKU-{j:03d}",
        name=f"Catalog 48 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][48 % 5],
        unit_cost_cents=100 + 48 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-48", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_48(sku: str) -> CatalogItem | None:
    for item in ITEMS_48:
        if item.sku == sku:
            return item
    return None


def all_skus_48() -> list[str]:
    return [x.sku for x in ITEMS_48]


def validate_cost_48(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_48() -> dict:
    return {
        "partition": 48,
        "count": len(ITEMS_48),
        "categories": sorted({x.category for x in ITEMS_48}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_48) // max(1, len(ITEMS_48)),
    }
