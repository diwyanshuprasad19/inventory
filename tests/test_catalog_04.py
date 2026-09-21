from inventory_app.catalog.sku_catalog_04 import all_skus_04, summarize_04, validate_cost_04


def test_catalog_04_size():
    assert len(all_skus_04()) == 40
    s = summarize_04()
    assert s["partition"] == 4
    assert s["count"] == 40


def test_catalog_04_cost():
    assert validate_cost_04(0)
    assert validate_cost_04(100)
    assert not validate_cost_04(-1)
