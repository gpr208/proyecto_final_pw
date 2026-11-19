from flask import Blueprint, render_template, request, redirect, flash
from math import isfinite
from app.database import obtener_conexion

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.route('/probar-conexion')
def probar_conexion():
    try:
        conexion = obtener_conexion()
        conexion.close()
        return "Conexion con PostgreSQL exitosa"
    except Exception as error:
        return f"Error de conexion: {error}"


@bp.route('/', strict_slashes=False)
def listar_categorias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM categorias ORDER BY categoria_id")
    categorias = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('categorias/categorias.html', categorias=categorias)

@bp.route('/nueva', methods=['GET', 'POST'])
def nueva_categoria():

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre de la categoria es obligatorio.', 'danger')
            return render_template('categorias/nueva_categoria.html')

        if len(nombre) > 50:
            flash('El nombre no puede superar los 50 caracteres.', 'danger')
            return render_template('categorias/nueva_categoria.html')

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)",
            (nombre, descripcion)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash('Categoria registrada correctamente.', 'success')
        return redirect('/categorias')

    return render_template('categorias/nueva_categoria.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre de la categoria es obligatorio.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'categorias/editar_categoria.html',
                categoria=(id, nombre, descripcion)
            )

        if len(nombre) > 50:
            flash('El nombre no puede superar los 50 caracteres.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'categorias/editar_categoria.html',
                categoria=(id, nombre, descripcion)
            )

        cursor.execute(
            """
            UPDATE categorias
            SET nombre = %s, descripcion = %s
            WHERE categoria_id = %s
            """,
            (nombre, descripcion, id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Categoria actualizada correctamente.', 'success')
        return redirect('/categorias')

    cursor.execute(
        "SELECT * FROM categorias WHERE categoria_id = %s",
        (id,)
    )

    categoria = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        'categorias/editar_categoria.html',
        categoria=categoria
    )

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_categoria(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM categorias WHERE categoria_id = %s",
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/categorias')
