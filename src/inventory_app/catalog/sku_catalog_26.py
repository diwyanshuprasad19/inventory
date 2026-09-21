"""SKU catalog partition 26 — reference data for seed / validation."""

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


ITEMS_26: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT26-SKU-{j:03d}",
        name=f"Catalog 26 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][26 % 5],
        unit_cost_cents=100 + 26 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-26", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_26(sku: str) -> CatalogItem | None:
    for item in ITEMS_26:
        if item.sku == sku:
            return item
    return None


def all_skus_26() -> list[str]:
    return [x.sku for x in ITEMS_26]


def validate_cost_26(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_26() -> dict:
    return {
        "partition": 26,
        "count": len(ITEMS_26),
        "categories": sorted({x.category for x in ITEMS_26}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_26) // max(1, len(ITEMS_26)),
    }
