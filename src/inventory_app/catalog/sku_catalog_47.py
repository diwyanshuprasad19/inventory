"""SKU catalog partition 47 — reference data for seed / validation."""

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


ITEMS_47: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT47-SKU-{j:03d}",
        name=f"Catalog 47 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][47 % 5],
        unit_cost_cents=100 + 47 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-47", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_47(sku: str) -> CatalogItem | None:
    for item in ITEMS_47:
        if item.sku == sku:
            return item
    return None


def all_skus_47() -> list[str]:
    return [x.sku for x in ITEMS_47]


def validate_cost_47(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_47() -> dict:
    return {
        "partition": 47,
        "count": len(ITEMS_47),
        "categories": sorted({x.category for x in ITEMS_47}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_47) // max(1, len(ITEMS_47)),
    }
