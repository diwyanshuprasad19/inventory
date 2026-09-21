"""SKU catalog partition 01 — reference data for seed / validation."""

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


ITEMS_01: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT01-SKU-{j:03d}",
        name=f"Catalog 01 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][1 % 5],
        unit_cost_cents=100 + 1 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-1", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_01(sku: str) -> CatalogItem | None:
    for item in ITEMS_01:
        if item.sku == sku:
            return item
    return None


def all_skus_01() -> list[str]:
    return [x.sku for x in ITEMS_01]


def validate_cost_01(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_01() -> dict:
    return {
        "partition": 1,
        "count": len(ITEMS_01),
        "categories": sorted({x.category for x in ITEMS_01}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_01) // max(1, len(ITEMS_01)),
    }
