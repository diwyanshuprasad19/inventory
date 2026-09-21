from inventory_app.catalog.sku_catalog_07 import all_skus_07, summarize_07, validate_cost_07


def test_catalog_07_size():
    assert len(all_skus_07()) == 40
    s = summarize_07()
    assert s["partition"] == 7
    assert s["count"] == 40


def test_catalog_07_cost():
    assert validate_cost_07(0)
    assert validate_cost_07(100)
    assert not validate_cost_07(-1)
