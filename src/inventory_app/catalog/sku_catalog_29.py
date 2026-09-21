"""SKU catalog partition 29 — reference data for seed / validation."""

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


ITEMS_29: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT29-SKU-{j:03d}",
        name=f"Catalog 29 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][29 % 5],
        unit_cost_cents=100 + 29 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-29", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_29(sku: str) -> CatalogItem | None:
    for item in ITEMS_29:
        if item.sku == sku:
            return item
    return None


def all_skus_29() -> list[str]:
    return [x.sku for x in ITEMS_29]


def validate_cost_29(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_29() -> dict:
    return {
        "partition": 29,
        "count": len(ITEMS_29),
        "categories": sorted({x.category for x in ITEMS_29}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_29) // max(1, len(ITEMS_29)),
    }
