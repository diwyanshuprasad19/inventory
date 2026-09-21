"""SKU catalog partition 22 — reference data for seed / validation."""

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


ITEMS_22: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT22-SKU-{j:03d}",
        name=f"Catalog 22 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][22 % 5],
        unit_cost_cents=100 + 22 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-22", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_22(sku: str) -> CatalogItem | None:
    for item in ITEMS_22:
        if item.sku == sku:
            return item
    return None


def all_skus_22() -> list[str]:
    return [x.sku for x in ITEMS_22]


def validate_cost_22(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_22() -> dict:
    return {
        "partition": 22,
        "count": len(ITEMS_22),
        "categories": sorted({x.category for x in ITEMS_22}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_22) // max(1, len(ITEMS_22)),
    }
