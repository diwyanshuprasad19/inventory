"""SKU catalog partition 41 — reference data for seed / validation."""

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


ITEMS_41: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT41-SKU-{j:03d}",
        name=f"Catalog 41 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][41 % 5],
        unit_cost_cents=100 + 41 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-41", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_41(sku: str) -> CatalogItem | None:
    for item in ITEMS_41:
        if item.sku == sku:
            return item
    return None


def all_skus_41() -> list[str]:
    return [x.sku for x in ITEMS_41]


def validate_cost_41(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_41() -> dict:
    return {
        "partition": 41,
        "count": len(ITEMS_41),
        "categories": sorted({x.category for x in ITEMS_41}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_41) // max(1, len(ITEMS_41)),
    }
