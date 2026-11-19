from flask import Blueprint, render_template, request, redirect, flash
from app.database import obtener_conexion
from decimal import Decimal, InvalidOperation

bp = Blueprint("detalles", __name__, url_prefix="/detalles")


@bp.route('/', strict_slashes=False)
def listar_detalles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT detalles_orden.detalle_id,
               ordenes.orden_id,
               productos.nombre,
               detalles_orden.cantidad,
               detalles_orden.precio_unitario
        FROM detalles_orden
        LEFT JOIN ordenes
        ON detalles_orden.orden_id = ordenes.orden_id
        LEFT JOIN productos
        ON detalles_orden.producto_id = productos.producto_id
        ORDER BY detalles_orden.detalle_id
    """)

    detalles = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('detalles/detalles.html', detalles=detalles)



@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_detalle():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT orden_id FROM ordenes ORDER BY orden_id")
    ordenes = cursor.fetchall()

    cursor.execute("SELECT producto_id, nombre, precio FROM productos ORDER BY nombre")
    productos = cursor.fetchall()

    if request.method == 'POST':
        orden_texto = request.form.get('orden_id', '').strip()
        producto_texto = request.form.get('producto_id', '').strip()
        cantidad_texto = request.form.get('cantidad', '').strip()
        precio_texto = request.form.get('precio_unitario', '').strip()

        # Validar orden
        try:
            orden_id = int(orden_texto)
        except ValueError:
            orden_id = None

        if not any(orden[0] == orden_id for orden in ordenes):
            flash('Debes seleccionar una orden existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/nuevo_detalle.html',
                ordenes=ordenes,
                productos=productos
            )

        # Validar producto
        try:
            producto_id = int(producto_texto)
        except ValueError:
            producto_id = None

        if not any(producto[0] == producto_id for producto in productos):
            flash('Debes seleccionar un producto existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/nuevo_detalle.html',
                ordenes=ordenes,
                productos=productos
            )

        # Validar cantidad
        try:
            cantidad = int(cantidad_texto)

            if cantidad <= 0 or cantidad > 2147483647:
                raise ValueError

        except ValueError:
            flash('La cantidad debe ser un entero entre 1 y 2147483647.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/nuevo_detalle.html',
                ordenes=ordenes,
                productos=productos
            )

        # Validar precio
        try:
            precio_unitario = Decimal(precio_texto)

            if (not precio_unitario.is_finite()
                    or precio_unitario <= 0
                    or precio_unitario > Decimal('99999999.99')
                    or precio_unitario.as_tuple().exponent < -2):
                raise ValueError

        except (InvalidOperation, ValueError):
            flash('El precio debe ser mayor que cero y no superar 99999999.99, con maximo dos decimales.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/nuevo_detalle.html',
                ordenes=ordenes,
                productos=productos
            )

        # Registrar detalle
        cursor.execute(
            """
            INSERT INTO detalles_orden
            (orden_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
            """,
            (orden_id, producto_id, cantidad, precio_unitario)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Detalle registrado correctamente.', 'success')
        return redirect('/detalles')

    cursor.close()
    conexion.close()

    return render_template(
        'detalles/nuevo_detalle.html',
        ordenes=ordenes,
        productos=productos
    )


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_detalle(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM detalles_orden WHERE detalle_id = %s",
        (id,)
    )
    detalle = cursor.fetchone()

    if not detalle:
        cursor.close()
        conexion.close()
        flash('El detalle que intentas editar no existe.', 'danger')
        return redirect('/detalles')

    cursor.execute("SELECT orden_id FROM ordenes ORDER BY orden_id")
    ordenes = cursor.fetchall()

    cursor.execute("SELECT producto_id, nombre FROM productos ORDER BY nombre")
    productos = cursor.fetchall()

    if request.method == 'POST':
        orden_texto = request.form.get('orden_id', '').strip()
        producto_texto = request.form.get('producto_id', '').strip()
        cantidad_texto = request.form.get('cantidad', '').strip()
        precio_texto = request.form.get('precio_unitario', '').strip()

        try:
            orden_id = int(orden_texto)
        except ValueError:
            orden_id = None

        if not any(orden[0] == orden_id for orden in ordenes):
            flash('Debes seleccionar una orden existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/editar_detalle.html',
                detalle=(id, orden_texto, producto_texto, cantidad_texto, precio_texto),
                ordenes=ordenes,
                productos=productos
            )

        # Validar producto
        try:
            producto_id = int(producto_texto)
        except ValueError:
            producto_id = None

        if not any(producto[0] == producto_id for producto in productos):
            flash('Debes seleccionar un producto existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/editar_detalle.html',
                detalle=(id, orden_id, producto_texto, cantidad_texto, precio_texto),
                ordenes=ordenes,
                productos=productos
            )

                # Validar cantidad
        try:
            cantidad = int(cantidad_texto)

            if cantidad <= 0 or cantidad > 2147483647:
                raise ValueError

        except ValueError:
            flash('La cantidad debe ser un entero entre 1 y 2147483647.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/editar_detalle.html',
                detalle=(id, orden_id, producto_id, cantidad_texto, precio_texto),
                ordenes=ordenes,
                productos=productos
            )

        # Validar precio
        try:
            precio_unitario = Decimal(precio_texto)

            if (not precio_unitario.is_finite()
                    or precio_unitario <= 0
                    or precio_unitario > Decimal('99999999.99')
                    or precio_unitario.as_tuple().exponent < -2):
                raise ValueError

        except (InvalidOperation, ValueError):
            flash('El precio debe ser mayor que cero y no superar 99999999.99, con maximo dos decimales.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'detalles/editar_detalle.html',
                detalle=(id, orden_id, producto_id, cantidad_texto, precio_texto),
                ordenes=ordenes,
                productos=productos
            )

        cursor.execute(
            """
            UPDATE detalles_orden
            SET orden_id = %s,
                producto_id = %s,
                cantidad = %s,
                precio_unitario = %s
            WHERE detalle_id = %s
            """,
            (orden_id, producto_id, cantidad, precio_unitario, id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Detalle actualizado correctamente.', 'success')
        return redirect('/detalles')

    cursor.close()
    conexion.close()

    return render_template(
        'detalles/editar_detalle.html',
        detalle=detalle,
        ordenes=ordenes,
        productos=productos
    )


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_detalle(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM detalles_orden WHERE detalle_id = %s",
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/detalles')
