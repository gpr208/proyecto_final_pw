## Listado: que podamos consultar las órdenes.
##Registro: que podamos registrar una orden con mesa, estado y mesero válidos.
##validación: que el sistema rechace una orden con número de mesa igual a cero.
class CursorOrdenesFalso:
    def execute(self, consulta, parametros=None):
        self.consulta = consulta

    def fetchall(self):
        if "SELECT mesero_id, nombre FROM meseros" in self.consulta:
            return [(1, "Carlos")]

        return []

    def close(self):
        pass


class ConexionOrdenesFalsa:
    def cursor(self):
        return CursorOrdenesFalso()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


def test_listar_ordenes(client, monkeypatch):
    conexion = ConexionOrdenesFalsa()

    monkeypatch.setattr(
        "app.routes.ordenes.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.get("/ordenes")

    assert respuesta.status_code == 200


def test_crear_orden(client, monkeypatch):
    conexion = ConexionOrdenesFalsa()

    monkeypatch.setattr(
        "app.routes.ordenes.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/ordenes/nueva",
        data={
            "numero_mesa": "5",
            "estado": "Abierta",
            "mesero_id": "1"
        },
        follow_redirects=False
    )

    assert respuesta.status_code == 302


def test_rechazar_orden_mesa_invalida(client, monkeypatch):
    conexion = ConexionOrdenesFalsa()

    monkeypatch.setattr(
        "app.routes.ordenes.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/ordenes/nueva",
        data={
            "numero_mesa": "0",
            "estado": "Abierta",
            "mesero_id": "1"
        }
    )

    assert respuesta.status_code == 200