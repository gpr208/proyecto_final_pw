from flask import Blueprint, render_template, request, redirect, flash
from math import isfinite
from app.database import obtener_conexion

bp = Blueprint("productos", __name__, url_prefix="/productos")


@bp.route('/', strict_slashes=False)
def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT productos.producto_id,
               productos.nombre,
               productos.precio,
               productos.stock,
               categorias.nombre
        FROM productos
        LEFT JOIN categorias
        ON productos.categoria_id = categorias.categoria_id
        ORDER BY productos.producto_id
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('productos/productos.html', productos=productos)

@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT categoria_id, nombre FROM categorias ORDER BY nombre")
    categorias = cursor.fetchall()

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        precio_texto = request.form.get('precio', '').strip()
        stock_texto = request.form.get('stock', '').strip()
        categoria_texto = request.form.get('categoria_id', '').strip()

        if not nombre:
            flash('El nombre del producto es obligatorio.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('productos/nuevo_producto.html', categorias=categorias)

        if len(nombre) > 100:
            flash('El nombre no puede superar los 100 caracteres.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('productos/nuevo_producto.html', categorias=categorias)

        # Validar precio
        try:
            precio = float(precio_texto)
            if not isfinite(precio) or precio <= 0:
                raise ValueError
        except ValueError:
            flash('El precio debe ser un numero mayor que cero.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('productos/nuevo_producto.html', categorias=categorias)

        try:
            stock = int(stock_texto)
            if stock < 0:
                raise ValueError
        except ValueError:
            flash('El stock debe ser un numero entero igual o mayor que cero.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('productos/nuevo_producto.html', categorias=categorias)

        try:
            categoria_id = int(categoria_texto)
        except ValueError:
            categoria_id = None

        if not any(categoria[0] == categoria_id for categoria in categorias):
            flash('Debes seleccionar una categoria existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template('productos/nuevo_producto.html', categorias=categorias)

        cursor.execute(
            """
            INSERT INTO productos (nombre, precio, stock, categoria_id)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre, precio, stock, categoria_id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Producto registrado correctamente.', 'success')
        return redirect('/productos')

    cursor.close()
    conexion.close()

    return render_template('productos/nuevo_producto.html', categorias=categorias)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT categoria_id, nombre FROM categorias ORDER BY nombre")
    categorias = cursor.fetchall()

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        precio_texto = request.form.get('precio', '').strip()
        stock_texto = request.form.get('stock', '').strip()
        categoria_texto = request.form.get('categoria_id', '').strip()

        try:
            categoria_id = int(categoria_texto)
        except ValueError:
            categoria_id = None

        producto_form = (id, nombre, precio_texto, stock_texto, categoria_id)

        # Validar nombre
        if not nombre:
            flash('El nombre del producto es obligatorio.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'productos/editar_producto.html',
                producto=producto_form,
                categorias=categorias
            )

        if len(nombre) > 100:
            flash('El nombre no puede superar los 100 caracteres.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'productos/editar_producto.html',
                producto=producto_form,
                categorias=categorias
            )

        try:
            precio = float(precio_texto)
            if not isfinite(precio) or precio <= 0:
                raise ValueError
        except ValueError:
            flash('El precio debe ser un numero mayor que cero.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'productos/editar_producto.html',
                producto=producto_form,
                categorias=categorias
            )

        # Validar stock
        try:
            stock = int(stock_texto)
            if stock < 0:
                raise ValueError
        except ValueError:
            flash('El stock debe ser un numero entero igual o mayor que cero.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'productos/editar_producto.html',
                producto=producto_form,
                categorias=categorias
            )

        # Validar categoria
        if not any(categoria[0] == categoria_id for categoria in categorias):
            flash('Debes seleccionar una categoria existente.', 'danger')
            cursor.close()
            conexion.close()
            return render_template(
                'productos/editar_producto.html',
                producto=producto_form,
                categorias=categorias
            )

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s, precio = %s, stock = %s, categoria_id = %s
            WHERE producto_id = %s
            """,
            (nombre, precio, stock, categoria_id, id)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Producto actualizado correctamente.', 'success')
        return redirect('/productos')

    cursor.execute(
        "SELECT * FROM productos WHERE producto_id = %s",
        (id,)
    )
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        'productos/editar_producto.html',
        producto=producto,
        categorias=categorias
    )
@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE producto_id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect('/productos')
