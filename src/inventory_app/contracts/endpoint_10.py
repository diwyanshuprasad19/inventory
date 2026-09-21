"""OpenAPI contract fragment 10 for inventory."""

CONTRACT_10 = {
    "id": "inv-10",
    "method": "POST",
    "path": "/v1/contract/10",
    "summary": "Contract endpoint 10",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-10-1",
        "case-10-2",
        "case-10-3",
        "case-10-4",
        "case-10-5",
        "case-10-6",
        "case-10-7",
        "case-10-8",
        "case-10-9",
        "case-10-10",
        "case-10-11",
        "case-10-12",
        "case-10-13",
        "case-10-14",
        "case-10-15",
        "case-10-16",
        "case-10-17",
        "case-10-18",
        "case-10-19"
    ],
}


def validate_request_10(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
