from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="database_name"
)
cursor = db.cursor()

# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/items')
@login_required
def index():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
        db.commit()
        return redirect('/items')
    return render_template('add.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id):
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("UPDATE items SET name = %s WHERE id = %s", (name, item_id))
        db.commit()
        return redirect('/items')
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
@login_required
def delete(item_id):
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    db.commit()
    return redirect('/items')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verifikasi pengguna (ganti dengan logika verifikasi Anda)
        if username == "admin" and password == "password":  # Contoh sederhana
            user = User(1)  # Ganti dengan ID pengguna yang valid
            login_user(user)
            return redirect('/')
        flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)