from inventory_app.catalog.sku_catalog_05 import all_skus_05, summarize_05, validate_cost_05


def test_catalog_05_size():
    assert len(all_skus_05()) == 40
    s = summarize_05()
    assert s["partition"] == 5
    assert s["count"] == 40


def test_catalog_05_cost():
    assert validate_cost_05(0)
    assert validate_cost_05(100)
    assert not validate_cost_05(-1)
