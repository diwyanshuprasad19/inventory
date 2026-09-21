"""OpenAPI contract fragment 15 for inventory."""

CONTRACT_15 = {
    "id": "inv-15",
    "method": "GET",
    "path": "/v1/contract/15",
    "summary": "Contract endpoint 15",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-15-1",
        "case-15-2",
        "case-15-3",
        "case-15-4",
        "case-15-5",
        "case-15-6",
        "case-15-7",
        "case-15-8",
        "case-15-9",
        "case-15-10",
        "case-15-11",
        "case-15-12",
        "case-15-13",
        "case-15-14",
        "case-15-15",
        "case-15-16",
        "case-15-17",
        "case-15-18",
        "case-15-19"
    ],
}


def validate_request_15(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
