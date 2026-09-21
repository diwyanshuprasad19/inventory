from inventory_app.catalog.sku_catalog_15 import all_skus_15, summarize_15, validate_cost_15


def test_catalog_15_size():
    assert len(all_skus_15()) == 40
    s = summarize_15()
    assert s["partition"] == 15
    assert s["count"] == 40


def test_catalog_15_cost():
    assert validate_cost_15(0)
    assert validate_cost_15(100)
    assert not validate_cost_15(-1)
