"""OpenAPI contract fragment 02 for inventory."""

CONTRACT_02 = {
    "id": "inv-02",
    "method": "PATCH",
    "path": "/v1/contract/02",
    "summary": "Contract endpoint 2",
    "edge_cases": [
        "empty sku",
        "qty zero",
        "case-2-1",
        "case-2-2",
        "case-2-3",
        "case-2-4",
        "case-2-5",
        "case-2-6",
        "case-2-7",
        "case-2-8",
        "case-2-9",
        "case-2-10",
        "case-2-11",
        "case-2-12",
        "case-2-13",
        "case-2-14",
        "case-2-15",
        "case-2-16",
        "case-2-17",
        "case-2-18",
        "case-2-19"
    ],
}


def validate_request_02(payload: dict) -> list[str]:
    errors: list[str] = []
    if not payload.get("sku"):
        errors.append("sku required")
    qty = payload.get("qty", 1)
    if not isinstance(qty, int) or qty < 1:
        errors.append("qty must be positive int")
    return errors
