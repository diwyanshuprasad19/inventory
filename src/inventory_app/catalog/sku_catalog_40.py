"""SKU catalog partition 40 — reference data for seed / validation."""

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


ITEMS_40: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT40-SKU-{j:03d}",
        name=f"Catalog 40 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][40 % 5],
        unit_cost_cents=100 + 40 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-40", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_40(sku: str) -> CatalogItem | None:
    for item in ITEMS_40:
        if item.sku == sku:
            return item
    return None


def all_skus_40() -> list[str]:
    return [x.sku for x in ITEMS_40]


def validate_cost_40(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_40() -> dict:
    return {
        "partition": 40,
        "count": len(ITEMS_40),
        "categories": sorted({x.category for x in ITEMS_40}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_40) // max(1, len(ITEMS_40)),
    }
