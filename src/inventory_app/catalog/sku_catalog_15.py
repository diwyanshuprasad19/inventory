"""SKU catalog partition 15 — reference data for seed / validation."""

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


ITEMS_15: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT15-SKU-{j:03d}",
        name=f"Catalog 15 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][15 % 5],
        unit_cost_cents=100 + 15 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-15", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_15(sku: str) -> CatalogItem | None:
    for item in ITEMS_15:
        if item.sku == sku:
            return item
    return None


def all_skus_15() -> list[str]:
    return [x.sku for x in ITEMS_15]


def validate_cost_15(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_15() -> dict:
    return {
        "partition": 15,
        "count": len(ITEMS_15),
        "categories": sorted({x.category for x in ITEMS_15}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_15) // max(1, len(ITEMS_15)),
    }
