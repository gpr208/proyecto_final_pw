# Plan de pruebas - Proyecto bar

- Rama: documentacion-pruebas
- Servidor local: http://127.0.0.1:5000
- Fecha de ejecución: 20/11/2026
- Responsable de pruebas: miguel anel muñoz g

## 1. Pruebas automáticas (pytest)

- Comando: `python -m pytest -v`
- Resultado: 17 pruebas ejecutadas, 17 aprobadas
- Evidencia: `docs/resultado_pytest.txt` y `docs/evidencias/pytest_resultado.png`

## 2. Pruebas manuales en el navegador

| ID | Módulo | Caso de prueba | Pasos | Resultado esperado | Captura | Resultado real | Estado |
|----|--------|----------------|-------|--------------------|---------|----------------|--------|
| CP-01 | Inicio | Cargar la página principal | Abrir http://127.0.0.1:5000 | Carga la página y el menú sin errores | CP01_inicio.png | | aprobado |
| CP-02 | Categorías | Listar categorías | Entrar a Categorías (/categorias) | Se muestra la tabla con las categorías | CP02_listar_categorias.png | | aprobado |
| CP-03 | Categorías | Crear categoría | Pulsar el botón de nueva categoría, escribir el nombre "Prueba_Captura" y guardar | La categoría aparece en el listado | CP03_crear_categoria.png | | aprobado |
| CP-04 | Categorías | Editar categoría | Editar "Prueba_Captura", cambiar el nombre y guardar | El listado muestra el nombre nuevo | CP04_editar_categoria.png | | aprobado |
| CP-05 | Categorías | Eliminar categoría | Eliminar la categoría de prueba y confirmar | La categoría desaparece del listado | CP05_eliminar_categoria.png | | aprobado |
| CP-06 | Productos | Listar productos | Entrar a Productos (/productos) | Se muestra la tabla de productos | CP06_listar_productos.png | | aprobado |
| CP-07 | Productos | Crear producto | Pulsar nuevo producto, llenar los datos con un precio válido y guardar | El producto aparece en el listado | CP07_crear_producto.png | | aprobado |
| CP-08 | Productos | Rechazar precio inválido | Intentar guardar un producto con precio negativo o vacío | La app muestra un mensaje de error y no guarda | CP08_producto_precio_invalido.png | | aprobado |
| CP-09 | Meseros | Crear mesero | Entrar a Meseros, pulsar nuevo mesero, escribir un nombre y guardar | El mesero aparece en el listado | CP09_crear_mesero.png | | aprobado |
| CP-10 | Meseros | Rechazar mesero sin nombre | Intentar guardar un mesero dejando el nombre vacío | La app muestra un mensaje de error y no guarda | CP10_mesero_sin_nombre.png | | apronado |
| CP-11 | Órdenes | Listar órdenes | Entrar a Órdenes (/ordenes) | Se muestra la tabla de órdenes | CP11_listar_ordenes.png | | aprobado |
| CP-12 | Órdenes | Crear orden | Pulsar nueva orden, elegir mesa y mesero válidos y guardar | La orden aparece en el listado | CP12_crear_orden.png | | aprobado |
| CP-13 | Órdenes | Rechazar mesa inválida | Intentar crear una orden con una mesa inválida (vacía o inexistente) | La app muestra un mensaje de error y no guarda | CP13_orden_mesa_invalida.png | | fallido |
| CP-14 | Detalles | Crear detalle | Entrar a Detalles, agregar un producto con cantidad válida a una orden y guardar | El detalle aparece en el listado | CP14_crear_detalle.png | | aprobado |
| CP-15 | Detalles | Rechazar cantidad inválida | Intentar guardar un detalle con cantidad 0 o negativa | La app muestra un mensaje de error y no guarda | CP15_detalle_cantidad_invalida.png | | aprobado |

## 3. Observaciones

(arreglar lo de las mesas y servido)