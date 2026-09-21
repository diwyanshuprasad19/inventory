"""OpenAPI contract fragment 24 for inventory."""

CONTRACT_24 = {
    "id": "inv-24",
    "method": "GET",
    "path": "/v1/contract/24",
    "summary": "Contract endpoint 24",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-24-1",
        "case-24-2",
        "case-24-3",
        "case-24-4",
        "case-24-5",
        "case-24-6",
        "case-24-7",
        "case-24-8",
        "case-24-9",
        "case-24-10",
        "case-24-11",
        "case-24-12",
        "case-24-13",
        "case-24-14",
        "case-24-15",
        "case-24-16",
        "case-24-17",
        "case-24-18",
        "case-24-19"
    ],
}


def validate_request_24(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
