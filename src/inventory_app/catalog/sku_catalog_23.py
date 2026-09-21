"""SKU catalog partition 23 — reference data for seed / validation."""

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


ITEMS_23: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT23-SKU-{j:03d}",
        name=f"Catalog 23 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][23 % 5],
        unit_cost_cents=100 + 23 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-23", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_23(sku: str) -> CatalogItem | None:
    for item in ITEMS_23:
        if item.sku == sku:
            return item
    return None


def all_skus_23() -> list[str]:
    return [x.sku for x in ITEMS_23]


def validate_cost_23(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_23() -> dict:
    return {
        "partition": 23,
        "count": len(ITEMS_23),
        "categories": sorted({x.category for x in ITEMS_23}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_23) // max(1, len(ITEMS_23)),
    }
