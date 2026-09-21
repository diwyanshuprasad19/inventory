"""SKU catalog partition 43 — reference data for seed / validation."""

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


ITEMS_43: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT43-SKU-{j:03d}",
        name=f"Catalog 43 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][43 % 5],
        unit_cost_cents=100 + 43 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-43", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_43(sku: str) -> CatalogItem | None:
    for item in ITEMS_43:
        if item.sku == sku:
            return item
    return None


def all_skus_43() -> list[str]:
    return [x.sku for x in ITEMS_43]


def validate_cost_43(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_43() -> dict:
    return {
        "partition": 43,
        "count": len(ITEMS_43),
        "categories": sorted({x.category for x in ITEMS_43}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_43) // max(1, len(ITEMS_43)),
    }
