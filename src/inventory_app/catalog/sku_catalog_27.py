"""SKU catalog partition 27 — reference data for seed / validation."""

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


ITEMS_27: list[CatalogItem] = [
    CatalogItem(
        sku=f"CAT27-SKU-{j:03d}",
        name=f"Catalog 27 Item {j:03d}",
        category=["Electronics", "Home", "Sports", "Office", "Auto"][27 % 5],
        unit_cost_cents=100 + 27 * 10 + j * 3,
        default_qty=10 + (j % 50),
        tags=("part-27", f"batch-{j}", "demo"),
    )
    for j in range(1, 41)
]


def lookup_27(sku: str) -> CatalogItem | None:
    for item in ITEMS_27:
        if item.sku == sku:
            return item
    return None


def all_skus_27() -> list[str]:
    return [x.sku for x in ITEMS_27]


def validate_cost_27(cents: int) -> bool:
    return 0 <= cents <= 10_000_000


def summarize_27() -> dict:
    return {
        "partition": 27,
        "count": len(ITEMS_27),
        "categories": sorted({x.category for x in ITEMS_27}),
        "avg_cost": sum(x.unit_cost_cents for x in ITEMS_27) // max(1, len(ITEMS_27)),
    }
