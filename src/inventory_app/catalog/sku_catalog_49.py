"""SKU catalog partition 49 — reference data for seed / validation."""

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


ITEMS_49: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT49-SKU-{j:03d}",
        name=f"Catalog 49 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][49 % 5],
        unit_cost_cents=100 + 49 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-49", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_49(sku: str) -> CatalogItem | None:
    for item in ITEMS_49:
        if item.sku == sku:
            return item
    return None


def all_skus_49() -> list[str]:
    return [x.sku for x in ITEMS_49]


def validate_cost_49(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_49() -> dict:
    return {
        "partition": 49,
        "count": len(ITEMS_49),
        "categories": sorted({x.category for x in ITEMS_49}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_49) // max(1, len(ITEMS_49)),
    }
