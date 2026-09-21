"""SKU catalog partition 46 — reference data for seed / validation."""

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


ITEMS_46: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT46-SKU-{j:03d}",
        name=f"Catalog 46 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][46 % 5],
        unit_cost_cents=100 + 46 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-46", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_46(sku: str) -> CatalogItem | None:
    for item in ITEMS_46:
        if item.sku == sku:
            return item
    return None


def all_skus_46() -> list[str]:
    return [x.sku for x in ITEMS_46]


def validate_cost_46(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_46() -> dict:
    return {
        "partition": 46,
        "count": len(ITEMS_46),
        "categories": sorted({x.category for x in ITEMS_46}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_46) // max(1, len(ITEMS_46)),
    }
