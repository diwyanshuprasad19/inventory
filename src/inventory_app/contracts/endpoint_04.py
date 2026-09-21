"""OpenAPI contract fragment 04 for inventory."""

CONTRACT_04 = {
    "id": "inv-04",
    "method": "POST",
    "path": "/v1/contract/04",
    "summary": "Contract endpoint 4",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-4-1",
        "case-4-2",
        "case-4-3",
        "case-4-4",
        "case-4-5",
        "case-4-6",
        "case-4-7",
        "case-4-8",
        "case-4-9",
        "case-4-10",
        "case-4-11",
        "case-4-12",
        "case-4-13",
        "case-4-14",
        "case-4-15",
        "case-4-16",
        "case-4-17",
        "case-4-18",
        "case-4-19",
    ],
}


def validate_request_04(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
