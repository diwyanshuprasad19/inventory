"""OpenAPI contract fragment 23 for inventory."""

CONTRACT_23 = {
    "id": "inv-23",
    "method": "PATCH",
    "path": "/v1/contract/23",
    "summary": "Contract endpoint 23",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-23-1",
        "case-23-2",
        "case-23-3",
        "case-23-4",
        "case-23-5",
        "case-23-6",
        "case-23-7",
        "case-23-8",
        "case-23-9",
        "case-23-10",
        "case-23-11",
        "case-23-12",
        "case-23-13",
        "case-23-14",
        "case-23-15",
        "case-23-16",
        "case-23-17",
        "case-23-18",
        "case-23-19"
    ],
}


def validate_request_23(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
