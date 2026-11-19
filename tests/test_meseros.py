## valida que los meseros tengan si o si nombre
class CursorMeserosFalso:
    def execute(self, consulta, parametros=None):
        self.consulta = consulta

    def fetchall(self):
        return []

    def close(self):
        pass


class ConexionMeserosFalsa:
    def cursor(self):
        return CursorMeserosFalso()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


def test_listar_meseros(client, monkeypatch):
    conexion = ConexionMeserosFalsa()

    monkeypatch.setattr(
        "app.routes.meseros.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.get("/meseros")

    assert respuesta.status_code == 200


def test_crear_mesero(client, monkeypatch):
    conexion = ConexionMeserosFalsa()

    monkeypatch.setattr(
        "app.routes.meseros.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/meseros/nuevo",
        data={
            "nombre": "Carlos",
            "telefono": "3001234567",
            "fecha": "2026-11-19"
        },
        follow_redirects=False
    )

    assert respuesta.status_code == 302


def test_rechazar_mesero_sin_nombre(client):
    respuesta = client.post(
        "/meseros/nuevo",
        data={
            "nombre": "",
            "telefono": "3001234567",
            "fecha": "2026-11-19"
        }
    )

    assert respuesta.status_code == 200