from inventory_app.catalog.sku_catalog_20 import all_skus_20, summarize_20, validate_cost_20


def test_catalog_20_size():
    assert len(all_skus_20()) == 40
    s = summarize_20()
    assert s["partition"] == 20
    assert s["count"] == 40


def test_catalog_20_cost():
    assert validate_cost_20(0)
    assert validate_cost_20(100)
    assert not validate_cost_20(-1)
