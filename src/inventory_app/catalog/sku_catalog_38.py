"""SKU catalog partition 38 — reference data for seed / validation."""

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


ITEMS_38: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT38-SKU-{j:03d}",
        name=f"Catalog 38 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][38 % 5],
        unit_cost_cents=100 + 38 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-38", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_38(sku: str) -> CatalogItem | None:
    for item in ITEMS_38:
        if item.sku == sku:
            return item
    return None


def all_skus_38() -> list[str]:
    return [x.sku for x in ITEMS_38]


def validate_cost_38(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_38() -> dict:
    return {
        "partition": 38,
        "count": len(ITEMS_38),
        "categories": sorted({x.category for x in ITEMS_38}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_38) // max(1, len(ITEMS_38)),
    }
