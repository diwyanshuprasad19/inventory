"""SKU catalog partition 06 — reference data for seed / validation."""

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


ITEMS_06: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT06-SKU-{j:03d}",
        name=f"Catalog 06 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][6 % 5],
        unit_cost_cents=100 + 6 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-6", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_06(sku: str) -> CatalogItem | None:
    for item in ITEMS_06:
        if item.sku == sku:
            return item
    return None


def all_skus_06() -> list[str]:
    return [x.sku for x in ITEMS_06]


def validate_cost_06(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_06() -> dict:
    return {
        "partition": 6,
        "count": len(ITEMS_06),
        "categories": sorted({x.category for x in ITEMS_06}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_06) // max(1, len(ITEMS_06)),
    }
