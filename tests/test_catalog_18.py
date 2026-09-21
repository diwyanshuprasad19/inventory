from inventory_app.catalog.sku_catalog_18 import (
    summarize_18, all_skus_18, validate_cost_18
)


def test_catalog_18_size():
    assert len(all_skus_18()) == 40
    s = summarize_18()
    assert s["partition"] == 18
    assert s["count"] == 40


def test_catalog_18_cost():
    assert validate_cost_18(0)
    assert validate_cost_18(100)
    assert not validate_cost_18(-1)
