"""SKU catalog partition 44 — reference data for seed / validation."""

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


ITEMS_44: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT44-SKU-{j:03d}",
        name=f"Catalog 44 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][44 % 5],
        unit_cost_cents=100 + 44 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=(f"part-44", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_44(sku: str) -> CatalogItem | None:
    for item in ITEMS_44:
        if item.sku == sku:
            return item
    return None


def all_skus_44() -> list[str]:
    return [x.sku for x in ITEMS_44]


def validate_cost_44(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_44() -> dict:
    return {
        "partition": 44,
        "count": len(ITEMS_44),
        "categories": sorted({x.category for x in ITEMS_44}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_44) // max(1, len(ITEMS_44)),
    }
