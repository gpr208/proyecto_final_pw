## esta prueba verifica que la página responda correctamente con código 200
class CursorFalso:
    rowcount = 1

    def execute(self, consulta, parametros=None):
        self.consulta = consulta

    def fetchall(self):
        return []

    def close(self):
        pass


class ConexionFalsa:
    def cursor(self):
        return CursorFalso()

    def commit(self):
        pass

    def close(self):
        pass

def test_listar_categorias(client, monkeypatch):
    conexion = ConexionFalsa()

    monkeypatch.setattr(
        "app.routes.categorias.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.get("/categorias")

    assert respuesta.status_code == 200

## Probar la creación de categorías

def test_crear_categoria(client, monkeypatch):
    conexion = ConexionFalsa()

    monkeypatch.setattr(
        "app.routes.categorias.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/categorias/nueva",
        data={
            "nombre": "Bebidas",
            "descripcion": "Bebidas del establecimiento"
        },
        follow_redirects=False
    )

    assert respuesta.status_code == 302

## Probar la edición de categorías
def test_editar_categoria(client, monkeypatch):
    conexion = ConexionFalsa()

    monkeypatch.setattr(
        "app.routes.categorias.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/categorias/editar/1",
        data={
            "nombre": "Bebidas frías",
            "descripcion": "Bebidas para los clientes"
        },
        follow_redirects=False
    )

    assert respuesta.status_code == 302

### Probar la eliminación de categorías
def test_eliminar_categoria(client, monkeypatch):
    conexion = ConexionFalsa()

    monkeypatch.setattr(
        "app.routes.categorias.obtener_conexion",
        lambda: conexion
    )

    respuesta = client.post(
        "/categorias/eliminar/1",
        follow_redirects=False
    )

    assert respuesta.status_code == 302