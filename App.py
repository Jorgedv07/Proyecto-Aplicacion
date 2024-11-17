import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, flash
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

@app.route('/registro_socio', methods=['POST'])
def registro_socio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO socios (nombre, email) VALUES (%s, %s)', (nombre, email))
        mysql.connection.commit()
        flash('Socio registrado con éxito')
        return redirect(url_for('Index'))

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

@app.route('/registro_hincha', methods=['POST'])
def registro_hincha():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO hinchas (nombre, email) VALUES (%s, %s)', (nombre, email))
        mysql.connection.commit()
        flash('Hincha registrado con éxito')
        return redirect(url_for('Index'))

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
@app.route('/partidos')
def lista_partidos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM partidos')
    partidos = cur.fetchall()
    return render_template('partidos/lista.html', partidos=partidos)

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


if __name__ == '__main__':
    app.run(port=3000, debug=True)
