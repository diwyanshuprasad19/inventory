"""OpenAPI contract fragment 06 for inventory."""

CONTRACT_06 = {
    "id": "inv-06",
    "method": "GET",
    "path": "/v1/contract/06",
    "summary": "Contract endpoint 6",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-6-1",
        "case-6-2",
        "case-6-3",
        "case-6-4",
        "case-6-5",
        "case-6-6",
        "case-6-7",
        "case-6-8",
        "case-6-9",
        "case-6-10",
        "case-6-11",
        "case-6-12",
        "case-6-13",
        "case-6-14",
        "case-6-15",
        "case-6-16",
        "case-6-17",
        "case-6-18",
        "case-6-19",
    ],
}


def validate_request_06(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
