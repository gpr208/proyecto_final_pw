from flask import Blueprint, render_template, request, redirect, flash
from math import isfinite
import psycopg2
from app.database import obtener_conexion

bp = Blueprint("productos", __name__, url_prefix="/productos")


def validar_producto(form, categorias):
    nombre = form.get('nombre', '').strip()

    try:
        precio = float(form.get('precio', ''))
        if not isfinite(precio) or precio <= 0:
            raise ValueError
    except ValueError:
        return None, 'El precio debe ser mayor que cero.'

    try:
        stock = int(form.get('stock', ''))
        if stock < 0:
            raise ValueError
    except ValueError:
        return None, 'El stock debe ser un entero positivo o cero.'

    try:
        categoria = int(form.get('categoria_id', ''))
    except ValueError:
        categoria = None

    if not nombre or len(nombre) > 100:
        return None, 'El nombre es obligatorio y máximo de 100 caracteres.'

    if not any(c[0] == categoria for c in categorias):
        return None, 'Selecciona una categoría existente.'

    return (nombre, precio, stock, categoria), None


@bp.route('/', strict_slashes=False)
def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT p.producto_id, p.nombre, p.precio,
               p.stock, c.nombre
        FROM productos p
        LEFT JOIN categorias c
        ON p.categoria_id = c.categoria_id
        ORDER BY p.producto_id
    """)

    productos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template('productos/productos.html',
                           productos=productos)


@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT categoria_id, nombre FROM categorias")
    categorias = cursor.fetchall()

    if request.method == 'POST':
        datos, error = validar_producto(request.form, categorias)

        if error:
            flash(error, 'danger')
        else:
            cursor.execute("""
                INSERT INTO productos
                (nombre, precio, stock, categoria_id)
                VALUES (%s, %s, %s, %s)
            """, datos)

            conexion.commit()
            flash('Producto registrado correctamente.', 'success')
            cursor.close()
            conexion.close()
            return redirect('/productos')

    cursor.close()
    conexion.close()

    return render_template('productos/nuevo_producto.html',
                           categorias=categorias)


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT categoria_id, nombre FROM categorias")
    categorias = cursor.fetchall()

    if request.method == 'POST':
        datos, error = validar_producto(request.form, categorias)

        producto = (
            id,
            request.form.get('nombre', ''),
            request.form.get('precio', ''),
            request.form.get('stock', ''),
            request.form.get('categoria_id', '')
        )

        if error:
            flash(error, 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'productos/editar_producto.html',
                producto=producto,
                categorias=categorias
            )

        cursor.execute("""
            UPDATE productos
            SET nombre=%s, precio=%s, stock=%s, categoria_id=%s
            WHERE producto_id=%s
        """, datos + (id,))

        conexion.commit()
        flash('Producto actualizado correctamente.', 'success')
        cursor.close()
        conexion.close()
        return redirect('/productos')

    cursor.execute("SELECT * FROM productos WHERE producto_id=%s", (id,))
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template('productos/editar_producto.html',
                           producto=producto, categorias=categorias)


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM productos WHERE producto_id=%s", (id,))

        if cursor.rowcount:
            conexion.commit()
            flash('Producto eliminado correctamente.', 'success')
        else:
            flash('El producto no existe.', 'warning')

    except psycopg2.errors.ForeignKeyViolation:
        conexion.rollback()
        flash('El producto tiene detalles de órdenes asociados.', 'danger')

    except psycopg2.Error:
        conexion.rollback()
        flash('Error al eliminar el producto.', 'danger')

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return redirect('/productos')
