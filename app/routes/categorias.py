from flask import Blueprint, render_template, request, redirect, flash
import psycopg2
from app.database import obtener_conexion

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.route('/', strict_slashes=False)
def listar_categorias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM categorias ORDER BY categoria_id")
    categorias = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('categorias/categorias.html',
                           categorias=categorias)


@bp.route('/nueva', methods=['GET', 'POST'])
def nueva_categoria():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre or len(nombre) > 50:
            flash('El nombre es obligatorio y máximo de 50 caracteres.', 'danger')
        else:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO categorias (nombre, descripcion)
                VALUES (%s, %s)
            """, (nombre, descripcion))

            conexion.commit()
            cursor.close()
            conexion.close()

            flash('Categoría registrada correctamente.', 'success')
            return redirect('/categorias')

    return render_template('categorias/nueva_categoria.html')


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre or len(nombre) > 50:
            flash('El nombre es obligatorio y máximo de 50 caracteres.', 'danger')
        else:
            cursor.execute("""
                UPDATE categorias
                SET nombre=%s, descripcion=%s
                WHERE categoria_id=%s
            """, (nombre, descripcion, id))

            conexion.commit()
            cursor.close()
            conexion.close()

            flash('Categoría actualizada correctamente.', 'success')
            return redirect('/categorias')

    cursor.execute("SELECT * FROM categorias WHERE categoria_id=%s", (id,))
    categoria = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template('categorias/editar_categoria.html',
                           categoria=categoria)


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_categoria(id):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM categorias WHERE categoria_id=%s", (id,))

        if cursor.rowcount:
            conexion.commit()
            flash('Categoría eliminada correctamente.', 'success')
        else:
            flash('La categoría no existe.', 'warning')

    except psycopg2.errors.ForeignKeyViolation:
        conexion.rollback()
        flash('No puedes eliminar una categoría que tiene productos asociados.', 'danger')

    except psycopg2.Error:
        conexion.rollback()
        flash('Error al eliminar la categoría.', 'danger')

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return redirect('/categorias')