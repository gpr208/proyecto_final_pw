## Comprobar que se rechacen productos inválidos
class CursorProductosFalso:
    rowcount = 1

    def execute(self, consulta, parametros=None):
        self.consulta = consulta

    def fetchall(self):
        if "SELECT categoria_id, nombre FROM categorias" in self.consulta:
            return [(1, "Bebidas")]

        return []

    def close(self):
        pass


class ConexionProductosFalsa:
    def cursor(self):
        return CursorProductosFalso()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


def test_listar_productos(client, monkeypatch):
    conexion = ConexionProductosFalsa()

    monkeypatch.setattr(
        "app.routes.productos.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.get("/productos")

    assert respuesta.status_code == 200


def test_crear_producto(client, monkeypatch):
    conexion = ConexionProductosFalsa()

    monkeypatch.setattr(
        "app.routes.productos.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/productos/nuevo",
        data={
            "nombre": "Agua",
            "precio": "3000",
            "stock": "20",
            "categoria_id": "1"
        },
        follow_redirects=False
    )

    assert respuesta.status_code == 302


def test_rechazar_producto_precio_invalido(client, monkeypatch):
    conexion = ConexionProductosFalsa()

    monkeypatch.setattr(
        "app.routes.productos.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/productos/nuevo",
        data={
            "nombre": "Agua",
            "precio": "0",
            "stock": "20",
            "categoria_id": "1"
        }
    )

    assert respuesta.status_code == 200