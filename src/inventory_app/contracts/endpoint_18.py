"""OpenAPI contract fragment 18 for inventory."""

CONTRACT_18 = {
    "id": "inv-18",
    "method": "GET",
    "path": "/v1/contract/18",
    "summary": "Contract endpoint 18",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-18-1",
        "case-18-2",
        "case-18-3",
        "case-18-4",
        "case-18-5",
        "case-18-6",
        "case-18-7",
        "case-18-8",
        "case-18-9",
        "case-18-10",
        "case-18-11",
        "case-18-12",
        "case-18-13",
        "case-18-14",
        "case-18-15",
        "case-18-16",
        "case-18-17",
        "case-18-18",
        "case-18-19",
    ],
}


def validate_request_18(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
