from fastapi.testclient import TestClient

import main

client = TestClient(main.app, raise_server_exceptions=False)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "online"


def test_version():
    assert client.get("/version").json()["version"] == "1.2.0"


def test_tareas_200_y_404():
    assert client.get("/tareas").status_code == 200
    assert client.get("/tareas/9999").status_code == 404
    assert client.get("/ruta-inexistente").status_code == 404


def test_crud():
    r = client.post("/tareas", json={"titulo": "Nueva"})
    assert r.status_code == 201
    tid = r.json()["id"]
    assert client.put(f"/tareas/{tid}", json={"titulo": "Editada", "completada": True}).json()["completada"]
    assert client.delete(f"/tareas/{tid}").status_code == 204
    assert client.get(f"/tareas/{tid}").status_code == 404


def test_config_check_no_revela_secreto():
    d = client.get("/config-check").json()
    assert "****" in d["prefijo_clave"] and len(d["prefijo_clave"]) == 8


def test_simular_error_corregido(monkeypatch):
    monkeypatch.delenv("SIMULAR_ERROR", raising=False)
    assert client.get("/simular-error").status_code == 400


def test_simular_error_500(monkeypatch):
    monkeypatch.setenv("SIMULAR_ERROR", "True")
    assert client.get("/simular-error").status_code == 500


def test_cors():
    r = client.get("/version", headers={"Origin": "https://miportafolio.vercel.app"})
    assert r.headers.get("access-control-allow-origin") in ("*", "https://miportafolio.vercel.app")
