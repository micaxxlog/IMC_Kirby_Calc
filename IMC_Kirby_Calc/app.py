from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = '578234'

def init_db():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT, email TEXT UNIQUE, fecha_nacimiento TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('imc'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        fecha = request.form['fecha']
        password = hash_password(request.form['password'])

        conn = sqlite3.connect('usuarios.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (nombre, apellido, email, fecha_nacimiento, password) VALUES (?, ?, ?, ?, ?)", 
                      (nombre, apellido, email, fecha, password))
            conn.commit()
        except sqlite3.IntegrityError:
            error = 'El correo electrónico ya está registrado.'
        conn.close()

        if not error:
            session['user'] = email
            return redirect(url_for('imc'))

    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['loginEmail']
        password = request.form['loginPassword']

        conn = sqlite3.connect('usuarios.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password(user[0], password):
            session['user'] = email
            return redirect(url_for('imc'))
        else:
            error = 'Correo electrónico o contraseña incorrectos.'

    return render_template('login.html', error=error)

@app.route('/imc', methods=['GET', 'POST'])
def imc():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('imc.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=40000)
