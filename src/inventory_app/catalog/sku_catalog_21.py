"""SKU catalog partition 21 — reference data for seed / validation."""

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


ITEMS_21: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT21-SKU-{j:03d}",
        name=f"Catalog 21 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][21 % 5],
        unit_cost_cents=100 + 21 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-21", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_21(sku: str) -> CatalogItem | None:
    for item in ITEMS_21:
        if item.sku == sku:
            return item
    return None


def all_skus_21() -> list[str]:
    return [x.sku for x in ITEMS_21]


def validate_cost_21(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_21() -> dict:
    return {
        "partition": 21,
        "count": len(ITEMS_21),
        "categories": sorted({x.category for x in ITEMS_21}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_21) // max(1, len(ITEMS_21)),
    }
