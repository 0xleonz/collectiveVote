# tests/test_auth_flow.py
from datetime import datetime

def test_auth_register_login_and_protected_route(client):
    # 1) Registro
    resp = client.post(
        "/auth/register",
        json={
            "username": "flowuser",
            "email": "flow@example.com",
            "password": "FlowPass123"
        }
    )
    assert resp.status_code == 200
    assert resp.json()["username"] == "flowuser"

    # 2) Login (note que es form-data)
    login = client.post(
        "/auth/login",
        data={
            "username": "flowuser",
            "password": "FlowPass123"
        }
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert token

    # 3) Ruta protegida
    protected = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert protected.status_code == 200
    assert protected.json()["email"] == "flow@example.com"

    # 4) Ahora prueba un endpoint de voto: crear elección
    create = client.post(
        "/vote/election",
        json={
            "title": "Flow Election",
            "description": "Testing protected",
            "start_time": datetime.utcnow().isoformat(),
            "end_time": (datetime.utcnow()).isoformat()
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create.status_code == 200
    data = create.json()
    assert data["title"] == "Flow Election"
