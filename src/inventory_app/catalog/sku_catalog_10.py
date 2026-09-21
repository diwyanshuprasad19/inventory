"""SKU catalog partition 10 — reference data for seed / validation."""

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


ITEMS_10: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT10-SKU-{j:03d}",
        name=f"Catalog 10 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][10 % 5],
        unit_cost_cents=100 + 10 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-10", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_10(sku: str) -> CatalogItem | None:
    for item in ITEMS_10:
        if item.sku == sku:
            return item
    return None


def all_skus_10() -> list[str]:
    return [x.sku for x in ITEMS_10]


def validate_cost_10(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_10() -> dict:
    return {
        "partition": 10,
        "count": len(ITEMS_10),
        "categories": sorted({x.category for x in ITEMS_10}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_10) // max(1, len(ITEMS_10)),
    }
