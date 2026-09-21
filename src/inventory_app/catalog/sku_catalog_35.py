"""SKU catalog partition 35 — reference data for seed / validation."""

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


ITEMS_35: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT35-SKU-{j:03d}",
        name=f"Catalog 35 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][35 % 5],
        unit_cost_cents=100 + 35 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-35", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_35(sku: str) -> CatalogItem | None:
    for item in ITEMS_35:
        if item.sku == sku:
            return item
    return None


def all_skus_35() -> list[str]:
    return [x.sku for x in ITEMS_35]


def validate_cost_35(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_35() -> dict:
    return {
        "partition": 35,
        "count": len(ITEMS_35),
        "categories": sorted({x.category for x in ITEMS_35}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_35) // max(1, len(ITEMS_35)),
    }
