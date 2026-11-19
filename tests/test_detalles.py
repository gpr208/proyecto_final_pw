## Listado: que podamos consultar los detalles de las órdenes.
##Registro: que podamos agregar un producto a una orden con cantidad y precio válidos.
##Validación: que el sistema rechace una cantidad igual a cero.

class CursorDetallesFalso:
    def execute(self, consulta, parametros=None):
        self.consulta = consulta

    def fetchall(self):
        if "SELECT orden_id FROM ordenes" in self.consulta:
            return [(1,)]

        if "SELECT producto_id, nombre FROM productos" in self.consulta:
            return [(1, "Agua")]

        return []

    def close(self):
        pass


class ConexionDetallesFalsa:
    def cursor(self):
        return CursorDetallesFalso()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


def test_listar_detalles(client, monkeypatch):
    conexion = ConexionDetallesFalsa()

    monkeypatch.setattr(
        "app.routes.detalles.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.get("/detalles")

    assert respuesta.status_code == 200


def test_crear_detalle(client, monkeypatch):
    conexion = ConexionDetallesFalsa()

    monkeypatch.setattr(
        "app.routes.detalles.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/detalles/nuevo",
        data={
            "orden_id": "1",
            "producto_id": "1",
            "cantidad": "2",
            "precio_unitario": "3000"
        },
        follow_redirects=False
    )

    assert respuesta.status_code == 302


def test_rechazar_detalle_cantidad_invalida(client, monkeypatch):
    conexion = ConexionDetallesFalsa()

    monkeypatch.setattr(
        "app.routes.detalles.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/detalles/nuevo",
        data={
            "orden_id": "1",
            "producto_id": "1",
            "cantidad": "0",
            "precio_unitario": "3000"
        }
    )

    assert respuesta.status_code == 200