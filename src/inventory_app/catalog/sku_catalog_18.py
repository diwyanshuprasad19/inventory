"""SKU catalog partition 18 — reference data for seed / validation."""

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


ITEMS_18: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT18-SKU-{j:03d}",
        name=f"Catalog 18 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][18 % 5],
        unit_cost_cents=100 + 18 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-18", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_18(sku: str) -> CatalogItem | None:
    for item in ITEMS_18:
        if item.sku == sku:
            return item
    return None


def all_skus_18() -> list[str]:
    return [x.sku for x in ITEMS_18]


def validate_cost_18(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_18() -> dict:
    return {
        "partition": 18,
        "count": len(ITEMS_18),
        "categories": sorted({x.category for x in ITEMS_18}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_18) // max(1, len(ITEMS_18)),
    }
