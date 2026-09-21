"""OpenAPI contract fragment 03 for inventory."""

CONTRACT_03 = {
    "id": "inv-03",
    "method": "GET",
    "path": "/v1/contract/03",
    "summary": "Contract endpoint 3",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-3-1",
        "case-3-2",
        "case-3-3",
        "case-3-4",
        "case-3-5",
        "case-3-6",
        "case-3-7",
        "case-3-8",
        "case-3-9",
        "case-3-10",
        "case-3-11",
        "case-3-12",
        "case-3-13",
        "case-3-14",
        "case-3-15",
        "case-3-16",
        "case-3-17",
        "case-3-18",
        "case-3-19"
    ],
}


def validate_request_03(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
