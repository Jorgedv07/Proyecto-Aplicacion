import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia esto si tu usuario es diferente
app.config['MYSQL_PASSWORD'] = ''  # Asegúrate de agregar tu contraseña si tienes una
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Configuración de la clave secreta
app.secret_key = 'mysecretkey'

# Ruta de bienvenida - Muestra opciones iniciales
@app.route('/')
def Index():
  cur = mysql.connection.cursor()  
  cur.execute('SELECT * FROM contacts')
  data = cur.fetchall()
  return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("""
      UPDATE contacts
      SET fullname = %s,
          email = %s,
          phone = %s
      WHERE id = %s
    """, (fullname, email, phone, id))
    mysql.connection.commit()
    flash('Contact Updated Successfully')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


# --- Rutas para la tabla de socios ---

# Ruta para mostrar el formulario de registro de socios
@app.route('/registro_socio', methods=['GET', 'POST'])
def registro_socio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        # Conexión a la base de datos
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO socios (nombre, email) VALUES (%s, %s)', (nombre, email))
        mysql.connection.commit()
        cur.close()
        session['es_socio'] = True
        session['descuento'] = 0.3  # Ejemplo de descuento para socios
        flash('Tu registro como socio ha sido exitoso. ¡Disfruta de los beneficios!')
        return redirect(url_for('mostrar_partidos'))
    return render_template('socios/registro.html')  # Mostrar el formulario


@app.route('/compra_socio', methods=['POST'])
def compra_socio():
    if request.method == 'POST':
        socio_id = request.form['socio_id']
        partido_id = request.form['partido_id']
        beneficio = request.form['beneficio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO compras_socios (socio_id, partido_id, beneficio) VALUES (%s, %s, %s)',
                    (socio_id, partido_id, beneficio))
        mysql.connection.commit()
        flash('Compra como socio registrada')
        return redirect(url_for('Index'))
    
    # --- Rutas CRUD para la tabla de socios ---

# Ver todos los socios
@app.route('/socios')
def lista_socios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM socios')
    socios = cur.fetchall()
    return render_template('socios/lista.html', socios=socios)

