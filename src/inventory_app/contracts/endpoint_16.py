"""OpenAPI contract fragment 16 for inventory."""

CONTRACT_16 = {
    "id": "inv-16",
    "method": "POST",
    "path": "/v1/contract/16",
    "summary": "Contract endpoint 16",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-16-1",
        "case-16-2",
        "case-16-3",
        "case-16-4",
        "case-16-5",
        "case-16-6",
        "case-16-7",
        "case-16-8",
        "case-16-9",
        "case-16-10",
        "case-16-11",
        "case-16-12",
        "case-16-13",
        "case-16-14",
        "case-16-15",
        "case-16-16",
        "case-16-17",
        "case-16-18",
        "case-16-19",
    ],
}


def validate_request_16(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
