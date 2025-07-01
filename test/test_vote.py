from datetime import datetime, timedelta

def test_create_election(client):
    start = datetime.utcnow()
    payload = {
        "title": "Elección Demo",
        "description": "Test election",
        "start_time": start.isoformat(),
        # pon un end_time futuro como string ISO
        "end_time": (start + timedelta(hours=1)).isoformat()
    }
    response = client.post("/vote/election", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_active"] is True
    assert "id" in data
