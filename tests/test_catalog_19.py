from inventory_app.catalog.sku_catalog_19 import (
    summarize_19, all_skus_19, validate_cost_19
)


def test_catalog_19_size():
    assert len(all_skus_19()) == 40
    s = summarize_19()
    assert s["partition"] == 19
    assert s["count"] == 40


def test_catalog_19_cost():
    assert validate_cost_19(0)
    assert validate_cost_19(100)
    assert not validate_cost_19(-1)
