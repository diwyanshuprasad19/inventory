"""OpenAPI contract fragment 05 for inventory."""

CONTRACT_05 = {
    "id": "inv-05",
    "method": "PATCH",
    "path": "/v1/contract/05",
    "summary": "Contract endpoint 5",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-5-1",
        "case-5-2",
        "case-5-3",
        "case-5-4",
        "case-5-5",
        "case-5-6",
        "case-5-7",
        "case-5-8",
        "case-5-9",
        "case-5-10",
        "case-5-11",
        "case-5-12",
        "case-5-13",
        "case-5-14",
        "case-5-15",
        "case-5-16",
        "case-5-17",
        "case-5-18",
        "case-5-19"
    ],
}


def validate_request_05(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
