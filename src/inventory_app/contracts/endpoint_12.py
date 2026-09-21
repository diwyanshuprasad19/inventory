"""OpenAPI contract fragment 12 for inventory."""

CONTRACT_12 = {
    "id": "inv-12",
    "method": "GET",
    "path": "/v1/contract/12",
    "summary": "Contract endpoint 12",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-12-1",
        "case-12-2",
        "case-12-3",
        "case-12-4",
        "case-12-5",
        "case-12-6",
        "case-12-7",
        "case-12-8",
        "case-12-9",
        "case-12-10",
        "case-12-11",
        "case-12-12",
        "case-12-13",
        "case-12-14",
        "case-12-15",
        "case-12-16",
        "case-12-17",
        "case-12-18",
        "case-12-19"
    ],
}


def validate_request_12(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
