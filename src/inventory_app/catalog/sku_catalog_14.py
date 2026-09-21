"""SKU catalog partition 14 — reference data for seed / validation."""

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


ITEMS_14: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT14-SKU-{j:03d}",
        name=f"Catalog 14 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][14 % 5],
        unit_cost_cents=100 + 14 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-14", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_14(sku: str) -> CatalogItem | None:
    for item in ITEMS_14:
        if item.sku == sku:
            return item
    return None


def all_skus_14() -> list[str]:
    return [x.sku for x in ITEMS_14]


def validate_cost_14(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_14() -> dict:
    return {
        "partition": 14,
        "count": len(ITEMS_14),
        "categories": sorted({x.category for x in ITEMS_14}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_14) // max(1, len(ITEMS_14)),
    }
