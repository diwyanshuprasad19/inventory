from inventory_app.catalog.sku_catalog_01 import all_skus_01, summarize_01, validate_cost_01


def test_catalog_01_size():
    assert len(all_skus_01()) == 40
    s = summarize_01()
    assert s["partition"] == 1
    assert s["count"] == 40


def test_catalog_01_cost():
    assert validate_cost_01(0)
    assert validate_cost_01(100)
    assert not validate_cost_01(-1)
