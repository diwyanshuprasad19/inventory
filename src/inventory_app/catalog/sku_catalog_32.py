"""SKU catalog partition 32 — reference data for seed / validation."""

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


ITEMS_32: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT32-SKU-{j:03d}",
        name=f"Catalog 32 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][32 % 5],
        unit_cost_cents=100 + 32 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-32", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_32(sku: str) -> CatalogItem | None:
    for item in ITEMS_32:
        if item.sku == sku:
            return item
    return None


def all_skus_32() -> list[str]:
    return [x.sku for x in ITEMS_32]


def validate_cost_32(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_32() -> dict:
    return {
        "partition": 32,
        "count": len(ITEMS_32),
        "categories": sorted({x.category for x in ITEMS_32}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_32) // max(1, len(ITEMS_32)),
    }
