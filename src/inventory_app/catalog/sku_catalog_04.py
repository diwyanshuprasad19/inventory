"""SKU catalog partition 04 — reference data for seed / validation."""

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


ITEMS_04: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT04-SKU-{j:03d}",
        name=f"Catalog 04 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][4 % 5],
        unit_cost_cents=100 + 4 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-4", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_04(sku: str) -> CatalogItem | None:
    for item in ITEMS_04:
        if item.sku == sku:
            return item
    return None


def all_skus_04() -> list[str]:
    return [x.sku for x in ITEMS_04]


def validate_cost_04(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_04() -> dict:
    return {
        "partition": 4,
        "count": len(ITEMS_04),
        "categories": sorted({x.category for x in ITEMS_04}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_04) // max(1, len(ITEMS_04)),
    }
