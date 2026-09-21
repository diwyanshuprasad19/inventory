from inventory_app.catalog.sku_catalog_10 import (
    summarize_10, all_skus_10, validate_cost_10
)


def test_catalog_10_size():
    assert len(all_skus_10()) == 40
    s = summarize_10()
    assert s["partition"] == 10
    assert s["count"] == 40


def test_catalog_10_cost():
    assert validate_cost_10(0)
    assert validate_cost_10(100)
    assert not validate_cost_10(-1)
