"""OpenAPI contract fragment 13 for inventory."""

CONTRACT_13 = {
    "id": "inv-13",
    "method": "POST",
    "path": "/v1/contract/13",
    "summary": "Contract endpoint 13",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-13-1",
        "case-13-2",
        "case-13-3",
        "case-13-4",
        "case-13-5",
        "case-13-6",
        "case-13-7",
        "case-13-8",
        "case-13-9",
        "case-13-10",
        "case-13-11",
        "case-13-12",
        "case-13-13",
        "case-13-14",
        "case-13-15",
        "case-13-16",
        "case-13-17",
        "case-13-18",
        "case-13-19",
    ],
}


def validate_request_13(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
