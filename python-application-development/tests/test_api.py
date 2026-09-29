import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import app

def test_home():
    client = app.test_client()
    assert client.get("/").status_code == 200

def test_create_user_validation():
    client = app.test_client()
    assert client.post("/users", json={}).status_code == 400
