"""OpenAPI contract fragment 01 for inventory."""

CONTRACT_01 = {
    "id": "inv-01",
    "method": "POST",
    "path": "/v1/contract/01",
    "summary": "Contract endpoint 1",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-1-1",
        "case-1-2",
        "case-1-3",
        "case-1-4",
        "case-1-5",
        "case-1-6",
        "case-1-7",
        "case-1-8",
        "case-1-9",
        "case-1-10",
        "case-1-11",
        "case-1-12",
        "case-1-13",
        "case-1-14",
        "case-1-15",
        "case-1-16",
        "case-1-17",
        "case-1-18",
        "case-1-19",
    ],
}


def validate_request_01(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
