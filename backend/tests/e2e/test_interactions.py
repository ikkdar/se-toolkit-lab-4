"""End-to-end tests for the GET /interactions endpoint."""
import httpx


def test_get_interactions_returns_200(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_items_have_expected_fields(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    data = response.json()
    assert len(data) > 0
    assert "id" in data[0]
    assert "item_id" in data[0]
    assert "created_at" in data[0]


def test_get_interactions_filter_includes_boundary(client: httpx.Client) -> None:
    response = client.get("/interactions/?max_item_id=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(item["item_id"] <= 1 for item in data)

def test_get_interactions_response_structure(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if data:
        item = data[0]
        # Ожидаемые поля из реального ответа API
        expected_fields = {"id", "learner_id", "item_id", "kind", "created_at"}
        assert expected_fields.issubset(item.keys()), f"Missing fields: {expected_fields - item.keys()}"