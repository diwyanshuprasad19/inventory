from inventory_app.catalog.sku_catalog_08 import all_skus_08, summarize_08, validate_cost_08


def test_catalog_08_size():
    assert len(all_skus_08()) == 40
    s = summarize_08()
    assert s["partition"] == 8
    assert s["count"] == 40


def test_catalog_08_cost():
    assert validate_cost_08(0)
    assert validate_cost_08(100)
    assert not validate_cost_08(-1)
