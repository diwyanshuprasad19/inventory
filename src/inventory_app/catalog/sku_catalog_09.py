"""SKU catalog partition 09 — reference data for seed / validation."""

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


ITEMS_09: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT09-SKU-{j:03d}",
        name=f"Catalog 09 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][9 % 5],
        unit_cost_cents=100 + 9 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-9", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_09(sku: str) -> CatalogItem | None:
    for item in ITEMS_09:
        if item.sku == sku:
            return item
    return None


def all_skus_09() -> list[str]:
    return [x.sku for x in ITEMS_09]


def validate_cost_09(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_09() -> dict:
    return {
        "partition": 9,
        "count": len(ITEMS_09),
        "categories": sorted({x.category for x in ITEMS_09}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_09) // max(1, len(ITEMS_09)),
    }
