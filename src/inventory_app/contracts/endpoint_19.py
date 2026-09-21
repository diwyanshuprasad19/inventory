"""OpenAPI contract fragment 19 for inventory."""

CONTRACT_19 = {
    "id": "inv-19",
    "method": "POST",
    "path": "/v1/contract/19",
    "summary": "Contract endpoint 19",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-19-1",
        "case-19-2",
        "case-19-3",
        "case-19-4",
        "case-19-5",
        "case-19-6",
        "case-19-7",
        "case-19-8",
        "case-19-9",
        "case-19-10",
        "case-19-11",
        "case-19-12",
        "case-19-13",
        "case-19-14",
        "case-19-15",
        "case-19-16",
        "case-19-17",
        "case-19-18",
        "case-19-19"
    ],
}


def validate_request_19(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
