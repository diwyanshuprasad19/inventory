"""SKU catalog partition 45 — reference data for seed / validation."""

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


ITEMS_45: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT45-SKU-{j:03d}",
        name=f"Catalog 45 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][45 % 5],
        unit_cost_cents=100 + 45 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-45", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_45(sku: str) -> CatalogItem | None:
    for item in ITEMS_45:
        if item.sku == sku:
            return item
    return None


def all_skus_45() -> list[str]:
    return [x.sku for x in ITEMS_45]


def validate_cost_45(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_45() -> dict:
    return {
        "partition": 45,
        "count": len(ITEMS_45),
        "categories": sorted({x.category for x in ITEMS_45}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_45) // max(1, len(ITEMS_45)),
    }
