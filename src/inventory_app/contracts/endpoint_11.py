"""OpenAPI contract fragment 11 for inventory."""

CONTRACT_11 = {
    "id": "inv-11",
    "method": "PATCH",
    "path": "/v1/contract/11",
    "summary": "Contract endpoint 11",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-11-1",
        "case-11-2",
        "case-11-3",
        "case-11-4",
        "case-11-5",
        "case-11-6",
        "case-11-7",
        "case-11-8",
        "case-11-9",
        "case-11-10",
        "case-11-11",
        "case-11-12",
        "case-11-13",
        "case-11-14",
        "case-11-15",
        "case-11-16",
        "case-11-17",
        "case-11-18",
        "case-11-19"
    ],
}


def validate_request_11(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
