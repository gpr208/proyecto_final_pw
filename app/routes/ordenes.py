from flask import Blueprint, render_template, request, redirect, flash
from app.database import obtener_conexion

bp = Blueprint("ordenes", __name__, url_prefix="/ordenes")


@bp.route('/', strict_slashes=False)
def listar_ordenes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT ordenes.orden_id,
               ordenes.numero_mesa,
               ordenes.fecha_hora,
               ordenes.estado,
               meseros.nombre
        FROM ordenes
        LEFT JOIN meseros
        ON ordenes.mesero_id = meseros.mesero_id
        ORDER BY ordenes.orden_id
    """)

    ordenes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('ordenes/ordenes.html', ordenes=ordenes)


@bp.route('/nueva', methods=['GET', 'POST'])
def nueva_orden():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT mesero_id, nombre FROM meseros ORDER BY nombre"
    )
    meseros = cursor.fetchall()

    if request.method == 'POST':
        mesa_texto = request.form.get('numero_mesa', '').strip()
        estado = request.form.get('estado', '').strip()
        mesero_texto = request.form.get('mesero_id', '').strip()

        try:
            numero_mesa = int(mesa_texto)
            if numero_mesa <= 0:
                raise ValueError
        except ValueError:
            flash('El numero de mesa debe ser un entero mayor que cero.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('ordenes/nueva_orden.html', meseros=meseros)

        if not estado:
            flash('El estado de la orden es obligatorio.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('ordenes/nueva_orden.html', meseros=meseros)

        if len(estado) > 20:
            flash('El estado no puede superar los 20 caracteres.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('ordenes/nueva_orden.html', meseros=meseros)

        try:
            mesero_id = int(mesero_texto)
        except ValueError:
            mesero_id = None

        if not any(mesero[0] == mesero_id for mesero in meseros):
            flash('Debes seleccionar un mesero existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('ordenes/nueva_orden.html', meseros=meseros)

        # Registrar orden
        cursor.execute(
            """
            INSERT INTO ordenes (numero_mesa, estado, mesero_id)
            VALUES (%s, %s, %s)
            """,
            (numero_mesa, estado, mesero_id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Orden registrada correctamente.', 'success')
        return redirect('/ordenes')

    cursor.close()
    conexion.close()

    return render_template('ordenes/nueva_orden.html', meseros=meseros)



@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_orden(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM ordenes WHERE orden_id = %s",
        (id,)
    )
    orden = cursor.fetchone()

    if not orden:
        cursor.close()
        conexion.close()
        flash('La orden que intentas editar no existe.', 'danger')
        return redirect('/ordenes')

    cursor.execute(
        "SELECT mesero_id, nombre FROM meseros ORDER BY nombre"
    )
    meseros = cursor.fetchall()

    if request.method == 'POST':
        mesa_texto = request.form.get('numero_mesa', '').strip()
        estado = request.form.get('estado', '').strip()
        mesero_texto = request.form.get('mesero_id', '').strip()

        try:
            numero_mesa = int(mesa_texto)
            if numero_mesa <= 0:
                raise ValueError
        except ValueError:
            flash('El numero de mesa debe ser un entero mayor que cero.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'ordenes/editar_orden.html',
                orden=(id, mesa_texto, orden[2], estado, mesero_texto),
                meseros=meseros
            )

        if not estado:
            flash('El estado de la orden es obligatorio.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'ordenes/editar_orden.html',
                orden=(id, numero_mesa, orden[2], estado, mesero_texto),
                meseros=meseros
            )

        if len(estado) > 20:
            flash('El estado no puede superar los 20 caracteres.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'ordenes/editar_orden.html',
                orden=(id, numero_mesa, orden[2], estado, mesero_texto),
                meseros=meseros
            )

        try:
            mesero_id = int(mesero_texto)
        except ValueError:
            mesero_id = None

        if not any(mesero[0] == mesero_id for mesero in meseros):
            flash('Debes seleccionar un mesero existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'ordenes/editar_orden.html',
                orden=(id, numero_mesa, orden[2], estado, mesero_texto),
                meseros=meseros
            )

        cursor.execute(
            """
            UPDATE ordenes
            SET numero_mesa = %s, estado = %s, mesero_id = %s
            WHERE orden_id = %s
            """,
            (numero_mesa, estado, mesero_id, id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Orden actualizada correctamente.', 'success')
        return redirect('/ordenes')

    cursor.close()
    conexion.close()

    return render_template(
        'ordenes/editar_orden.html',
        orden=orden,
        meseros=meseros
    )
@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_orden(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM ordenes WHERE orden_id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect('/ordenes')
