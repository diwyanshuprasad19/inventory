"""OpenAPI contract fragment 14 for inventory."""

CONTRACT_14 = {
    "id": "inv-14",
    "method": "PATCH",
    "path": "/v1/contract/14",
    "summary": "Contract endpoint 14",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-14-1",
        "case-14-2",
        "case-14-3",
        "case-14-4",
        "case-14-5",
        "case-14-6",
        "case-14-7",
        "case-14-8",
        "case-14-9",
        "case-14-10",
        "case-14-11",
        "case-14-12",
        "case-14-13",
        "case-14-14",
        "case-14-15",
        "case-14-16",
        "case-14-17",
        "case-14-18",
        "case-14-19",
    ],
}


def validate_request_14(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
