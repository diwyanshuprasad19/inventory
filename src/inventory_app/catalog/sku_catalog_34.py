"""SKU catalog partition 34 — reference data for seed / validation."""

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


ITEMS_34: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT34-SKU-{j:03d}",
        name=f"Catalog 34 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][34 % 5],
        unit_cost_cents=100 + 34 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-34", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_34(sku: str) -> CatalogItem | None:
    for item in ITEMS_34:
        if item.sku == sku:
            return item
    return None


def all_skus_34() -> list[str]:
    return [x.sku for x in ITEMS_34]


def validate_cost_34(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_34() -> dict:
    return {
        "partition": 34,
        "count": len(ITEMS_34),
        "categories": sorted({x.category for x in ITEMS_34}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_34) // max(1, len(ITEMS_34)),
    }
