"""In-memory stock store with edge-case validation."""

from __future__ import annotations

from dataclasses import dataclass


class StockError(ValueError):
    pass


@dataclass
class StockItem:
    sku: str
    quantity: int
    reserved: int = 0

    @property
    def available(self) -> int:
        return max(0, self.quantity - self.reserved)


class InventoryStore:
    def __init__(self) -> None:
        self._items: dict[str, StockItem] = {
            "sku-100": StockItem("sku-100", 50),
            "sku-200": StockItem("sku-200", 0),
            "sku-300": StockItem("sku-300", 10, reserved=10),
        }

    def get(self, sku: str) -> StockItem:
        item = self._items.get(sku)
        if item is None:
            raise StockError(f"unknown sku: {sku}")
        return item

    def reserve(self, sku: str, qty: int) -> StockItem:
        if qty <= 0:
            raise StockError("qty must be > 0")
        item = self.get(sku)
        if item.available < qty:
            raise StockError(f"insufficient stock for {sku}: available={item.available}")
        item.reserved += qty
        return item

    def release(self, sku: str, qty: int) -> StockItem:
        if qty <= 0:
            raise StockError("qty must be > 0")
        item = self.get(sku)
        item.reserved = max(0, item.reserved - qty)
        return item
