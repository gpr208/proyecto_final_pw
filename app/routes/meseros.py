from flask import Blueprint, render_template, request, redirect, flash
from datetime import datetime
from app.database import obtener_conexion
import psycopg2

bp = Blueprint("meseros", __name__, url_prefix="/meseros")

@bp.route('/', strict_slashes=False)
def listar_meseros():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM meseros ORDER BY mesero_id"
    )

    meseros = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('meseros/meseros.html', meseros=meseros)



@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_mesero():

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip()
        fecha_texto = request.form.get('fecha', '').strip()

        if not nombre:
            flash('El nombre del mesero es obligatorio.', 'danger')
            return render_template('meseros/nuevo_mesero.html')

        if len(nombre) > 100:
            flash('El nombre no puede superar los 100 caracteres.', 'danger')
            return render_template('meseros/nuevo_mesero.html')

        if len(telefono) > 20:
            flash('El telefono no puede superar los 20 caracteres.', 'danger')
            return render_template('meseros/nuevo_mesero.html')

        try:
            fecha = datetime.strptime(fecha_texto, '%Y-%m-%d').date()
        except ValueError:
            flash('Debes ingresar una fecha de contratacion valida.', 'danger')
            return render_template('meseros/nuevo_mesero.html')

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO meseros (nombre, telefono, fecha_contratacion)
            VALUES (%s, %s, %s)
            """,
            (nombre, telefono or None, fecha)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Mesero registrado correctamente.', 'success')
        return redirect('/meseros')

    return render_template('meseros/nuevo_mesero.html')


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_mesero(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip()
        fecha_texto = request.form.get('fecha', '').strip()

        mesero_form = (id, nombre, telefono, fecha_texto)

        if not nombre:
            flash('El nombre del mesero es obligatorio.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'meseros/editar_mesero.html',
                mesero=mesero_form
            )

        if len(nombre) > 100:
            flash('El nombre no puede superar los 100 caracteres.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'meseros/editar_mesero.html',
                mesero=mesero_form
            )

        if len(telefono) > 20:
            flash('El telefono no puede superar los 20 caracteres.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'meseros/editar_mesero.html',
                mesero=mesero_form
            )

        try:
            fecha = datetime.strptime(fecha_texto, '%Y-%m-%d').date()
        except ValueError:
            flash('Debes ingresar una fecha de contratacion valida.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'meseros/editar_mesero.html',
                mesero=mesero_form
            )

        cursor.execute(
            """
            UPDATE meseros
            SET nombre = %s, telefono = %s, fecha_contratacion = %s
            WHERE mesero_id = %s
            """,
            (nombre, telefono or None, fecha, id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Mesero actualizado correctamente.', 'success')
        return redirect('/meseros')

    cursor.execute(
        "SELECT * FROM meseros WHERE mesero_id = %s",
        (id,)
    )

    mesero = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        'meseros/editar_mesero.html',
        mesero=mesero
    )

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_mesero(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "DELETE FROM meseros WHERE mesero_id = %s",
            (id,)
        )
        conexion.commit()

    except psycopg2.errors.ForeignKeyViolation:
        conexion.rollback()
        flash('No se puede eliminar porque tiene órdenes asociadas.', 'danger')

    finally:
        cursor.close()
        conexion.close()

    return redirect('/meseros')
