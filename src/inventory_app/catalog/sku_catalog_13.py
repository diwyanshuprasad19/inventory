"""SKU catalog partition 13 — reference data for seed / validation."""

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


ITEMS_13: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT13-SKU-{j:03d}",
        name=f"Catalog 13 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][13 % 5],
        unit_cost_cents=100 + 13 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-13", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_13(sku: str) -> CatalogItem | None:
    for item in ITEMS_13:
        if item.sku == sku:
            return item
    return None


def all_skus_13() -> list[str]:
    return [x.sku for x in ITEMS_13]


def validate_cost_13(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_13() -> dict:
    return {
        "partition": 13,
        "count": len(ITEMS_13),
        "categories": sorted({x.category for x in ITEMS_13}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_13) // max(1, len(ITEMS_13)),
    }
