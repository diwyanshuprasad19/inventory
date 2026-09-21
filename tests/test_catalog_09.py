from inventory_app.catalog.sku_catalog_09 import all_skus_09, summarize_09, validate_cost_09


def test_catalog_09_size():
    assert len(all_skus_09()) == 40
    s = summarize_09()
    assert s["partition"] == 9
    assert s["count"] == 40


def test_catalog_09_cost():
    assert validate_cost_09(0)
    assert validate_cost_09(100)
    assert not validate_cost_09(-1)
