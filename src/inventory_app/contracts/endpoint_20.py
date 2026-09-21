"""OpenAPI contract fragment 20 for inventory."""

CONTRACT_20 = {
    "id": "inv-20",
    "method": "PATCH",
    "path": "/v1/contract/20",
    "summary": "Contract endpoint 20",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-20-1",
        "case-20-2",
        "case-20-3",
        "case-20-4",
        "case-20-5",
        "case-20-6",
        "case-20-7",
        "case-20-8",
        "case-20-9",
        "case-20-10",
        "case-20-11",
        "case-20-12",
        "case-20-13",
        "case-20-14",
        "case-20-15",
        "case-20-16",
        "case-20-17",
        "case-20-18",
        "case-20-19"
    ],
}


def validate_request_20(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
