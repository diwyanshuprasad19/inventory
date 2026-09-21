"""OpenAPI contract fragment 21 for inventory."""

CONTRACT_21 = {
    "id": "inv-21",
    "method": "GET",
    "path": "/v1/contract/21",
    "summary": "Contract endpoint 21",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-21-1",
        "case-21-2",
        "case-21-3",
        "case-21-4",
        "case-21-5",
        "case-21-6",
        "case-21-7",
        "case-21-8",
        "case-21-9",
        "case-21-10",
        "case-21-11",
        "case-21-12",
        "case-21-13",
        "case-21-14",
        "case-21-15",
        "case-21-16",
        "case-21-17",
        "case-21-18",
        "case-21-19"
    ],
}


def validate_request_21(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
