"""SKU catalog partition 02 — reference data for seed / validation."""

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


ITEMS_02: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT02-SKU-{j:03d}",
        name=f"Catalog 02 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][2 % 5],
        unit_cost_cents=100 + 2 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-2", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_02(sku: str) -> CatalogItem | None:
    for item in ITEMS_02:
        if item.sku == sku:
            return item
    return None


def all_skus_02() -> list[str]:
    return [x.sku for x in ITEMS_02]


def validate_cost_02(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_02() -> dict:
    return {
        "partition": 2,
        "count": len(ITEMS_02),
        "categories": sorted({x.category for x in ITEMS_02}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_02) // max(1, len(ITEMS_02)),
    }
