"""SKU catalog partition 03 — reference data for seed / validation."""

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


ITEMS_03: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT03-SKU-{j:03d}",
        name=f"Catalog 03 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][3 % 5],
        unit_cost_cents=100 + 3 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-3", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_03(sku: str) -> CatalogItem | None:
    for item in ITEMS_03:
        if item.sku == sku:
            return item
    return None


def all_skus_03() -> list[str]:
    return [x.sku for x in ITEMS_03]


def validate_cost_03(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_03() -> dict:
    return {
        "partition": 3,
        "count": len(ITEMS_03),
        "categories": sorted({x.category for x in ITEMS_03}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_03) // max(1, len(ITEMS_03)),
    }
