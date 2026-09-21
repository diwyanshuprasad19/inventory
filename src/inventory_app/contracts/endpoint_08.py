"""OpenAPI contract fragment 08 for inventory."""

CONTRACT_08 = {
    "id": "inv-08",
    "method": "PATCH",
    "path": "/v1/contract/08",
    "summary": "Contract endpoint 8",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-8-1",
        "case-8-2",
        "case-8-3",
        "case-8-4",
        "case-8-5",
        "case-8-6",
        "case-8-7",
        "case-8-8",
        "case-8-9",
        "case-8-10",
        "case-8-11",
        "case-8-12",
        "case-8-13",
        "case-8-14",
        "case-8-15",
        "case-8-16",
        "case-8-17",
        "case-8-18",
        "case-8-19",
    ],
}


def validate_request_08(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
