"""OpenAPI contract fragment 22 for inventory."""

CONTRACT_22 = {
    "id": "inv-22",
    "method": "POST",
    "path": "/v1/contract/22",
    "summary": "Contract endpoint 22",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-22-1",
        "case-22-2",
        "case-22-3",
        "case-22-4",
        "case-22-5",
        "case-22-6",
        "case-22-7",
        "case-22-8",
        "case-22-9",
        "case-22-10",
        "case-22-11",
        "case-22-12",
        "case-22-13",
        "case-22-14",
        "case-22-15",
        "case-22-16",
        "case-22-17",
        "case-22-18",
        "case-22-19"
    ],
}


def validate_request_22(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
