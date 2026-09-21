"""SKU catalog partition 19 — reference data for seed / validation."""

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


ITEMS_19: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT19-SKU-{j:03d}",
        name=f"Catalog 19 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][19 % 5],
        unit_cost_cents=100 + 19 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-19", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_19(sku: str) -> CatalogItem | None:
    for item in ITEMS_19:
        if item.sku == sku:
            return item
    return None


def all_skus_19() -> list[str]:
    return [x.sku for x in ITEMS_19]


def validate_cost_19(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_19() -> dict:
    return {
        "partition": 19,
        "count": len(ITEMS_19),
        "categories": sorted({x.category for x in ITEMS_19}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_19) // max(1, len(ITEMS_19)),
    }
