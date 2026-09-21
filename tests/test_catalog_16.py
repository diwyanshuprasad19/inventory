from inventory_app.catalog.sku_catalog_16 import all_skus_16, summarize_16, validate_cost_16


def test_catalog_16_size():
    assert len(all_skus_16()) == 40
    s = summarize_16()
    assert s["partition"] == 16
    assert s["count"] == 40


def test_catalog_16_cost():
    assert validate_cost_16(0)
    assert validate_cost_16(100)
    assert not validate_cost_16(-1)
