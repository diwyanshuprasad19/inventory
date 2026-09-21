from inventory_app.catalog.sku_catalog_12 import all_skus_12, summarize_12, validate_cost_12


def test_catalog_12_size():
    assert len(all_skus_12()) == 40
    s = summarize_12()
    assert s["partition"] == 12
    assert s["count"] == 40


def test_catalog_12_cost():
    assert validate_cost_12(0)
    assert validate_cost_12(100)
    assert not validate_cost_12(-1)
