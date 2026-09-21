from inventory_app.catalog.sku_catalog_06 import all_skus_06, summarize_06, validate_cost_06


def test_catalog_06_size():
    assert len(all_skus_06()) == 40
    s = summarize_06()
    assert s["partition"] == 6
    assert s["count"] == 40


def test_catalog_06_cost():
    assert validate_cost_06(0)
    assert validate_cost_06(100)
    assert not validate_cost_06(-1)
