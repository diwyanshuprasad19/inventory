from inventory_app.catalog.sku_catalog_13 import all_skus_13, summarize_13, validate_cost_13


def test_catalog_13_size():
    assert len(all_skus_13()) == 40
    s = summarize_13()
    assert s["partition"] == 13
    assert s["count"] == 40


def test_catalog_13_cost():
    assert validate_cost_13(0)
    assert validate_cost_13(100)
    assert not validate_cost_13(-1)
