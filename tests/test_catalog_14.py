from inventory_app.catalog.sku_catalog_14 import (
    summarize_14, all_skus_14, validate_cost_14
)


def test_catalog_14_size():
    assert len(all_skus_14()) == 40
    s = summarize_14()
    assert s["partition"] == 14
    assert s["count"] == 40


def test_catalog_14_cost():
    assert validate_cost_14(0)
    assert validate_cost_14(100)
    assert not validate_cost_14(-1)
