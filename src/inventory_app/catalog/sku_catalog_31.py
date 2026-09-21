"""SKU catalog partition 31 — reference data for seed / validation."""

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


ITEMS_31: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT31-SKU-{j:03d}",
        name=f"Catalog 31 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][31 % 5],
        unit_cost_cents=100 + 31 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-31", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_31(sku: str) -> CatalogItem | None:
    for item in ITEMS_31:
        if item.sku == sku:
            return item
    return None


def all_skus_31() -> list[str]:
    return [x.sku for x in ITEMS_31]


def validate_cost_31(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_31() -> dict:
    return {
        "partition": 31,
        "count": len(ITEMS_31),
        "categories": sorted({x.category for x in ITEMS_31}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_31) // max(1, len(ITEMS_31)),
    }
