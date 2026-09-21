"""SKU catalog partition 08 — reference data for seed / validation."""

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


ITEMS_08: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT08-SKU-{j:03d}",
        name=f"Catalog 08 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][8 % 5],
        unit_cost_cents=100 + 8 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-8", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_08(sku: str) -> CatalogItem | None:
    for item in ITEMS_08:
        if item.sku == sku:
            return item
    return None


def all_skus_08() -> list[str]:
    return [x.sku for x in ITEMS_08]


def validate_cost_08(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_08() -> dict:
    return {
        "partition": 8,
        "count": len(ITEMS_08),
        "categories": sorted({x.category for x in ITEMS_08}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_08) // max(1, len(ITEMS_08)),
    }
