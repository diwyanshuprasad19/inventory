"""SKU catalog partition 20 — reference data for seed / validation."""

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


ITEMS_20: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT20-SKU-{j:03d}",
        name=f"Catalog 20 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][20 % 5],
        unit_cost_cents=100 + 20 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-20", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_20(sku: str) -> CatalogItem | None:
    for item in ITEMS_20:
        if item.sku == sku:
            return item
    return None


def all_skus_20() -> list[str]:
    return [x.sku for x in ITEMS_20]


def validate_cost_20(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_20() -> dict:
    return {
        "partition": 20,
        "count": len(ITEMS_20),
        "categories": sorted({x.category for x in ITEMS_20}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_20) // max(1, len(ITEMS_20)),
    }
