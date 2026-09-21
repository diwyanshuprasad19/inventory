from inventory_app.catalog.sku_catalog_02 import all_skus_02, summarize_02, validate_cost_02


def test_catalog_02_size():
    assert len(all_skus_02()) == 40
    s = summarize_02()
    assert s["partition"] == 2
    assert s["count"] == 40


def test_catalog_02_cost():
    assert validate_cost_02(0)
    assert validate_cost_02(100)
    assert not validate_cost_02(-1)
