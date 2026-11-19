from flask import Blueprint, render_template, request, redirect, flash
from decimal import Decimal, InvalidOperation
import psycopg2
from app.database import obtener_conexion

bp = Blueprint("detalles", __name__, url_prefix="/detalles")


def validar_detalle(form, ordenes, productos):
    try:
        orden = int(form.get('orden_id', ''))
    except ValueError:
        orden = None

    if not any(o[0] == orden for o in ordenes):
        return None, 'Selecciona una orden existente.'

    try:
        producto = int(form.get('producto_id', ''))
    except ValueError:
        producto = None

    if not any(p[0] == producto for p in productos):
        return None, 'Selecciona un producto existente.'

    try:
        cantidad = int(form.get('cantidad', ''))
        if cantidad <= 0 or cantidad > 2147483647:
            raise ValueError
    except ValueError:
        return None, 'La cantidad debe ser un entero positivo.'

    try:
        precio = Decimal(form.get('precio_unitario', ''))
        if (not precio.is_finite() or precio <= 0
                or precio > Decimal('99999999.99')
                or precio.as_tuple().exponent < -2):
            raise ValueError
    except (InvalidOperation, ValueError):
        return None, 'El precio debe ser positivo y tener máximo dos decimales.'

    return (orden, producto, cantidad, precio), None


@bp.route('/', strict_slashes=False)
def listar_detalles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT d.detalle_id, d.orden_id, p.nombre,
               d.cantidad, d.precio_unitario
        FROM detalles_orden d
        LEFT JOIN productos p ON d.producto_id = p.producto_id
        ORDER BY d.detalle_id
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

    cursor.execute("SELECT producto_id, nombre FROM productos ORDER BY nombre")
    productos = cursor.fetchall()

    if request.method == 'POST':
        datos, error = validar_detalle(request.form, ordenes, productos)

        if error:
            flash(error, 'danger')
        else:
            try:
                cursor.execute("""
                    INSERT INTO detalles_orden
                    (orden_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                """, datos)

                conexion.commit()
                flash('Detalle registrado correctamente.', 'success')
                cursor.close()
                conexion.close()
                return redirect('/detalles')

            except psycopg2.Error:
                conexion.rollback()
                flash('Error al registrar el detalle.', 'danger')

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
        flash('El detalle no existe.', 'warning')
        return redirect('/detalles')

    cursor.execute("SELECT orden_id FROM ordenes ORDER BY orden_id")
    ordenes = cursor.fetchall()

    cursor.execute("SELECT producto_id, nombre FROM productos ORDER BY nombre")
    productos = cursor.fetchall()

    if request.method == 'POST':
        datos, error = validar_detalle(request.form, ordenes, productos)

        detalle = (
            id,
            request.form.get('orden_id', ''),
            request.form.get('producto_id', ''),
            request.form.get('cantidad', ''),
            request.form.get('precio_unitario', '')
        )

        if error:
            flash(error, 'danger')
        else:
            try:
                cursor.execute("""
                    UPDATE detalles_orden
                    SET orden_id = %s, producto_id = %s,
                        cantidad = %s, precio_unitario = %s
                    WHERE detalle_id = %s
                """, datos + (id,))

                conexion.commit()
                flash('Detalle actualizado correctamente.', 'success')
                cursor.close()
                conexion.close()
                return redirect('/detalles')

            except psycopg2.Error:
                conexion.rollback()
                flash('Error al actualizar el detalle.', 'danger')

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

    try:
        cursor.execute(
            "DELETE FROM detalles_orden WHERE detalle_id = %s",
            (id,)
        )

        conexion.commit()
        flash('Detalle eliminado correctamente.', 'success')

    except psycopg2.Error:
        conexion.rollback()
        flash('Error al eliminar el detalle.', 'danger')

    finally:
        cursor.close()
        conexion.close()

    return redirect('/detalles')
