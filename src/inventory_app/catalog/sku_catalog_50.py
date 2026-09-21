"""SKU catalog partition 50 — reference data for seed / validation."""

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


ITEMS_50: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT50-SKU-{j:03d}",
        name=f"Catalog 50 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][50 % 5],
        unit_cost_cents=100 + 50 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-50", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_50(sku: str) -> CatalogItem | None:
    for item in ITEMS_50:
        if item.sku == sku:
            return item
    return None


def all_skus_50() -> list[str]:
    return [x.sku for x in ITEMS_50]


def validate_cost_50(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_50() -> dict:
    return {
        "partition": 50,
        "count": len(ITEMS_50),
        "categories": sorted({x.category for x in ITEMS_50}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_50) // max(1, len(ITEMS_50)),
    }
