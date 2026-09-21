from inventory_app.catalog.sku_catalog_17 import (
    summarize_17, all_skus_17, validate_cost_17
)


def test_catalog_17_size():
    assert len(all_skus_17()) == 40
    s = summarize_17()
    assert s["partition"] == 17
    assert s["count"] == 40


def test_catalog_17_cost():
    assert validate_cost_17(0)
    assert validate_cost_17(100)
    assert not validate_cost_17(-1)
