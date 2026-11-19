from flask import Blueprint, render_template, request, redirect, flash
import psycopg2
from app.database import obtener_conexion

bp = Blueprint("ordenes", __name__, url_prefix="/ordenes")


def validar_orden(form, meseros):
    try:
        mesa = int(form.get('numero_mesa', ''))
        if mesa <= 0:
            raise ValueError
    except ValueError:
        return None, 'El número de mesa debe ser mayor que cero.'

    estado = form.get('estado', '').strip()

    if not estado or len(estado) > 20:
        return None, 'El estado es obligatorio y máximo de 20 caracteres.'

    try:
        mesero = int(form.get('mesero_id', ''))
    except ValueError:
        mesero = None

    if not any(m[0] == mesero for m in meseros):
        return None, 'Selecciona un mesero existente.'

    return (mesa, estado, mesero), None


@bp.route('/', strict_slashes=False)
def listar_ordenes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT o.orden_id, o.numero_mesa, o.fecha_hora,
               o.estado, m.nombre
        FROM ordenes o
        LEFT JOIN meseros m ON o.mesero_id = m.mesero_id
        ORDER BY o.orden_id
    """)

    ordenes = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template('ordenes/ordenes.html', ordenes=ordenes)


@bp.route('/nueva', methods=['GET', 'POST'])
def nueva_orden():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT mesero_id, nombre FROM meseros")
    meseros = cursor.fetchall()

    if request.method == 'POST':
        datos, error = validar_orden(request.form, meseros)

        if error:
            flash(error, 'danger')
        else:
            try:
                cursor.execute("""
                    INSERT INTO ordenes
                    (numero_mesa, estado, mesero_id)
                    VALUES (%s, %s, %s)
                """, datos)

                conexion.commit()
                flash('Orden registrada correctamente.', 'success')
                cursor.close()
                conexion.close()
                return redirect('/ordenes')

            except psycopg2.Error:
                conexion.rollback()
                flash('Error al registrar la orden.', 'danger')

    cursor.close()
    conexion.close()

    return render_template('ordenes/nueva_orden.html',
                           meseros=meseros)


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_orden(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM ordenes WHERE orden_id = %s", (id,)
    )
    orden = cursor.fetchone()

    if not orden:
        cursor.close()
        conexion.close()
        flash('La orden no existe.', 'warning')
        return redirect('/ordenes')

    cursor.execute("SELECT mesero_id, nombre FROM meseros")
    meseros = cursor.fetchall()

    if request.method == 'POST':
        datos, error = validar_orden(request.form, meseros)

        orden_form = (
            id,
            request.form.get('numero_mesa', ''),
            orden[2],
            request.form.get('estado', ''),
            request.form.get('mesero_id', '')
        )

        if error:
            flash(error, 'danger')
        else:
            try:
                cursor.execute("""
                    UPDATE ordenes
                    SET numero_mesa = %s, estado = %s, mesero_id = %s
                    WHERE orden_id = %s
                """, datos + (id,))

                conexion.commit()
                flash('Orden actualizada correctamente.', 'success')
                cursor.close()
                conexion.close()
                return redirect('/ordenes')

            except psycopg2.Error:
                conexion.rollback()
                flash('Error al actualizar la orden.', 'danger')

        orden = orden_form

    cursor.close()
    conexion.close()

    return render_template('ordenes/editar_orden.html',
                           orden=orden, meseros=meseros)


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_orden(id):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM ordenes WHERE orden_id = %s", (id,)
        )

        if cursor.rowcount:
            conexion.commit()
            flash('Orden eliminada correctamente.', 'success')
        else:
            flash('La orden no existe.', 'warning')

    except psycopg2.errors.ForeignKeyViolation:
        conexion.rollback()
        flash('No se puede eliminar una orden que tiene detalles asociados.', 'danger')

    except psycopg2.Error:
        conexion.rollback()
        flash('Error al eliminar la orden.', 'danger')

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return redirect('/ordenes')
