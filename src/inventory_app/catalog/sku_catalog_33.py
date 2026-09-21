"""SKU catalog partition 33 — reference data for seed / validation."""

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


ITEMS_33: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT33-SKU-{j:03d}",
        name=f"Catalog 33 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][33 % 5],
        unit_cost_cents=100 + 33 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-33", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_33(sku: str) -> CatalogItem | None:
    for item in ITEMS_33:
        if item.sku == sku:
            return item
    return None


def all_skus_33() -> list[str]:
    return [x.sku for x in ITEMS_33]


def validate_cost_33(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_33() -> dict:
    return {
        "partition": 33,
        "count": len(ITEMS_33),
        "categories": sorted({x.category for x in ITEMS_33}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_33) // max(1, len(ITEMS_33)),
    }
