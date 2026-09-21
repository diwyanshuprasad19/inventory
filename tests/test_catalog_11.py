from inventory_app.catalog.sku_catalog_11 import all_skus_11, summarize_11, validate_cost_11


def test_catalog_11_size():
    assert len(all_skus_11()) == 40
    s = summarize_11()
    assert s["partition"] == 11
    assert s["count"] == 40


def test_catalog_11_cost():
    assert validate_cost_11(0)
    assert validate_cost_11(100)
    assert not validate_cost_11(-1)
