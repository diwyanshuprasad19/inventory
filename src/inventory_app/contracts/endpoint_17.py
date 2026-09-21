"""OpenAPI contract fragment 17 for inventory."""

CONTRACT_17 = {
    "id": "inv-17",
    "method": "PATCH",
    "path": "/v1/contract/17",
    "summary": "Contract endpoint 17",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-17-1",
        "case-17-2",
        "case-17-3",
        "case-17-4",
        "case-17-5",
        "case-17-6",
        "case-17-7",
        "case-17-8",
        "case-17-9",
        "case-17-10",
        "case-17-11",
        "case-17-12",
        "case-17-13",
        "case-17-14",
        "case-17-15",
        "case-17-16",
        "case-17-17",
        "case-17-18",
        "case-17-19",
    ],
}


def validate_request_17(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
