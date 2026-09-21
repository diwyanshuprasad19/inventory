"""SKU catalog partition 37 — reference data for seed / validation."""

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


ITEMS_37: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT37-SKU-{j:03d}",
        name=f"Catalog 37 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][37 % 5],
        unit_cost_cents=100 + 37 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-37", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_37(sku: str) -> CatalogItem | None:
    for item in ITEMS_37:
        if item.sku == sku:
            return item
    return None


def all_skus_37() -> list[str]:
    return [x.sku for x in ITEMS_37]


def validate_cost_37(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_37() -> dict:
    return {
        "partition": 37,
        "count": len(ITEMS_37),
        "categories": sorted({x.category for x in ITEMS_37}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_37) // max(1, len(ITEMS_37)),
    }
