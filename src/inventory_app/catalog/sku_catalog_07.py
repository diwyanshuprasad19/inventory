"""SKU catalog partition 07 — reference data for seed / validation."""

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


ITEMS_07: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT07-SKU-{j:03d}",
        name=f"Catalog 07 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][7 % 5],
        unit_cost_cents=100 + 7 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-7", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_07(sku: str) -> CatalogItem | None:
    for item in ITEMS_07:
        if item.sku == sku:
            return item
    return None


def all_skus_07() -> list[str]:
    return [x.sku for x in ITEMS_07]


def validate_cost_07(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_07() -> dict:
    return {
        "partition": 7,
        "count": len(ITEMS_07),
        "categories": sorted({x.category for x in ITEMS_07}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_07) // max(1, len(ITEMS_07)),
    }
