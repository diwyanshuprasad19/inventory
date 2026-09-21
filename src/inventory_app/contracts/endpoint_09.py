"""OpenAPI contract fragment 09 for inventory."""

CONTRACT_09 = {
    "id": "inv-09",
    "method": "GET",
    "path": "/v1/contract/09",
    "summary": "Contract endpoint 9",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-9-1",
        "case-9-2",
        "case-9-3",
        "case-9-4",
        "case-9-5",
        "case-9-6",
        "case-9-7",
        "case-9-8",
        "case-9-9",
        "case-9-10",
        "case-9-11",
        "case-9-12",
        "case-9-13",
        "case-9-14",
        "case-9-15",
        "case-9-16",
        "case-9-17",
        "case-9-18",
        "case-9-19"
    ],
}


def validate_request_09(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
