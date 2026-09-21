from inventory_app.catalog.sku_catalog_03 import all_skus_03, summarize_03, validate_cost_03


def test_catalog_03_size():
    assert len(all_skus_03()) == 40
    s = summarize_03()
    assert s["partition"] == 3
    assert s["count"] == 40


def test_catalog_03_cost():
    assert validate_cost_03(0)
    assert validate_cost_03(100)
    assert not validate_cost_03(-1)
