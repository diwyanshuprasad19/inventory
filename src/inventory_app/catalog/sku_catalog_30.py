"""SKU catalog partition 30 — reference data for seed / validation."""

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


ITEMS_30: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT30-SKU-{j:03d}",
        name=f"Catalog 30 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][30 % 5],
        unit_cost_cents=100 + 30 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-30", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_30(sku: str) -> CatalogItem | None:
    for item in ITEMS_30:
        if item.sku == sku:
            return item
    return None


def all_skus_30() -> list[str]:
    return [x.sku for x in ITEMS_30]


def validate_cost_30(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_30() -> dict:
    return {
        "partition": 30,
        "count": len(ITEMS_30),
        "categories": sorted({x.category for x in ITEMS_30}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_30) // max(1, len(ITEMS_30)),
    }
