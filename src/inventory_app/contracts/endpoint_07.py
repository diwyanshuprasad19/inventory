"""OpenAPI contract fragment 07 for inventory."""

CONTRACT_07 = {
    "id": "inv-07",
    "method": "POST",
    "path": "/v1/contract/07",
    "summary": "Contract endpoint 7",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-7-1",
        "case-7-2",
        "case-7-3",
        "case-7-4",
        "case-7-5",
        "case-7-6",
        "case-7-7",
        "case-7-8",
        "case-7-9",
        "case-7-10",
        "case-7-11",
        "case-7-12",
        "case-7-13",
        "case-7-14",
        "case-7-15",
        "case-7-16",
        "case-7-17",
        "case-7-18",
        "case-7-19",
    ],
}


def validate_request_07(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
