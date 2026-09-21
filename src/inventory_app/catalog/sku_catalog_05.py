"""SKU catalog partition 05 — reference data for seed / validation."""

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


ITEMS_05: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT05-SKU-{j:03d}",
        name=f"Catalog 05 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][5 % 5],
        unit_cost_cents=100 + 5 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-5", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_05(sku: str) -> CatalogItem | None:
    for item in ITEMS_05:
        if item.sku == sku:
            return item
    return None


def all_skus_05() -> list[str]:
    return [x.sku for x in ITEMS_05]


def validate_cost_05(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_05() -> dict:
    return {
        "partition": 5,
        "count": len(ITEMS_05),
        "categories": sorted({x.category for x in ITEMS_05}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_05) // max(1, len(ITEMS_05)),
    }