# Editar socio
@app.route('/edit_socio/<id>')
def get_socio(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM socios WHERE id = %s', (id,))
    socio = cur.fetchone()
    return render_template('socios/edit.html', socio=socio)

@app.route('/update_socio/<id>', methods=['POST'])
def update_socio(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE socios SET nombre = %s, email = %s WHERE id = %s', (nombre, email, id))
        mysql.connection.commit()
        flash('Socio actualizado correctamente')
        return redirect(url_for('lista_socios'))

# Eliminar socio
@app.route('/delete_socio/<id>')
def delete_socio(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM socios WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Socio eliminado correctamente')
    return redirect(url_for('lista_socios'))


# --- Rutas para la tabla de hinchas ---

# Ruta para mostrar el formulario de registro de hinchas
@app.route('/registro_hincha', methods=['GET', 'POST'])
def registro_hincha():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        # Conexión a la base de datos
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO hinchas (nombre, email) VALUES (%s, %s)', (nombre, email))
        mysql.connection.commit()
        cur.close()
        session['es_socio'] = False
        flash('Hincha registrado exitosamente')
        return redirect(url_for('mostrar_partidos'))  # Redirigir a la página principal después de registrar
    return render_template('hinchas/registroh.html')  # Mostrar el formulario

@app.route('/compra_hincha', methods=['POST'])
def compra_hincha():
    if request.method == 'POST':
        hincha_id = request.form['hincha_id']
        partido_id = request.form['partido_id']
        localidad = request.form['localidad']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO compras_hinchas (hincha_id, partido_id, localidad, precio) VALUES (%s, %s, %s, %s)',
                    (hincha_id, partido_id, localidad, precio))
        mysql.connection.commit()
        flash('Compra como hincha registrada')
        return redirect(url_for('Index'))
    
    # --- Rutas CRUD para la tabla de hinchas ---

# Ver todos los hinchas
@app.route('/hinchas')
def lista_hinchas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM hinchas')
    hinchas = cur.fetchall()
    return render_template('hinchas/lista.html', hinchas=hinchas)

# Editar hincha
@app.route('/edit_hincha/<id>')
def get_hincha(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM hinchas WHERE id = %s', (id,))
    hincha = cur.fetchone()
    return render_template('hinchas/edit.html', hincha=hincha)

@app.route('/update_hincha/<id>', methods=['POST'])
def update_hincha(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE hinchas SET nombre = %s, email = %s WHERE id = %s', (nombre, email, id))
        mysql.connection.commit()
        flash('Hincha actualizado correctamente')
        return redirect(url_for('lista_hinchas'))

# Eliminar hincha
@app.route('/delete_hincha/<id>')
def delete_hincha(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM hinchas WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Hincha eliminado correctamente')
    return redirect(url_for('lista_hinchas'))


# --- Rutas CRUD para la tabla de partidos ---

# Ver todos los partidos
@app.route('/partidos', methods=['GET', 'POST'])
def mostrar_partidos():
    # Verificar si el usuario es socio
    es_socio = session.get('es_socio', False)
    
    # Conexión a la base de datos
    cursor = mysql.connection.cursor()

    # Obtener todos los partidos disponibles
    cursor.execute("SELECT id, equipos, fecha, hora, ubicacion, precio_general, precio_preferencial, precio_vip FROM partidos")
    partidos = cursor.fetchall()

    # Si el formulario es enviado
    if request.method == 'POST':
        # Obtener el id del partido seleccionado
        partido_id = request.form['partido_id']
        # Obtener el precio de acuerdo al tipo de socio
        if es_socio:
            # Obtener el descuento
            descuento = session.get('descuento', 0)
            # Guardar la compra en la base de datos, puedes agregar la lógica que desees aquí.
            cursor.execute("INSERT INTO compras_socios (partido_id, descuento) VALUES (%s, %s)", (partido_id, descuento))
            mysql.connection.commit()

            # Mostrar mensaje de éxito
            flash('Compra registrada exitosamente con el descuento para socios.')

        else:
            # Guardar compra de hincha (sin descuento)
            cursor.execute("INSERT INTO compras_hinchas (partido_id) VALUES (%s)", (partido_id,))
            mysql.connection.commit()
            flash('Compra registrada exitosamente.')

        return redirect(url_for('mostrar_partidos'))  # Redirigir después de la compra

    return render_template('partidos.html', partidos=partidos, es_socio=es_socio)
# Agregar partido
@app.route('/add_partido', methods=['POST'])
def add_partido():
    if request.method == 'POST':
        equipo_local = request.form['equipo_local']
        equipo_visitante = request.form['equipo_visitante']
        fecha = request.form['fecha']
        lugar = request.form['lugar']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO partidos (equipo_local, equipo_visitante, fecha, lugar) VALUES (%s, %s, %s, %s)', 
                    (equipo_local, equipo_visitante, fecha, lugar))
        mysql.connection.commit()
        flash('Partido agregado correctamente')
        return redirect(url_for('lista_partidos'))

# Editar partido
@app.route('/edit_partido/<id>')
def get_partido(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM partidos WHERE id = %s', (id,))
    partido = cur.fetchone()
    return render_template('partidos/edit.html', partido=partido)

@app.route('/update_partido/<id>', methods=['POST'])
def update_partido(id):
    if request.method == 'POST':
        equipo_local = request.form['equipo_local']
        equipo_visitante = request.form['equipo_visitante']
        fecha = request.form['fecha']
        lugar = request.form['lugar']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE partidos 
            SET equipo_local = %s, equipo_visitante = %s, fecha = %s, lugar = %s 
            WHERE id = %s
        """, (equipo_local, equipo_visitante, fecha, lugar, id))
        mysql.connection.commit()
        flash('Partido actualizado correctamente')
        return redirect(url_for('lista_partidos'))

# Eliminar partido
@app.route('/delete_partido/<id>')
def delete_partido(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM partidos WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Partido eliminado correctamente')
    return redirect(url_for('lista_partidos'))

# Ruta para comprar boletos (requiere estar registrado)
@app.route('/comprar_boletos', methods=['GET', 'POST'])
def comprar_boletos():
    if request.method == 'POST':
        partido = request.form['partido']
        cantidad = request.form['cantidad']
        # Lógica para guardar la compra en la base de datos
        flash('Compra realizada exitosamente')
        return redirect(url_for('Index'))
    return render_template('compras/seleccion_boletos.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
