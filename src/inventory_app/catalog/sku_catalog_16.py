"""SKU catalog partition 16 — reference data for seed / validation."""

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


ITEMS_16: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT16-SKU-{j:03d}",
        name=f"Catalog 16 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][16 % 5],
        unit_cost_cents=100 + 16 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-16", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_16(sku: str) -> CatalogItem | None:
    for item in ITEMS_16:
        if item.sku == sku:
            return item
    return None


def all_skus_16() -> list[str]:
    return [x.sku for x in ITEMS_16]


def validate_cost_16(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_16() -> dict:
    return {
        "partition": 16,
        "count": len(ITEMS_16),
        "categories": sorted({x.category for x in ITEMS_16}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_16) // max(1, len(ITEMS_16)),
    }
