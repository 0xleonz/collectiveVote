from datetime import datetime

def test_create_election(client):
    payload = {
        "title": "Elección Demo",
        "description": "Test election",
        "start_time": datetime.utcnow().isoformat(),
        "end_time": None
    }
    response = client.post("/vote/election", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_active"] is True
    assert "id" in data

